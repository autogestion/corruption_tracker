"""
Django settings for corruption_tracker project.
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
from django.utils.translation import ugettext_lazy as _

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


# Application definition

INSTALLED_APPS = (
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    'django.contrib.sites',
    'django.contrib.gis',

    # 'debug_toolbar',

    # 'allauth',
    # 'allauth.account',
    # 'allauth.socialaccount',
    # 'allauth.socialaccount.providers.facebook',
    'oauth2_provider',
    'rest_framework',
    # 'rest_framework.authtoken',
    'rest_framework_swagger',
    'leaflet',

    'corruption_tracker',
    'claim',
    'geoinfo',
    'api',
)

MIDDLEWARE_CLASSES = (
    'corruption_tracker.middleware.SqlProfilingMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    # 'oauth2_provider.middleware.OAuth2TokenMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.security.SecurityMiddleware',
    
)

AUTHENTICATION_BACKENDS = (
    # 'oauth2_provider.backends.OAuth2Backend',
    'django.contrib.auth.backends.ModelBackend',
    # 'allauth.account.auth_backends.AuthenticationBackend'
)


ROOT_URLCONF = 'corruption_tracker.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'corruption_tracker.wsgi.application'

# Internationalization
LANGUAGE_CODE = 'en-us'
LANGUAGES = (
    ('uk', _('Ukrainian')),
    ('en', _('English')),
    # ('ru', _('Russian')),
)
LOCALE_PATHS = [os.path.join(BASE_DIR, 'locale')]

TIME_ZONE = 'UTC'
USE_I18N = True
USE_L10N = True
USE_TZ = True

# Static files (CSS, JavaScript, Images)
STATIC_URL = '/static/'
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, "static"),
)
MEDIA_URL = '/media/'


SITE_ID = 1
LOGIN_REDIRECT_URL = '/'

# SOCIALACCOUNT_PROVIDERS = {
#     'facebook': {
#         'SCOPE': ['email', 'publish_stream'],
#         'METHOD': 'js_sdk'  # instead of 'oauth2'
#     }
# }


# Could be switched to another folder with geojsons
INIT_GEOJSON_FOLDER = os.path.join(BASE_DIR, 'init_geo_data')

LEAFLET_CONFIG = { 
    'RESET_VIEW': False,
	'PLUGINS': {
	'fontawesome': {
        'css': 'https://maxcdn.bootstrapcdn.com/font-awesome/4.4.0/css/font-awesome.min.css',
        'auto-include': True
    },	
    'geolocation': {
        'css': 'https://api.tiles.mapbox.com/mapbox.js/plugins/leaflet-locatecontrol/v0.43.0/L.Control.Locate.css',
        'js': 'https://api.tiles.mapbox.com/mapbox.js/plugins/leaflet-locatecontrol/v0.43.0/L.Control.Locate.min.js', 
        'auto-include': True
    }  
	},	
    'TILES': [('Hydda', 'http://{s}.tile.openstreetmap.se/hydda/full/{z}/{x}/{y}.png',
                            {'attribution':
                            'Tiles courtesy of <a href="http://openstreetmap.se/" '
                            'target="_blank">OpenStreetMap Sweden</a> &mdash; Map data &copy; '
                            '<a href="http://www.openstreetmap.org/copyright">OpenStreetMap</a>'
                            }),

              ('Streets', 'http://server.arcgisonline.com/ArcGIS/rest/'
                             'services/World_Street_Map/MapServer/tile/'
                             '{z}/{y}/{x}',
                             {'attribution':
                              'Tiles &copy; Esri &mdash; Source: Esri, '
                              'DeLorme, NAVTEQ, USGS, Intermap, iPC, '
                              'NRCAN, Esri Japan, METI, Esri China (Hong Kong)'
                              ', Esri (Thailand), TomTom, 2012'}),

              ('Satellite', 'http://server.arcgisonline.com/ArcGIS/rest/'
                               'services/World_Imagery/MapServer/tile/'
                               '{z}/{y}/{x}',
                               {'attribution':
                                'Tiles &copy; Esri &mdash; Source: Esri, '
                                'i-cubed, USDA, USGS, AEX, GeoEye, Getmapping,'
                                ' Aerogrid, IGN, IGP, UPR-EGP, and the GIS'
                                ' User Community'})]

}

GEOIP_PATH = os.path.join(BASE_DIR, 'geoinfo', 'geolite')



MEMCACHED_HOST = ('127.0.0.1', 11211)


REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'oauth2_provider.ext.rest_framework.OAuth2Authentication',
    ),
   'DEFAULT_PERMISSION_CLASSES': (
        'rest_framework.permissions.AllowAny',
    ),
   'PAGE_SIZE': 50,
   # 'URL_FORMAT_OVERRIDE': None,
}


try:
    from .local_settings import *
except ImportError as e:
    print(e)
