#!/usr/bin/evn python
import os, sys

#make sure app's modules can be found
sys.path.append('/home/mark')
sys.path.append('/home/mark/cssearchengine')
os.environ['DJANGO_SETTINGS_MODULE'] = 'settings'

os.chdir("/home/mark/cssearchengine")

import django.core.handlers.wsgi
application = django.core.handlers.wsgi.WSGIHandler()

