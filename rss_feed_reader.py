#!/usr/bin/env python3

import datetime
import logging
import re

import feedparser

RSS_FEED_URL = 'https://www.jenkins.io/security/advisories/rss.xml'
HowDeepItemsLookBack = 1
DATE_FORMAT_STR = '%a, %d %b %Y %I:%M:%S %z'
SENSITIVE_PLUGINS = ['saml', 'kubernetes']

loggeg = logging.getLogger(__name__)
FORMAT_INFO = '%(asctime)s - %(levelname)s - %(message)s'
logging.basicConfig(format=FORMAT_INFO, level=logging.INFO)

def calculate_boundaries_of_interest(days_delta=7):
  now = datetime.datetime.today()


