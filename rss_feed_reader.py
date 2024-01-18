#!/usr/bin/env python3

import datetime
import logging
import re
import sys

import feedparser


RSS_FEED_URL = 'https://www.jenkins.io/security/advisories/rss.xml'
HOW_DEEP_ITEMS_LOOK_BACK = 1
DATE_FORMAT_STR = '%a, %d %b %Y %I:%M:%S %z'
SENSITIVE_PLUGINS = ['saml', 'kubernetes', 'HTMLResource', 'Nexus Platform']
REGEXP_PATTERNS = [
    r'<li>',
    r'<\/li>',
    r'<ul>',
    r'<\/ul>',
    r'<\/a>',
    r'Affects plugin: ',
    r'<a.*>']

logger = logging.getLogger(__name__)
FORMAT_INFO = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT_INFO, level=logging.INFO)


def check_python_release():
    python_major_version_tested = 3
    python_minor_version_tested = 10
    stable_runtime_verions = ".".join(
        [str(python_major_version_tested), str(python_minor_version_tested)]
        )

    is_runtime_major_ok = True if sys.version_info[0] == python_major_version_tested else False
    is_runtime_minor_ok = True if sys.version_info[1] < python_minor_version_tested else False

    if (is_runtime_major_ok) and (is_runtime_minor_ok):
        logger.warning('Mismatch runtime versions')
        logger.info(f'The stable runtime verision is: {stable_runtime_verions}')
        logger.info(f'The Python3 runtime is {sys.version_info[0]}.{sys.version_info[1]}')


def calculate_boundaries_of_interest(days_delta=7):
    now = datetime.datetime.today()
    till_date = now.strftime('%Y-%m-%d')
    from_date = (now - datetime.timedelta(days=days_delta)).strftime('%Y-%m-%d')
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

    try:
        news_feed.status
    except Exception:
        custom_exception()

    if news_feed.status != 200:
        custom_exception

    plugins = []
    if news_feed_counter > HOW_DEEP_ITEMS_LOOK_BACK:
        for idx in range(0, HOW_DEEP_ITEMS_LOOK_BACK):

            news_udated_when_raw = news_feed.entries[idx].updated
            news_udated_when = datetime.datetime.strptime(
                    news_udated_when_raw,
                    DATE_FORMAT_STR
            ).strftime('%Y-%m-%d')

            if from_date < news_udated_when < till_date:
                affected_plugins = news_feed.entries[idx].summary
                for REGEXP_PATTERN in REGEXP_PATTERNS:
                    affected_plugins = re.sub(
                        REGEXP_PATTERN,
                        '',
                        affected_plugins)

                for affected_plugin in affected_plugins.splitlines():
                    if affected_plugin:
                        plugins.append(affected_plugin)

        logger.info('A list of all affected plugins has been collected')
        logger.info(plugins)

        return (plugins)
    return (None)


def validate_affected_plugins(SENSITIVE_PLUGINS, affected_plugins) -> list:
    detected_plugins = [affected_plugin for affected_plugin
                        in SENSITIVE_PLUGINS
                        if affected_plugin in affected_plugins]

    return (detected_plugins)


def main():
    days = 91
    affected_plugins = None
    check_python_release()

    actual_affected_plugins = get_latest_feed(days=days)
    if actual_affected_plugins:
        logger.info('Cheking whether plugins are affected')
        affected_plugins = validate_affected_plugins(SENSITIVE_PLUGINS, actual_affected_plugins)

    if affected_plugins:
        logger.info('[ALARM] One or more plugin(-s) is affeted')
        logger.info(f'The list of affected plugin(-s): {affected_plugins}')
    else:
        logger.info(f'For the {days} day(-s) no any sensitive affected plugin(-s) found')


if __name__ == "__main__":
    logger.info('Script started')
    main()
    logger.info('Script completed')
