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
    missed_env_vars = []
    try:
        how_deep_items_look_back = int(os.environ['HOW_DEEP_ITEMS_LOOK_BACK'])
    except Exception:
        missed_env_vars.append('HOW_DEEP_ITEMS_LOOK_BACK')

    try:
        looking_days = int(os.environ['LOOKING_DAYS'])
    except Exception:
        missed_env_vars.append('LOOKING_DAYS')

    try:
        sensitive_plugins = os.environ['SENSITIVE_PLUGINS'].split(';')
        sensitive_plugins = [x.lstrip(' ').rstrip(' ')
                             for x in sensitive_plugins]
    except Exception:
        missed_env_vars.append('SENSITIVE_PLUGINS')

    try:
        if_gha_execute = os.environ['GITHUB_ACTIONS']
        logger.disabled = True
    except Exception:
        if_gha_execute = False

    if len(missed_env_vars) != 0:
        results = (
            'One or more env variable missed. '
            'List of missed variable(-s): %s'
            % missed_env_vars
        )
        logger.error(results)
        sys.exit(1)

    return (
        how_deep_items_look_back,
        looking_days,
        sensitive_plugins,
        if_gha_execute
    )


def calculate_boundaries_of_interest(days_delta=7):
    now = datetime.datetime.today()
    till_date = now.strftime(SHORT_DATE_FORMAT)
    from_date = (now - datetime.timedelta(days=days_delta))
    from_date = from_date.strftime(SHORT_DATE_FORMAT)
    logger.info(
        'Specific date ranges calculated. From date:'
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


def get_latest_feed(days: int, how_deep_items_look_back: int):
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
    (how_deep_items_look_back,
     looking_days,
     sensitive_plugins,
     is_gha_execute) = read_envs()

    logger.info('Script started')

    days = looking_days
    actual_affected_plugins = None

    actual_affected_plugins = get_latest_feed(
        days=days,
        how_deep_items_look_back=how_deep_items_look_back
        )

    affected_plugins = []
    if actual_affected_plugins:
        results = 'Checking whether plugins are affected'
        logger.info(results)
        affected_plugins = validate_affected_plugins(
            sensitive_plugins, actual_affected_plugins
        )

    if affected_plugins:
        results = f'The list of affected plugin(-s): {affected_plugins}.'
        if is_gha_execute:
            print(results)
        else:
            logger.info(results)
    else:
        results = f'For the {days} day(-s) no any sensitive plugin(-s) found'
        logger.info(results)


if __name__ == '__main__':
    main()
