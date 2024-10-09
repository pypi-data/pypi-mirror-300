#!/usr/bin/env python3
# -*- coding: utf-8 -*-
#-------------------------------------------------------------------------------
# This file is part of Mentat system (https://mentat.cesnet.cz/).
#
# Copyright (C) since 2011 CESNET, z.s.p.o (http://www.ces.net/)
# Use of this source is governed by the MIT license, see LICENSE file.
#-------------------------------------------------------------------------------


"""
Library for generating event reports.

The implementation is based on :py:class:`mentat.reports.base.BaseReporter`.
"""


__author__  = "Jan Mach <jan.mach@cesnet.cz>"
__credits__ = "Pavel Kácha <pavel.kacha@cesnet.cz>, Andrea Kropáčová <andrea.kropacova@cesnet.cz>"


import os
import json
import datetime
import zipfile
import socket
from copy import deepcopy
from sqlalchemy.orm.attributes import flag_modified

#
# Custom libraries
#
from pynspect.jpath   import jpath_values
from pynspect.gparser import PynspectFilterParser
from pynspect.filters import DataObjectFilter

from mentat.datatype.sqldb import EventClassModel
from mentat.idea.internal import IDEAFilterCompiler

import mentat.const
import mentat.datatype.internal
import mentat.idea.internal
import mentat.stats.idea
import mentat.services.whois
from mentat.const import tr_
from mentat.reports.utils import StorageThresholdingCache, NoThresholdingCache
from mentat.datatype.sqldb import EventReportModel, DetectorModel
from mentat.emails.event import ReportEmail
from mentat.reports.base import BaseReporter
from mentat.services.eventstorage import record_to_idea


REPORT_SUBJECT_SUMMARY = tr_("[{:s}] {:s} - Notice about possible problems in your network")
"""Subject for summary report emails."""

REPORT_SUBJECT_EXTRA = tr_("[{:s}] {:s} - Notice about possible problems regarding host {:s}")
"""Subject for extra report emails."""

REPORT_EMAIL_TEXT_WIDTH = 90
"""Width of the report email text."""


def json_default(val):
    """
    Helper function for JSON serialization of non basic data types.
    """
    if isinstance(val, datetime.datetime):
        return val.isoformat()
    return str(val)


