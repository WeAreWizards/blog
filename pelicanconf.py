#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

AUTHOR = u'We Are Wizards'
SITENAME = u'We Are Wizards Blog'
SITEURL = 'http://localhost:8000'

PATH = 'content/'
THEME = "hogwarts"

TIMEZONE = 'Europe/London'

DEFAULT_LANG = u'en'

# Feed generation is usually not desired when developing
FEED_ALL_ATOM = None
CATEGORY_FEED_ATOM = None
AUTHOR_FEED_ATOM = None
AUTHOR_FEED_RSS = None
TRANSLATION_FEED_ATOM = None

AUTHOR_URL = ''
AUTHOR_SAVE_AS = ''

DEFAULT_PAGINATION = False

# Uncomment following line if you want document-relative URLs when developing
#RELATIVE_URLS = True

PLUGIN_PATHS = ['plugins']
PLUGINS = [
    'gzip_cache',
    'feed_summary',
    'sitemap',
    'share_post',
    'summary',
    'liquid_tags.notebook',
]

SITEMAP = {
    'format': 'xml',
    'priorities': {
        'articles': 0.5,
        'indexes': 0.5,
        'pages': 0.5
    },
    'changefreqs': {
        'articles': 'monthly',
        'indexes': 'daily',
        'pages': 'monthly'
    }
}

STATIC_PATHS = ['images', 'extra/robots.txt', 'extra/favicon.ico']
EXTRA_PATH_METADATA = {
    'extra/robots.txt': {'path': 'robots.txt'},
    'extra/favicon.ico': {'path': 'favicon.ico'},
}

AUTHORS_INFO = {
    'tom': {
        'pic': 'https://wearewizards.io/img/team/tom.jpg',
        'name': 'Tom Hunger',
        'github': 'https://github.com/teh',
        'linkedin': 'https://www.linkedin.com/pub/thomas-h/a4/518/497'
    },
    'gautier': {
        'pic': 'https://wearewizards.io/img/team/gautier.jpg',
        'name': 'Gautier Hayoun',
        'github': 'https://github.com/Gautier',
        'linkedin': 'https://www.linkedin.com/in/gowtier'
    },
    'vincent': {
        'pic': 'https://wearewizards.io/img/team/vincent.jpg',
        'name': 'Vincent Prouillet',
        'github': 'https://github.com/Keats',
        'linkedin': 'https://www.linkedin.com/in/vincentprouillet'
    },
}
