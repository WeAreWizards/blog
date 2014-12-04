#!/usr/bin/env python
# -*- coding: utf-8 -*- #
from __future__ import unicode_literals

# This file is only used if you use `make publish` or
# explicitly specify it as your config file.

import os
import sys
sys.path.append(os.curdir)
from pelicanconf import *

SITEURL = 'https://blog.wearewizards.io'
RELATIVE_URLS = False

FEED_ALL_ATOM = 'all.atom.xml'

DELETE_OUTPUT_DIRECTORY = True

# Following items are often useful when publishing

DISQUS_SITENAME = "wearewizards"
GOOGLE_ANALYTICS = "UA-57056653-2"

# Cleaner URLs:
ARTICLE_URL = '{slug}'
ARTICLE_SAVE_AS = '{slug}.html'