class EventReporter(BaseReporter):
    """
    Implementation of reporting class providing Mentat event reports.
    """

    def __init__(self, logger, reports_dir, templates_dir, global_fallback, locale, timezone, eventservice, sqlservice, mailer, groups_dict, settings_dict, whoismodule, thresholding = True, item_limit = 15):
        super().__init__(logger, reports_dir, templates_dir, locale, timezone)

        self.eventservice    = eventservice
        self.sqlservice      = sqlservice
        self.mailer          = mailer

        self.global_fallback = global_fallback

        self.renderer.globals['item_limit'] = item_limit

        self.filter_parser   = PynspectFilterParser()
        self.filter_compiler = IDEAFilterCompiler()
        self.filter_worker   = DataObjectFilter()

        self.whoismodule = whoismodule

        self.groups_dict = groups_dict
        self.settings_dict = settings_dict
        self.detectors_dict = {det.name : det for det in self.sqlservice.session.query(DetectorModel).all()}

        self.message_id_dict = self._init_message_id_dict()

        self.filter_parser.build()

        if thresholding:
            self.tcache = StorageThresholdingCache(logger, eventservice)
        else:
            self.tcache = NoThresholdingCache()

    def _init_message_id_dict(self):
        result = {'thresholds': {}}
        thresholds = self.eventservice.fetch_thresholds()
        for (key, label) in thresholds:
            if not label:
                continue
            result['thresholds'][key] = label
        return result

    def _setup_renderer(self, templates_dir):
        """
        *Interface reimplementation* of :py:func:`mentat.reports.base.BaseReporter._setup_renderer`
        """

        renderer = super()._setup_renderer(templates_dir)

        renderer.globals['idea_path_valueset'] = self.j2t_idea_path_valueset

        return renderer

    @staticmethod
    def j2t_idea_path_valueset(message_s, jpath_s):
        """
        Calculate and return set of all values on all given jpaths in all given
        messages. Messages and jpaths can also be single values.
        """
        result = {}
        if not isinstance(message_s, list):
            message_s = [message_s]
        if not isinstance(jpath_s, list):
            jpath_s = [jpath_s]
        for item in message_s:
            for jpath in jpath_s:
                values = item.get_jpath_values(jpath)
                for val in values:
                    result[val] = 1
        return list(sorted(result.keys()))

    #---------------------------------------------------------------------------

    def cleanup(self, ttl):
        """
        Cleanup thresholding cache and remove all records with TTL older than given
        value.

        :param datetime.datetime time_h: Upper cleanup time threshold.
        :return: Number of removed records.
        :rtype: int
        """
        return self.tcache.cleanup(ttl)

    def report(self, abuse_group, severity, time_l, time_h, template_vars = None, testdata = False):
        """
        Perform reporting for given most specific abuse group, event severity and time window.

        :param mentat.datatype.internal.GroupModel abuse_group: Abuse group.
        :param str severity: Severity for which to perform reporting.
        :param datetime.datetime time_l: Lower reporting time threshold.
        :param datetime.datetime time_h: Upper reporting time threshold.
        :param dict template_vars: Dictionary containing additional template variables.
        :param bool testdata: Switch to use test data for reporting.
        """
        result = {}
        result['ts_from_s'] = time_l.isoformat()
        result['ts_to_s']   = time_h.isoformat()
        result['ts_from']   = int(time_l.timestamp())
        result['ts_to']     = int(time_h.timestamp())

        events = {}

        while True:
            # A: Fetch events from database.
            events_fetched = self.fetch_severity_events(abuse_group, severity, time_l, time_h, testdata)

            result['evcount_new'] = len(events_fetched)
            if not events_fetched:
                break

            # B: Perform event filtering according to custom group filters and aggregate by source.
            events_passed_filters, aggregated_events, fltlog, passed_cnt = self.filter_events(abuse_group.name, events_fetched)
            for groups in aggregated_events:
                group_chain = groups[0]
                if str(group_chain) not in result:
                    result[str(group_chain)] = {}
                result[str(group_chain)]['evcount_all'] = len(events_passed_filters[groups])
                result[str(group_chain)]['evcount_new'] = result[str(group_chain)]['evcount_all']

            result['evcount_flt'] = passed_cnt
            result['evcount_flt_blk'] = result['evcount_new'] - passed_cnt
            result['filtering'] = fltlog

            if result['evcount_flt']:
                self.logger.info(
                    "%s: Filters let %d events through, %d blocked.",
                    abuse_group.name,
                    result['evcount_flt'],
                    result['evcount_flt_blk']
                )
            else:
                self.logger.info(
                    "%s: Filters blocked all %d events, nothing to report.",
                    abuse_group.name,
                    result['evcount_flt_blk']
                )
                break

            # Create new dictionary to store events coming from credible detectors.
            aggregated_credible_events = {}
            for groups, events_aggr in aggregated_events.items():
                group_chain = groups[0]
                # C: Discard events from detectors with low credibility.
                _events_aggr, blocked_cnt = self.filter_events_by_credibility(events_aggr)
                # If all events were discarded, _events_aggr is None.
                if _events_aggr:
                    aggregated_credible_events[groups] = _events_aggr
                # Save information about how many events passed and how many were discarded.
                result[str(group_chain)]['evcount_det'] = result['evcount_flt'] - blocked_cnt
                result[str(group_chain)]['evcount_det_blk'] = blocked_cnt

            for groups, events_aggr in aggregated_credible_events.items():
                group_chain = groups[0]
                # D: Perform event thresholding.
                events_thr, events_aggr = self.threshold_events(events_aggr, abuse_group, group_chain, severity, time_h)

                result[str(group_chain)]['evcount_thr'] = len(events_thr)
                result[str(group_chain)]['evcount_thr_blk'] = result[str(group_chain)]['evcount_det'] - len(events_thr)
                if not events_thr:
                    continue

                # E: Save aggregated events for further processing.
                events[groups] = {}
                events[groups]['regular'] = events_thr
                events[groups]['regular_aggr'] = events_aggr

            break

        while True:
            # A: Detect possible event relapses.
            events_rel = self.relapse_events(abuse_group, severity, time_h)
            if not events_rel:
                break

            # B: Aggregate events by sources for further processing.
            events_rel, events_aggregated, fltlog, passed_cnt = self.filter_events(abuse_group.name, map(record_to_idea, events_rel))
            for groups, events_aggr in events_aggregated.items():
                group_chain = groups[0]
                if str(group_chain) not in result:
                    result[str(group_chain)] = {}
                    result[str(group_chain)]['evcount_all'] = 0
                result[str(group_chain)]['evcount_rlp'] = len(events_rel[groups])
                result[str(group_chain)]['evcount_all'] += result[str(group_chain)]['evcount_rlp']
                if groups not in events:
                    events[groups] = {}
                events[groups]['relapsed'] = events_rel[groups]
                events[groups]['relapsed_aggr'] = events_aggr

            break

        if not events:
            result['result'] = 'skipped-no-events'

        for groups, groups_events in events.items():
            (group_chain, fallback_groups) = groups
            # Check, that there is anything to report (regular and/or relapsed events).
            if 'regular' not in groups_events and 'relapsed' not in groups_events:
                result[str(group_chain)]['evcount_rep'] = 0
                result[str(group_chain)]['result'] = 'skipped-no-events'
                continue
            result[str(group_chain)]['evcount_rep'] = len(groups_events.get('regular', [])) + len(groups_events.get('relapsed', []))

            main_group_settings = self.settings_dict[group_chain[0]]
            original_group_only = len(group_chain) == 1 and group_chain[0] == abuse_group.name

            # Generate summary report.
            report_summary = self.report_summary(result, groups_events, group_chain, fallback_groups, main_group_settings,
                                                 severity, time_l, time_h, original_group_only, template_vars, testdata)

            # Generate extra reports.
            self.report_extra(report_summary, result, groups_events, group_chain, fallback_groups, main_group_settings,
                              severity, time_l, time_h, template_vars, testdata)

            # Update thresholding cache.
            self.update_thresholding_cache(groups_events, main_group_settings, severity, time_h)

            result['result'] = 'reported'
            result[str(group_chain)]['result'] = 'reported'
        return result

    def report_summary(self, result, events, group_chain, fallback_groups, settings, severity, time_l, time_h, original_group_only, template_vars = None, testdata = False):
        """
        Generate summary report from given events for given abuse group, severity and period.

        :param dict result: Reporting result structure with various usefull metadata.
        :param dict events: Dictionary structure with IDEA events to be reported.
        :param list group_chain: List of resolved abuse groups.
        :param list fallback_groups: List of fallback abuse groups.
        :param mentat.reports.event.ReportingSettings settings: Reporting settings.
        :param str severity: Severity for which to perform reporting.
        :param datetime.datetime time_l: Lower reporting time threshold.
        :param datetime.datetime time_h: Upper reporting time threshold.
        :param bool original_group_only: Check if there is only the most specific abuse group.
        :param dict template_vars: Dictionary containing additional template variables.
        :param bool testdata: Switch to use test data for reporting.
        """
        # Instantinate the report object.
        evcount_flt_blk = result.get('evcount_flt_blk', 0) if original_group_only else 0
        report = EventReportModel(
            groups   = [self.groups_dict[group] for group in group_chain],
            severity = severity,
            type     = mentat.const.REPORT_TYPE_SUMMARY,
            dt_from  = time_l,
            dt_to    = time_h,

            evcount_rep     = result[str(group_chain)].get('evcount_rep', 0),
            evcount_all     = result[str(group_chain)].get('evcount_all', 0) + evcount_flt_blk,
            evcount_new     = result[str(group_chain)].get('evcount_new', 0) + evcount_flt_blk,
            evcount_flt     = result[str(group_chain)].get('evcount_new', 0),
            evcount_flt_blk = evcount_flt_blk,
            evcount_det     = result[str(group_chain)].get('evcount_det', 0),
            evcount_det_blk = result[str(group_chain)].get('evcount_det_blk', 0),
            evcount_thr     = result[str(group_chain)].get('evcount_thr', 0),
            evcount_thr_blk = result[str(group_chain)].get('evcount_thr_blk', 0),
            evcount_rlp     = result[str(group_chain)].get('evcount_rlp', 0),

            flag_testdata = testdata,

            filtering = result.get('filtering', {}) if original_group_only else {}
        )
        report.generate_label()
        report.calculate_delta()

        events_all = events.get('regular', []) + events.get('relapsed', [])
        report.statistics = mentat.stats.idea.truncate_evaluations(
            mentat.stats.idea.evaluate_events(events_all)
        )

        # Save report data to disk in JSON format.
        self._save_to_json_files(
            events_all,
            'security-report-{}.json'.format(report.label)
        )

        report.structured_data = self.prepare_structured_data(events.get('regular_aggr', {}), events.get('relapsed_aggr', {}), settings)

        # Add report to database session.
        self.sqlservice.session.add(report)

        # Remove groups which don't want to receive a summary.
        final_group_list = [g for g in group_chain if self.settings_dict[g].mode
                            in (mentat.const.REPORTING_MODE_SUMMARY, mentat.const.REPORTING_MODE_BOTH)]
        # Send report via email.
        if final_group_list:
            self._mail_report(report, self.settings_dict[final_group_list[0]], final_group_list, fallback_groups, result, template_vars)

        # Commit all changes on report object to database.
        self.sqlservice.session.commit()

        result['summary_id'] = report.label

        return report

    def report_extra(self, parent_rep, result, events, group_chain, fallback_groups, settings, severity, time_l, time_h, template_vars = None, testdata = False):
        """
        Generate extra reports from given events for given abuse group, severity and period.

        :param mentat.datatype.sqldb.EventReportModel parent_rep: Parent summary report.
        :param dict result: Reporting result structure with various usefull metadata.
        :param dict events: Dictionary structure with IDEA events to be reported.
        :param list group_chain: List of resolved abuse groups.
        :param list fallback_groups: List of fallback abuse groups.
        :param mentat.reports.event.ReportingSettings settings: Reporting settings.
        :param str severity: Severity for which to perform reporting.
        :param datetime.datetime time_l: Lower reporting time threshold.
        :param datetime.datetime time_h: Upper reporting time threshold.
        :param dict template_vars: Dictionary containing additional template variables.
        :param bool testdata: Switch to use test data for reporting.
        """
        if all(self.settings_dict[g].mode not in (mentat.const.REPORTING_MODE_EXTRA, mentat.const.REPORTING_MODE_BOTH) for g in group_chain):
            return

        sources = list(
            set(
                list(events.get('regular_aggr', {}).keys()) + list(events.get('relapsed_aggr', {}).keys())
            )
        )

        for src in sorted(sources):

            events_regular_aggr = events.get('regular_aggr', {}).get(src, [])
            events_relapsed_aggr = events.get('relapsed_aggr', {}).get(src, [])
            events_all = events_regular_aggr + events_relapsed_aggr

            # Instantinate the report object.
            report = EventReportModel(
                groups   = [self.groups_dict[group] for group in group_chain],
                parent   = parent_rep,
                severity = severity,
                type     = mentat.const.REPORT_TYPE_EXTRA,
                dt_from  = time_l,
                dt_to    = time_h,

                evcount_rep = len(events_all),
                evcount_all = result[str(group_chain)]['evcount_rep'],

                flag_testdata = testdata
            )
            report.generate_label()
            report.calculate_delta()

            report.statistics = mentat.stats.idea.truncate_evaluations(
                mentat.stats.idea.evaluate_events(events_all)
            )

            # Save report data to disk in JSON format.
            self._save_to_json_files(
                events_all,
                'security-report-{}.json'.format(report.label)
            )

            report.structured_data = self.prepare_structured_data({src: events_regular_aggr}, {src: events_relapsed_aggr}, settings)

            # Save the generated report label for the given source.
            self.message_id_dict[src] = report.label

            # Add report to database session.
            self.sqlservice.session.add(report)

            # Send report via email.
            final_group_list = [g for g in group_chain if self.settings_dict[g].mode
                                in (mentat.const.REPORTING_MODE_EXTRA, mentat.const.REPORTING_MODE_BOTH)]
            if final_group_list:
                self._mail_report(report, self.settings_dict[final_group_list[0]], final_group_list, fallback_groups, result, template_vars, src)

            # Commit all changes on report object to database.
            self.sqlservice.session.commit()

            result.setdefault('extra_id', []).append(report.label)

    #---------------------------------------------------------------------------

    @staticmethod
    def prepare_structured_data(events_reg_aggr, events_rel_aggr, settings):
        """
        Prepare structured data for report column

        :param dict events_reg_aggr: List of events as :py:class:`mentat.idea.internal.Idea` objects.
        :param dict events_rel_aggr: List of relapsed events as :py:class:`mentat.idea.internal.Idea` objects.
        :return: Structured data that can be used to generate report message
        :rtype: dict
        """
        result = {}
        result["regular"] = EventReporter.aggregate_events(events_reg_aggr)
        result["relapsed"] = EventReporter.aggregate_events(events_rel_aggr)
        result["timezone"] = str(settings.timezone)
        return result

    #---------------------------------------------------------------------------

    def fetch_severity_events(self, abuse_group, severity, time_l, time_h, testdata = False):
        """
        Fetch events with given severity for given abuse group within given time
        iterval.

        :param abuse_group: Abuse group model object.
        :param str severity: Event severity level to fetch.
        :param datetime.datetime time_l: Lower time interval boundary.
        :param datetime.datetime time_h: Upper time interval boundary.
        :param bool testdata: Switch to use test data for reporting.
        :return: List of events matching search criteria.
        :rtype: list
        """
        count, events = self.eventservice.search_events({
            'st_from':        time_l,
            'st_to':          time_h,
            'groups':         [abuse_group.name],
            'severities':     [severity],
            'categories':     ['Test'],
            'not_categories': not testdata
        })
        if not events:
            self.logger.debug(
                "%s: Found no event(s) with severity '%s' and time interval %s -> %s (%s).",
                abuse_group.name,
                severity,
                time_l.isoformat(),
                time_h.isoformat(),
                str(time_h - time_l)
            )
        else:
            self.logger.info(
                "%s: Found %d event(s) with severity '%s' and time interval %s -> %s (%s).",
                abuse_group.name,
                len(events),
                severity,
                time_l.isoformat(),
                time_h.isoformat(),
                str(time_h - time_l)
            )
        return events

    def _filter_groups(self, groups, event, fltlog):
        filtered_groups = []
        for group in groups:
            filter_list = self.settings_dict[group].setup_filters(self.filter_parser, self.filter_compiler)
            match = self.filter_event(filter_list, event)
            if match:
                self.logger.debug("Event matched filtering rule '%s' of group %s.", match, group)
                fltlog[match] = fltlog.get(match, 0) + 1
            else:
                filtered_groups.append(group)
        return filtered_groups, fltlog

    def filter_one_event(self, src, event, main_group, fltlog):
        """
        Compute and filter resolved abuses for an event with only one source IP address.

        :param ipranges.IP/Net/Range src: Source IP address
        :param mentat.idea.internal.Idea event: Event to be filtered.
        :param str main_group: Abuse group.
        :param dict fltlog: Filtering log.
        :return: List of resolved abuses, list of fallback groups and filtering log as dictionary.
        :rtype: tuple
        """
        # Get resolved abuses for a given source sorted by the priority.
        groups = []
        fallback_groups = []
        for net in self.whoismodule.lookup(src)[::-1]:
            if net['is_base']:
                self.logger.debug(
                    "Adding group '%s' to fallback groups of event with ID '%s' because '%s' belongs to base network.",
                    net['abuse_group'],
                    event['ID'],
                    str(src)
                )
                fallback_groups.append(net['abuse_group'])
            else:
                groups.append(net['abuse_group'])
        # dict.fromkeys uniquifies the list while preserving the order of the elements.
        groups = list(dict.fromkeys(groups))
        fallback_groups = list(dict.fromkeys(fallback_groups))

        # Ignore sources where the main abuse group is different from the currently processed one.
        if main_group not in groups:
            return [], [], fltlog

        filtered_groups, fltlog = self._filter_groups(groups, event, fltlog)

        # If any filtering rule of at least one of the groups was matched then this event shall not be reported to anyone.
        if filtered_groups != groups:
            self.logger.debug("Discarding event with ID '%s' from reports.", event['ID'])
            return [], [], fltlog

        fallback_groups, fltlog = self._filter_groups(fallback_groups, event, fltlog)
        return filtered_groups, fallback_groups, fltlog

    def filter_events_by_credibility(self, events_aggr):
        """
        Filter given dictionary of IDEA events aggregated by the source IP address by detector credibility.
        If the resulting credibility is less than 0.5, the event is discarded from the report.

        :param dict events_aggt: Dictionary of IDEA events as :py:class:`mentat.idea.internal.Idea` objects.
        :return: Tuple with filtered dictionary, number of events passed, number of events discarded.
        :rtype: tuple
        """
        blocked = set()
        _events_aggr = {}
        for ip in events_aggr:
            for event in events_aggr[ip]:
                _pass = 1.0
                for detector in event.get_detectors():
                    if detector not in self.detectors_dict:
                        self.logger.info("Event with ID '%s' contains unknown detector '%s'. Assuming full credibility.", event.get_id(), detector)
                        continue
                    _pass *= self.detectors_dict[detector].credibility
                if _pass < 0.5:
                    if event.get_id() in blocked:
                        continue
                    self.logger.info("Discarding event with ID '%s'.", event.get_id())
                    blocked.add(event.get_id())
                    # Increase number of hits.
                    sql_detector = self.detectors_dict[event.get_detectors()[-1]]
                    sql_detector.hits += 1
                    # Inefficient but rare so should be alright.
                    self.sqlservice.session.add(sql_detector)
                    self.sqlservice.session.commit()
                else:
                    if ip not in _events_aggr:
                        _events_aggr[ip] = []
                    _events_aggr[ip].append(event)
        return _events_aggr, len(blocked)

    def filter_events(self, main_group, events):
        """
        Filter given list of IDEA events according to given abuse group settings.
        Events are aggregated by resolved abuses and source IP addresses.

        :param str main_group: Abuse group.
        :param list events: List of IDEA events as :py:class:`mentat.idea.internal.Idea` objects.
        :return: Tuple with list of events that passed filtering, aggregation of them, filtering log as a dictionary and number of passed events.
        :rtype: tuple
        """
        result = {}
        aggregated_result = {}
        fltlog = {}
        filtered_cnt = 0
        seen = {}

        for event in events:
            acc = []
            passed = False
            if len(jpath_values(event, 'Source.IP4') + jpath_values(event, 'Source.IP6')) > 1:
                event_copy = deepcopy(event)
                for source in event_copy["Source"]:
                    source["IP4"] = []
                    source["IP6"] = []
                for src in set(jpath_values(event, 'Source.IP4')):
                    event_copy["Source"][0]["IP4"] = [src]
                    filtered_groups, fallback_groups, fltlog = self.filter_one_event(src, event_copy, main_group, fltlog)
                    acc.append((src, filtered_groups, fallback_groups))
                event_copy["Source"][0]["IP4"] = []
                for src in set(jpath_values(event, 'Source.IP6')):
                    event_copy["Source"][0]["IP6"] = [src]
                    filtered_groups, fallback_groups, fltlog = self.filter_one_event(src, event_copy, main_group, fltlog)
                    acc.append((src, filtered_groups, fallback_groups))
            else:
                for src in set(jpath_values(event, 'Source.IP4') + jpath_values(event, 'Source.IP6')):
                    filtered_groups, fallback_groups, fltlog = self.filter_one_event(src, event, main_group, fltlog)
                    acc.append((src, filtered_groups, fallback_groups))

            for src, filtered_groups, fallback_groups in acc:
                if not filtered_groups:
                    if not fallback_groups:
                        continue
                    filtered_groups = fallback_groups
                passed = True
                groups = (tuple(filtered_groups), tuple(fallback_groups))
                if groups not in result:
                    result[groups] = []
                    seen[groups] = []
                if groups not in aggregated_result:
                    aggregated_result[groups] = {}
                if str(src) not in aggregated_result[groups]:
                    aggregated_result[groups][str(src)] = []
                aggregated_result[groups][str(src)].append(event)
                if event['ID'] not in seen[groups]:
                    result[groups].append(event)
                    seen[groups].append(event['ID'])

            if passed:
                filtered_cnt += 1
            else:
                self.logger.debug("Event matched filtering rules, all sources filtered")

        return result, aggregated_result, fltlog, filtered_cnt

    @staticmethod
    def _whois_filter(sources, src, _whoismodule, whoismodule_cache):
        """
        Help method for filtering sources by abuse group's networks
        """
        if src not in whoismodule_cache:
            # Source IP must belong to network range of given abuse group.
            whoismodule_cache[src] = bool(_whoismodule.lookup(src))
        if whoismodule_cache[src]:
            sources.add(src)
        return sources

    def threshold_events(self, events_aggr, abuse_group, group_chain, severity, time_h):
        """
        Threshold given list of IDEA events according to given abuse group settings.

        :param dict events_aggr: Aggregation of IDEA events as :py:class:`mentat.idea.internal.Idea` objects by source.
        :param mentat.datatype.sqldb.GroupModel: Abuse group.
        :param str severity: Severity for which to perform reporting.
        :param datetime.datetime time_h: Upper reporting time threshold.
        :return: List of events that passed thresholding.
        :rtype: list
        """
        result = {}
        aggregated_result = {}
        filtered = set()
        for source, events in events_aggr.items():
            for event in events:
                if not self.tcache.event_is_thresholded(event, source, time_h):
                    if source not in aggregated_result:
                        aggregated_result[source] = []
                    aggregated_result[source].append(event)
                    result[event["ID"]] = event
                else:
                    filtered.add(event["ID"])
                    self.tcache.threshold_event(event, source, abuse_group.name, severity, time_h)

        filtered -= set(result.keys())
        if result:
            self.logger.info(
                "%s: Thresholds let %d events through, %d blocked.",
                group_chain,
                len(result),
                len(filtered)
            )
        else:
            self.logger.info(
                "%s: Thresholds blocked all %d events, nothing to report.",
                group_chain,
                len(filtered)
            )
        return list(result.values()), aggregated_result

    def relapse_events(self, abuse_group, severity, time_h):
        """
        Detect IDEA event relapses for given abuse group settings.

        :param mentat.datatype.sqldb.GroupModel abuse_group: Abuse group.
        :param str severity: Severity for which to perform reporting.
        :param datetime.datetime time_h: Upper reporting time threshold.
        :return: List of events that relapsed.
        :rtype: list
        """
        events = self.eventservice.search_relapsed_events(
            abuse_group.name,
            severity,
            time_h
        )
        if not events:
            self.logger.debug(
                "%s: No relapsed events with severity '%s' and relapse threshold TTL '%s'.",
                abuse_group.name,
                severity,
                time_h.isoformat()
            )
        else:
            self.logger.info(
                "%s: Found %d relapsed event(s) with severity '%s' and relapse threshold TTL '%s'.",
                abuse_group.name,
                len(events),
                severity,
                time_h.isoformat()
            )
        return events

    def aggregate_relapsed_events(self, relapsed):
        """
        :param dict events: Dictionary of events aggregated by threshold key.
        :return: Events aggregated by source.
        :rtype: dict
        """
        result = []
        aggregated_result = {}
        for event in relapsed:
            result.append(record_to_idea(event))
            for key in event.keyids:
                source = self.tcache.get_source_from_cache_key(key)
                if source not in aggregated_result:
                    aggregated_result[source] = []
                aggregated_result[source].append(result[-1])
        return result, aggregated_result

    def update_thresholding_cache(self, events, settings, severity, time_h):
        """
        :param dict events: Dictionary structure with IDEA events that were reported.
        :param mentat.reports.event.ReportingSettings settings: Reporting settings.
        :param str severity: Severity for which to perform reporting.
        :param datetime.datetime time_h: Upper reporting time threshold.
        """
        ttl = time_h + settings.timing_cfg[severity]['thr']
        rel = ttl - settings.timing_cfg[severity]['rel']
        for source in events.get('regular_aggr', {}):
            for event in events['regular_aggr'][source]:
                self.tcache.set_threshold(event, source, time_h, rel, ttl, self.message_id_dict.get(source, None))
        for source in events.get('relapsed_aggr', {}):
            for event in events['relapsed_aggr'][source]:
                self.tcache.set_threshold(event, source, time_h, rel, ttl, self.message_id_dict.get(source, None))

    #---------------------------------------------------------------------------

    def filter_event(self, filter_rules, event, to_db=True):
        """
        Filter given event according to given list of filtering rules.

        :param list filter_rules: Filters to be used.
        :param mentat.idea.internal.Idea: Event to be filtered.
        :param bool to_db: Save hit to db.
        :return: ``True`` in case any filter matched, ``False`` otherwise.
        :rtype: bool
        """
        for flt in filter_rules:
            if self.filter_worker.filter(flt[1], event):
                if to_db:
                    flt[0].hits += 1
                    flt[0].last_hit = datetime.datetime.utcnow()
                return flt[0].name
        return False

    @staticmethod
    def _get_relevant_source_sections(event, ip):
        """
        Helper method for aggregate_events.
        Returns all source sections of the event, where the ip
        from args is included.
        """
        sections = []
        for section in event.get("Source", []):
            if (str(ip) in list(map(str, section.get("IP4", [])))
                or str(ip) in list(map(str, section.get("IP6", [])))):
                sections.append(section)
        return sections

    @staticmethod
    def _initialize_result(result, event_class, ip, detector):
        """
        Helper method for aggregate_events.
        Initializes the detector result structure based on fields that
        are enumerated in mentat.const and should be aggregated.
        """
        ip_result = (result.setdefault(event_class, {})
            .setdefault(str(ip), {
                "first_time": datetime.datetime.max,
                "last_time": datetime.datetime.min,
                "detectors_count": {},
                "count": 0,
                "detector_data": {}
            })
        )
        detector_result = ip_result.get("detector_data").get(detector, None)
        if detector_result is None:
            detector_result = ip_result.get("detector_data").setdefault(detector, {
                "Source": {},
                "Target": {}
            })
            for field, _ in mentat.const.REPORT_FIELDS_MAIN_NUMBER:
                detector_result[field] = 0
            for field, _ in mentat.const.REPORT_FIELDS_MAIN_LIST:
                detector_result[field] = {}

            for field, _ in mentat.const.REPORT_FIELDS_SOURCE_NUMBER:
                detector_result["Source"][field] = 0
            for field, _ in mentat.const.REPORT_FIELDS_TARGET_NUMBER:
                detector_result["Target"][field] = 0
            for field, _ in mentat.const.REPORT_FIELDS_SOURCE_LIST:
                detector_result["Source"][field] = {}
            for field, _ in mentat.const.REPORT_FIELDS_TARGET_LIST:
                detector_result["Target"][field] = {}
        return (ip_result, detector_result)

    @staticmethod
    def _process_aggregated_results(result):
        """
        Helper method that does the final processing of the aggregated results.
        """
        for abuse_value in result.values():
            for ip_value in abuse_value.values():
                ip_value["detectors_count"] = len(ip_value["detectors_count"])
                ip_value["first_time"] = ip_value["first_time"].isoformat()
                ip_value["last_time"] = ip_value["last_time"].isoformat()
                for detector_value in ip_value.get("detector_data").values():
                    if detector_value.get("AvgPacketSize"):
                        detector_value["AvgPacketSize"] = round(
                            detector_value["AvgPacketSize"] / detector_value["PacketCount"])
                    for field, _ in mentat.const.REPORT_FIELDS_MAIN_LIST:
                        detector_value[field] = list(detector_value[field].keys())

                    for field, _ in mentat.const.REPORT_FIELDS_SOURCE_LIST:
                        detector_value["Source"][field] = sorted(detector_value["Source"][field].keys())
                    for field, _ in mentat.const.REPORT_FIELDS_TARGET_LIST:
                        detector_value["Target"][field] = sorted(detector_value["Target"][field].keys())
        return result

    @staticmethod
    def aggregate_events(events):
        """
        Aggregate given list of events to dictionary structure that can be used to generate report message.
        In "Source", only data from source sections that include the particular IP address are aggregated.

        :param dict events: Structure containing events as :py:class:`mentat.idea.internal.Idea` objects.
        :return: Dictionary structure of aggregated events.
        :rtype: dict
        """
        result = {}
        for ip in events.keys():
            for event in events[ip]:
                idea_event = mentat.idea.internal.Idea(event)
                event_class = idea_event.get_whole_class() or 'None'
                idea_detector = event.get("Node", [{}])[-1].get("Name")
                detector = str(idea_detector or '__UNKNOWN__')
                source_sections = EventReporter._get_relevant_source_sections(event, ip)

                ip_result, detector_result = EventReporter._initialize_result(result, event_class, ip, detector)

                ## Basic event data aggregation.
                ip_result["first_time"] = min(event.get("EventTime") or event["DetectTime"], ip_result["first_time"])
                ip_result["last_time"] = max(event.get("CeaseTime") or event.get("EventTime") or event["DetectTime"], ip_result["last_time"])
                ip_result["count"] += 1
                # Name of the last node to uniquely identify detectors.
                ip_result["detectors_count"][event.get("Node", [{}])[-1].get("Name")] = 1

                ## Aggregations from the main section.
                for field, _ in mentat.const.REPORT_FIELDS_MAIN_NUMBER:
                    if field == "AvgPacketSize":
                        # Sums packet size of all packets. Average is counted only after all events are aggregated.
                        if event.get("AvgPacketSize") and event.get("PacketCount"):
                            detector_result["AvgPacketSize"] = event.get("AvgPacketSize") * event.get("PacketCount")
                    else:
                        detector_result[field] += event.get(field, 0)
                for field, _ in mentat.const.REPORT_FIELDS_MAIN_LIST:
                    for value in jpath_values(event, field):
                        detector_result[field][value] = 1

                ## Aggregations from Source and Target sections.
                for (typ, fields) in [("Source", mentat.const.REPORT_FIELDS_SOURCE_NUMBER),
                                          ("Target", mentat.const.REPORT_FIELDS_TARGET_NUMBER)]:
                    for (field, _) in fields:
                        # Some detectors incorrectly use "In/OutPacketsCount" instead of "In/OutPacketCount".
                        event_fields = [field]
                        if field == "InPacketCount":
                            event_fields.append("InPacketsCount")
                        elif field == "OutPacketCount":
                            event_fields.append("OutPacketsCount")
                        for event_field in event_fields:
                            if typ == "Target":
                                for value in jpath_values(event, "Target." + event_field):
                                    detector_result[typ][field] += value
                            else:
                                for section in source_sections:
                                    detector_result[typ][field] += section.get(event_field, 0)

                for field, _ in mentat.const.REPORT_FIELDS_SOURCE_LIST:
                    for section in source_sections:
                        if field == "services":  # Aggregated as a tuple (ServiceName, ServiceVersion)
                            if section.get("ServiceName"):
                                detector_result["Source"]["services"][(section.get("ServiceName"), section.get("ServiceVersion"))] = 1
                        else:
                            for value in section.get(field, []):
                                detector_result["Source"][field][str(value)] = 1

                for field, _ in mentat.const.REPORT_FIELDS_TARGET_LIST:
                    if field == "ips":
                        for value in jpath_values(event, "Target.IP4") + jpath_values(event, "Target.IP6"):
                            detector_result["Target"][field][str(value)] = 1
                    elif field == "services":
                        for section in event.get("Target", []):
                            if section.get("ServiceName"):
                                detector_result["Target"]["services"][(section.get("ServiceName"), section.get("ServiceVersion"))] = 1
                    else:
                        for value in jpath_values(event, "Target." + field):
                            detector_result["Target"][field][str(value)] = 1

        return EventReporter._process_aggregated_results(result)

    #---------------------------------------------------------------------------

    def _save_to_json_files(self, data, filename):
        """
        Helper method for saving given data into given JSON file. This method can
        be used for saving report data attachments to disk.

        :param dict data: Data to be serialized.
        :param str filename: Name of the target JSON file.
        :return: Paths to the created files.
        :rtype: tuple
        """
        dirpath = mentat.const.construct_report_dirpath(self.reports_dir, filename)
        filepath = os.path.join(dirpath, filename)

        while True:
            try:
                with open(filepath, 'w', encoding="utf8") as jsonf:
                    json.dump(
                        data,
                        jsonf,
                        default = mentat.idea.internal.Idea.json_default,
                        sort_keys = True,
                        indent = 4
                    )
                break
            except FileNotFoundError:
                os.makedirs(dirpath)

        zipfilepath = "{}.zip".format(filepath)
        with zipfile.ZipFile(zipfilepath, mode = 'w') as zipf:
            zipf.write(filepath, compress_type = zipfile.ZIP_DEFLATED)

        return filepath, zipfilepath

    def _save_to_files(self, data, filename):
        """
        Helper method for saving given data into given file. This method can be
        used for saving copies of report messages to disk.

        :param dict data: Data to be serialized.
        :param str filename: Name of the target file.
        :return: Path to the created file.
        :rtype: str
        """
        dirpath = mentat.const.construct_report_dirpath(self.reports_dir, filename)
        filepath = os.path.join(dirpath, filename)

        while True:
            try:
                with open(filepath, 'w', encoding="utf8") as imf:
                    imf.write(data)
                break
            except FileNotFoundError:
                os.makedirs(dirpath)

        zipfilepath = "{}.zip".format(filepath)
        with zipfile.ZipFile(zipfilepath, mode = 'w') as zipf:
            zipf.write(filepath, compress_type = zipfile.ZIP_DEFLATED)

        return filepath, zipfilepath

    def get_event_class(self, name):
        """
        Returns object of an event class with the name from input.
        """
        # Get event class name from whole class. (whole class = event_class/subclass)
        if '/' in name:
            name = name.split('/')[0]
        return self.sqlservice.session.query(EventClassModel) \
            .filter(EventClassModel.name == name) \
            .one_or_none()

    def render_report(self, report, settings, template_vars=None, srcip=None):
        # Render report section.
        template = self.renderer.get_template(
            '{}.{}_v2.txt.j2'.format(settings.template, report.type)
        )

        # Force locale to given value.
        self.set_locale(settings.locale)

        # Force timezone to given value.
        self.set_timezone(settings.timezone)

        return template.render(
            dt_c=datetime.datetime.utcnow(),
            report=report,
            source=srcip,

            settings=settings,
            text_width=REPORT_EMAIL_TEXT_WIDTH,
            additional_vars=template_vars,
            get_event_class=self.get_event_class,
            fields={
                "MAIN_NUMBER": mentat.const.REPORT_FIELDS_MAIN_NUMBER,
                "MAIN_LIST": mentat.const.REPORT_FIELDS_MAIN_LIST_VIEW,
                "SOURCE_NUMBER": mentat.const.REPORT_FIELDS_SOURCE_NUMBER,
                "TARGET_NUMBER": mentat.const.REPORT_FIELDS_TARGET_NUMBER,
                "SOURCE_LIST": mentat.const.REPORT_FIELDS_SOURCE_LIST,
                "TARGET_LIST": mentat.const.REPORT_FIELDS_TARGET_LIST
            }
        )

    def _get_recipients(self, groups, severity):
        severities = ['low', 'medium', 'high', 'critical']
        to = []
        cc = []
        for group in groups:
            i = severities.index(severity)
            while i >= 0:
                if self.settings_dict[group].emails[i]:
                    if not to:
                        to = self.settings_dict[group].emails[i]
                    else:
                        for email in self.settings_dict[group].emails[i]:
                            if email not in to and email not in cc:
                                cc.append(email)
                i -= 1

        return to, cc

    def _mail_report(self, report, settings, groups, fallback_groups, result, template_vars, srcip=None):
        """
        Construct email report object and send it.
        """

        def get_message_id(label):
            return f'<{label}@{socket.getfqdn()}>'

        def get_relapsed_event_classes(data):
            if 'relapsed' in data:
                return data['relapsed'].keys()
            return []

        to, cc = self._get_recipients(groups, report.severity)

        # Use fallback option if no email addresses are found for the given severity.
        if not to:
            to, cc = self._get_recipients(fallback_groups, report.severity)
            to = to if to else self.global_fallback
            self.logger.info("No email addresses found for the given severity, using fallback: %s", to)

        # Set custom message id, which can be referenced later.
        message_id = get_message_id(report.label)

        # Common report email headers.
        report_msg_headers = {
            'to': to,
            'cc': cc,
            'report_id': report.label,
            'report_type': report.type,
            'report_severity': report.severity,
            'report_evcount': report.evcount_rep,
            'report_window': '{}___{}'.format(report.dt_from.isoformat(), report.dt_to.isoformat()),
            'report_testdata': report.flag_testdata,
            'message_id': message_id
        }

        message = self.render_report(report, settings, template_vars, srcip)

        # Report email headers specific for 'summary' reports.
        if report.type == mentat.const.REPORTING_MODE_SUMMARY:
            report_msg_headers['subject'] = self.translator.gettext(REPORT_SUBJECT_SUMMARY).format(
                report.label,
                self.translator.gettext(report.severity).title()
            )
        # Report email headers specific for 'extra' reports.
        else:
            report_msg_headers['subject'] = self.translator.gettext(REPORT_SUBJECT_EXTRA).format(
                report.label,
                self.translator.gettext(report.severity).title(),
                srcip
            )
            report_msg_headers['report_id_par'] = report.parent.label
            report_msg_headers['report_srcip']  = srcip
            event_classes = get_relapsed_event_classes(report.structured_data)
            for event_class in event_classes:
                key = str(event_class + '+++' + srcip)
                if key in self.message_id_dict['thresholds']:
                    reference_report = self.message_id_dict['thresholds'][key]
                    # Save the report reference so it can be viewed later in GUI.
                    report.structured_data['relapsed'][event_class][srcip]['reference'] = reference_report
                    if 'references' not in report_msg_headers:
                        report_msg_headers['references'] = []
                    # Add the report reference to references headers.
                    report_msg_headers['references'].append(get_message_id(reference_report))

            # Set flag so sqlalchemy knows to update this object.
            if 'references' in report_msg_headers:
                flag_modified(report, 'structured_data')

        report_msg_params = {
            'text_plain': message,
            'attachments': []
        }
        report_msg = self.mailer.email_send(
            ReportEmail,
            report_msg_headers,
            report_msg_params,
            settings.redirect
        )
        report.flag_mailed = True
        report.mail_to     = list(map(lambda x: 'to:' + str(x), to)) + list(map(lambda x: 'cc:' + str(x), cc))
        report.mail_dt     = datetime.datetime.utcnow()
        result['mail_to']  = list(
            set(
                result.get('mail_to', []) + report_msg.get_destinations()
            )
        )
