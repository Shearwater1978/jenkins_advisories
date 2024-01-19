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
    r'<a.*>'
  ]

logger = logging.getLogger(__name__)
FORMAT_INFO = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT_INFO, level=logging.INFO)


def read_envs():
    try:
        HOW_DEEP_ITEMS_LOOK_BACK = int(os.environ['HOW_DEEP_ITEMS_LOOK_BACK'])
    except Exception as e:
        results = 'Env variable HOW_DEEP_ITEMS_LOOK_BACK is not exists. Script terminated.'
        logger.error(results)
        raise SystemExit from e

    try:
        LOOKING_DAYS = int(os.environ['LOOKING_DAYS'])
    except Exception as e:
        results = 'Env variable LOOKING_DAYS is not exists. Script terminated.'
        logger.error(results)
        raise SystemExit from e

    try:
        SENSITIVE_PLUGINS = os.environ['SENSITIVE_PLUGINS'].split(";")
        SENSITIVE_PLUGINS = [x.lstrip(' ') for x in SENSITIVE_PLUGINS]
        SENSITIVE_PLUGINS = [x.rstrip(' ') for x in SENSITIVE_PLUGINS]
    except Exception as e:
        results = 'Env variable SENSITIVE_PLUGINS is not exists. Script terminated.'
        logger.error(results)
        raise SystemExit from e

    return (HOW_DEEP_ITEMS_LOOK_BACK, LOOKING_DAYS, SENSITIVE_PLUGINS)


def check_python_release():
    PYTHON_MAJOR_VERSION = 3
    PYTHON_MINOR_VERSION = 10
    stable_runtime_verions = ".".join(
        [
            str(PYTHON_MAJOR_VERSION), 
            str(PYTHON_MINOR_VERSION)
        ]
    )

    if (sys.version_info[0] == PYTHON_MAJOR_VERSION) and (sys.version_info[1] >= PYTHON_MINOR_VERSION):
        is_runtime_ok = True
    else:
        is_runtime_ok = False
    if not is_runtime_ok:
        logger.warning('Mismatch runtime versions')
        logger.warning(f'The stable runtime verision is: {stable_runtime_verions}')
        logger.warning(f'The Python3 runtime is {sys.version_info[0]}.{sys.version_info[1]}')


def calculate_boundaries_of_interest(days_delta=7):
    now = datetime.datetime.today()
    till_date = now.strftime(SHORT_DATE_FORMAT)
    from_date = (now - datetime.timedelta(days=days_delta)).strftime(SHORT_DATE_FORMAT)
    logger.info(f'Specific date range calculated. From date: {from_date}, till date: {till_date}')

    return (till_date, from_date)


def custom_exception():
    logger.error(f'Something wrong wuth the RSS endpoint: {RSS_FEED_URL}')
    logger.error('Please check an access to the RSS endpoint and try again')
    logger.error('Script abnormal tetminated')
    raise SystemError


def get_latest_feed(days: int) -> list:
    till_date, from_date = calculate_boundaries_of_interest(days_delta=days)

    news_feed = feedparser.parse(RSS_FEED_URL)
    news_feed_counter = len(news_feed)
    affected_plugin = []

    try:
        news_feed.status
    except Exception:
        custom_exception()

    if news_feed.status != 200:
        custom_exception()

    plugins = []
    if news_feed_counter > HOW_DEEP_ITEMS_LOOK_BACK:
        for idx in range(0, HOW_DEEP_ITEMS_LOOK_BACK):

            news_udated_when_raw = news_feed.entries[idx].updated
            news_udated_when = datetime.datetime.strptime(
                    news_udated_when_raw,
                    DATE_FORMAT_STR
            ).strftime(SHORT_DATE_FORMAT)

            if from_date <= news_udated_when <= till_date:
                logger.debug('from_date < news_udated_when < till_date')
                affected_plugins = news_feed.entries[idx].summary
                for regexp_pattern in REGEXP_PATTERNS:
                    affected_plugins = re.sub(
                        regexp_pattern,
                        '',
                        affected_plugins)

                for affected_plugin in affected_plugins.splitlines():
                    if affected_plugin:
                        plugins.append(affected_plugin)

        logger.info('A list of all affected plugins has been collected')
        return (plugins)


def validate_affected_plugins(sensitive_plugins, affected_plugins) -> list:
    detected_plugins = [affected_plugin for affected_plugin
                        in sensitive_plugins
                        if affected_plugin in affected_plugins]

    return (detected_plugins)


def main():
    check_python_release()

    days = LOOKING_DAYS
    affected_plugins = None
    actual_affected_plugins = get_latest_feed(days=days)
    if actual_affected_plugins:
        logger.info('Cheking whether plugins are affected')
        affected_plugins = validate_affected_plugins(SENSITIVE_PLUGINS, actual_affected_plugins)

    if affected_plugins:
        logger.info('[ALARM] One or more plugin(-s) is affeted')
        logger.info(f'The list of affected plugin(-s): {affected_plugins}')
    else:
        logger.info(f'For the {days} day(-s) no any sensitive plugin(-s) found')


if __name__ == "__main__":
    HOW_DEEP_ITEMS_LOOK_BACK, LOOKING_DAYS, SENSITIVE_PLUGINS = read_envs()
    logger.info('Script started')
    main()
    logger.info('Script completed')
