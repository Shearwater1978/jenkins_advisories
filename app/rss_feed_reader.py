#!/usr/bin/env python3

import datetime
import logging
import re
import sys
import os

import feedparser


RSS_FEED_URL = 'https://www.jenkins.io/security/advisories/rss.xml'
DATE_FORMAT_STR = '%a, %d %b %Y %I:%M:%S %z'
SHORT_DATE_FORMAT = '%Y-%m-%d'
REGEXP_PATTERNS = [
    r'<li>',
    r'<\/li>',
    r'<ul>',
    r'<\/ul>',
    r'<\/a>',
    r'Affects plugin: ',
    r'<a.*>',
]

logger = logging.getLogger(__name__)
FORMAT_INFO = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT_INFO, level=logging.INFO)


def read_envs():
    try:
        how_deep_items_look_back = int(os.environ['HOW_DEEP_ITEMS_LOOK_BACK'])
    except Exception as error:
        results = (
            'Env variable HOW_DEEP_ITEMS_LOOK_BACK is'
            'not exists. Script terminated.'
        )
        logger.error(results)
        raise SystemExit from error

    try:
        looking_days = int(os.environ['LOOKING_DAYS'])
    except Exception as error:
        results = 'Env variable LOOKING_DAYS is not exists. Script terminated.'
        logger.error(results)
        raise SystemExit from error

    try:
        sensitive_plugins = os.environ['SENSITIVE_PLUGINS'].split(';')
        sensitive_plugins = [x.lstrip(' ') for x in sensitive_plugins]
        sensitive_plugins = [x.rstrip(' ') for x in sensitive_plugins]
    except Exception as error:
        results = (
            'Env variable SENSITIVE_PLUGINS is not '
            'exists. Script terminated.'
        )
        logger.error(results)
        raise SystemExit from error

    return (how_deep_items_look_back, looking_days, sensitive_plugins)


def check_python_release():
    python_major_version = 3
    python_minor_version = 10
    stable_runtime_verions = '.'.join(
        [str(python_major_version), str(python_minor_version)]
    )

    if (sys.version_info[0] == python_major_version) and (
        sys.version_info[1] >= python_minor_version
    ):
        is_runtime_ok = True
    else:
        is_runtime_ok = False
    if not is_runtime_ok:
        logger.warning('Mismatch runtime versions')
        logger.warning(
            'The stable runtime verision is: %s'
            % stable_runtime_verions
        )
        logger.warning(
            'The Python3 runtime is %s.%s'
            % (sys.version_info[0], sys.version_info[1])
        )


def calculate_boundaries_of_interest(days_delta=7):
    now = datetime.datetime.today()
    till_date = now.strftime(SHORT_DATE_FORMAT)
    from_date = (now - datetime.timedelta(days=days_delta))
    from_date = from_date.strftime(SHORT_DATE_FORMAT)
    logger.info(
        'Specific date range calculated. From date:'
        '%s, till date: %s' % (from_date, till_date)
    )

    return (till_date, from_date)


def custom_exception():
    logger.error(
        'Something wrong wuth the RSS endpoint: %s'
        % RSS_FEED_URL
    )
    logger.error('Please check an access to the RSS endpoint and try again')
    logger.error('Script abnormal tetminated')
    raise SystemError


def get_latest_feed(days: int):
    till_date, from_date = calculate_boundaries_of_interest(days_delta=days)

    news_feed = feedparser.parse(RSS_FEED_URL)
    news_feed_counter = len(news_feed)
    affected_plugin = []

    try:
        news_feed.status
    except Exception as error:
        logger.error(error)
        custom_exception()

    if news_feed.status != 200:
        custom_exception()

    plugins = []
    if news_feed_counter > how_deep_items_look_back:
        for idx in range(0, how_deep_items_look_back):
            news_udated_when_raw = news_feed.entries[idx].updated
            news_udated_when = datetime.datetime.strptime(
                news_udated_when_raw, DATE_FORMAT_STR
            ).strftime(SHORT_DATE_FORMAT)

            if from_date <= news_udated_when <= till_date:
                results = 'from_date < news_udated_when < till_date'
                logger.debug(results)
                affected_plugins = news_feed.entries[idx].summary
                for regexp_pattern in REGEXP_PATTERNS:
                    affected_plugins = re.sub(
                        regexp_pattern, '', affected_plugins
                    )

                for affected_plugin in affected_plugins.splitlines():
                    if affected_plugin:
                        plugins.append(affected_plugin)

        results = 'A list of all affected plugins has been collected'
        logger.info(results)
    return plugins


def validate_affected_plugins(sensitive_plugins, affected_plugins) -> list:
    detected_plugins = [
        affected_plugin
        for affected_plugin in sensitive_plugins
        if affected_plugin in affected_plugins
    ]

    return detected_plugins


def main():
    check_python_release()

    days = looking_days
    affected_plugins = None
    actual_affected_plugins = get_latest_feed(days=days)
    if actual_affected_plugins:
        results = 'Checking whether plugins are affected'
        logger.info(results)
        affected_plugins = validate_affected_plugins(
            sensitive_plugins, actual_affected_plugins
        )

    if affected_plugins:
        results = (
            '[ALARM] One or more plugin(-s) is affeted'
            f'The list of affected plugin(-s): {affected_plugins}'
        )
        logger.info(results)
    else:
        results = f'For the {days} day(-s) no any sensitive plugin(-s) found'
        logger.info(results)


if __name__ == '__main__':
    how_deep_items_look_back, looking_days, sensitive_plugins = read_envs()
    logger.info('Script started')
    main()
    logger.info('Script completed')
