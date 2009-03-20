# -*- coding: utf-8 -*-

from local_settings import *
DEBUG = True
TEMPLATE_DEBUG = DEBUG
AUTH_PROFILE_MODULE = "profiles.UserProfile"
DEFAULT_CHARSET = 'utf-8'
MANAGERS = ADMINS
DATABASE_ENGINE = 'postgresql_psycopg2'     
SEARCH_ENGINE = 'postgresql' 
ACCOUNT_ACTIVATION_DAYS = 7
SITE_ID = 1
USE_I18N = True
ADMIN_MEDIA_PREFIX = '/adminmedia/'
TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.load_template_source',
    'django.template.loaders.app_directories.load_template_source',
)
MIDDLEWARE_CLASSES = (
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
)
MEDIA_ROOT = SITE_ROOT+'/media/'
TEMPLATE_DIRS = (
SITE_ROOT+"/templates",
)
ROOT_URLCONF = 'urls'
INSTALLED_APPS = (
    'django_evolution',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.admin',
    'django.contrib.admindocs',
    'albastryde.wiki',
    'albastryde.precios',
    'albastryde.graph',
    'albastryde.valuta',
    'django.contrib.gis',
    'albastryde.mapa',
    'albastryde.lugar',
    'albastryde.climate',
    'albastryde.cosecha',
    'albastryde.lluvia',
    'django.contrib.comments',
    'albastryde.ajax_comments',
    'albastryde.registration',
    'albastryde.profiles',
)
