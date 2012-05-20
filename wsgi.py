#!/usr/bin/env python

import os, os.path
import sys

os.environ['DJANGO_SETTINGS_MODULE'] = 'mancunia.settings'
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()
