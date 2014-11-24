#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'We Are Wizards'
SITENAME = u'We Are Wizards Blog'
SITEURL = 'blog.wearewizards.io'

PATH = 'content/'
THEME = "hogwarts"

TIMEZONE = 'Europe/London'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
TRANSLATION_FEED_ATOM = None

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

FILES_TO_COPY = (
    ('extra/robots.txt', 'robots.txt'),
    ('extra/favicon.ico', 'favicon.ico'),
)