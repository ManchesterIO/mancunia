from oauth.oauth import OAuthSignatureMethod_PLAINTEXT
import os, os.path, imp
from molly.conf.settings import Application, extract_installed_apps, Authentication, ExtraBase, ProviderConf
from molly.utils.media import get_compress_groups
from molly.conf.celery_util import prepare_celery
from mancunia import local_secrets

BROKER_URL = "amqp://molly:molly@localhost:5672/molly"
CELERYBEAT_SCHEDULER = "djcelery.schedulers.DatabaseScheduler"
CELERYD_CONCURRENCY = 1
CELERY_RETRY_DELAY = 3 * 60
CELERY_MAX_RETRIES = 3

prepare_celery()

MOLLY_ROOT = imp.find_module('molly')[1]
PROJECT_ROOT = os.path.normpath(os.path.dirname(__file__))

DEBUG = True
DEBUG_SECURE = DEBUG
TEMPLATE_DEBUG = DEBUG

ADMINS = (
    ('Chris Northwood', 'chris@mancunia.mobi'),
)
MANAGERS = ADMINS

SITE_NAME = 'mancunia.mobi'

DATABASES = {
    'default': {
        'ENGINE': 'django.contrib.gis.db.backends.postgis',
        'NAME': 'molly',
        'USER': 'molly',
        'PASSWORD': '',
        'HOST': '',
        'PORT': '',
    }
}

SERVER_EMAIL = 'server@mancunia.mobi'
EMAIL_HOST = 'localhost'

TIME_ZONE = 'Europe/London'

LANGUAGE_CODE = 'en'
LANGUAGES = (
        ('en', 'English'),
    )
USE_I18N = True
USE_L10N = True

MEDIA_ROOT = os.path.join(PROJECT_ROOT, 'site_media')
MEDIA_URL = '/site-media/'
STATIC_ROOT = os.path.join(PROJECT_ROOT, 'compiled_media/')
STATIC_URL = '/static/'
ADMIN_MEDIA_PREFIX = STATIC_URL + 'admin/'
CACHE_DIR = os.path.join(PROJECT_ROOT, 'cache')
MARKER_DIR = os.path.join(CACHE_DIR, 'markers')

STATICFILES_DIRS = (
    ('', os.path.join(PROJECT_ROOT, 'site_media')),
    ('', os.path.join(MOLLY_ROOT, 'media')),
    ('markers', MARKER_DIR),
)

PIPELINE_VERSION = True
PIPELINE_AUTO = False
PIPELINE_CSS, PIPELINE_JS = get_compress_groups(STATIC_ROOT)
PIPELINE_CSS_COMPRESSOR = 'molly.utils.compress.MollyCSSFilter'
PIPELINE_JS_COMPRESSOR = 'pipeline.compressors.jsmin.JSMinCompressor'
PIPELINE = not DEBUG

SECRET_KEY = local_secrets.SECRET_KEY

TEMPLATE_LOADERS = (
    'django.template.loaders.filesystem.Loader',
    'django.template.loaders.app_directories.Loader',
    'molly.utils.template_loaders.MollyDefaultLoader'
)

TEMPLATE_DIRS = (
    os.path.join(PROJECT_ROOT, 'templates'),
    os.path.join(MOLLY_ROOT, 'templates'),
)

MIDDLEWARE_CLASSES = (
    'django.middleware.csrf.CsrfViewMiddleware',
    'molly.wurfl.middleware.WurflMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'molly.utils.middleware.ErrorHandlingMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'molly.url_shortener.middleware.URLShortenerMiddleware',
    'molly.utils.middleware.LocationMiddleware',
)

TEMPLATE_CONTEXT_PROCESSORS = (
    'django.contrib.auth.context_processors.auth',
    'django.core.context_processors.debug',
    'django.core.context_processors.request',
    'molly.utils.context_processors.ssl_media',
    'molly.wurfl.context_processors.wurfl_device',
    'molly.wurfl.context_processors.device_specific_media',
    'molly.geolocation.context_processors.geolocation',
    'molly.utils.context_processors.full_path',
    'molly.utils.context_processors.google_analytics',
    'molly.utils.context_processors.site_name',
    'molly.utils.context_processors.languages',
    'django.core.context_processors.csrf',
)
f
ROOT_URLCONF = 'molly.urls'

CSRF_FAILURE_VIEW = 'molly.utils.views.CSRFFailureView'

LOGGING = {
    'version': 1,
    'disable_existing_loggers': True,
    'root': {
        'level': 'WARNING',
        'handlers': ['sentry'],
    },
    'formatters': {
        'verbose': {
            'format': '%(levelname)s %(asctime)s %(module)s %(process)d %(thread)d %(message)s'
        },
    },
    'handlers': {
        'sentry': {
            'level': 'ERROR',
            'class': 'raven.contrib.django.handlers.SentryHandler',
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'verbose'
        }
    },
    'loggers': {
        'django.db.backends': {
            'level': 'ERROR',
            'handlers': ['console'],
            'propagate': False,
        },
        'raven': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
        'sentry.errors': {
            'level': 'DEBUG',
            'handlers': ['console'],
            'propagate': False,
        },
    },
}

API_KEYS = {
    'cloudmade': local_secrets.CLOUDMADE,
    'google_analytics': local_secrets.GOOGLE_ANALYTICS,
}

APPLICATIONS = [
    
    Application('molly.apps.home', 'home', 'Home',
        display_to_user = False,
    ),

    Application('molly.apps.places', 'places', 'Places',
        providers = [
            ProviderConf('molly.apps.places.providers.NaptanMapsProvider',
                areas=('180','920','930','940'),
            ),
            
            ProviderConf('molly.apps.places.providers.PostcodesMapsProvider',
                codepoint_path = CACHE_DIR + '/codepo_gb.zip',
                import_areas = ('M', 'SK', 'WA', 'WN', 'BL', 'OL'),
            ),
            
            ProviderConf('molly.apps.places.providers.OSMMapsProvider',
                     lat_north=53.685760, # The northern limit on the bounding box
                     lat_south=53.327332, # The southern limit on the bounding box
                     lon_west=-2.730550, # The western limit on the bounding box
                     lon_east=-1.909630 # The eastern limit on the bounding box
                     #osm_tags_data_file=os.path.join(PROJECT_ROOT, 'data', 'osm_tags.yaml'),
                     #entity_type_data_file=os.path.join(PROJECT_ROOT, 'data', 'osm_entity_types.yaml')
            ),
            
            ProviderConf('molly.apps.places.providers.LiveDepartureBoardPlacesProvider',
                token = local_secrets.LDB
            ),
            
            ProviderConf('molly.apps.places.providers.AtcoCifTimetableProvider',
                url = 'http://store.datagm.org.uk/sets/TfGM/GMPTE_CIF.zip'
            ),
            
            #ProviderConf('molly.apps.places.providers.cif.CifTimetableProvider',
            #    filename = '/home/chris/Downloads/ttf597/TTISF597.MCA'
            #),
            
            ProviderConf('molly.apps.places.providers.TimetableAnnotationProvider'),
        ]
    ),

    Application('molly.apps.transport', 'transport', 'Transport',
        train_station = 'crs:MAN',
        train_station_nearest = True,
        nearby = {
            'bus': ('bus-stop', 5),
            'metrolink': ('metrolink-station', 3),
        },
        #park_and_rides = [
        #    'osm:W4333225',
        #    'osm:W4329908',
        #    'osm:W34425625',
        #    'osm:W24719725',
        #    'osm:W2809915'],
        # No real-time data for P&R in Greater Manchester atm so this is
        # disabled. List of P&R here though: http://www.tfgm.com/journey_planning/park_and_ride.cfm?submenuheader=0
        travel_alerts = False,
    ),
    
    Application('molly.apps.podcasts', 'podcasts', 'Podcasts',
        providers = [
            ProviderConf('molly.apps.podcasts.providers.RSSPodcastsProvider',
                podcasts = [
                    ('bbcmancnews', 'http://downloads.bbc.co.uk/podcasts/manchester/mancnews/rss.xml'),
                    ('bbcmancsports', 'http://downloads.bbc.co.uk/podcasts/manchester/spotlight/rss.xml'),
                    ('bbcmancbus', 'http://downloads.bbc.co.uk/podcasts/manchester/mancbus/rss.xml'),
                    ('bbcmancrugby', 'http://downloads.bbc.co.uk/podcasts/manchester/extra/rss.xml'),
                ],
                medium = 'audio'
            ),
        ]
    ),
    Application('molly.apps.webcams', 'webcams', 'Webcams'),

    Application('molly.apps.weather', 'weather', 'Weather',
        location_id = 'bbc/9',
        provider = ProviderConf('molly.apps.weather.providers.BBCWeatherProvider',
            location_id = 9,
        ),
    ),

    Application('molly.apps.search', 'search', 'Search',
        providers = [
            ProviderConf('molly.apps.search.providers.ApplicationSearchProvider'),
        ],
        display_to_user = False,
    ),

    Application('molly.apps.feeds', 'feeds', 'Feeds',
        providers = [
            ProviderConf('molly.apps.feeds.providers.RSSFeedsProvider'),
        ],
        display_to_user = False,
    ),

    Application('molly.apps.feeds.news', 'news', 'News'),
    Application('molly.apps.feeds.events', 'events', 'Events'),

    Application('molly.maps', 'maps', 'Maps',
        display_to_user = False,
    ),

    Application('molly.geolocation', 'geolocation', 'Geolocation',
        prefer_results_near = (-2.248810, 53.479599, 25000),
        providers = [
            ProviderConf('molly.geolocation.providers.PlacesGeolocationProvider'),
            ProviderConf('molly.geolocation.providers.CloudmadeGeolocationProvider',
                search_locality = 'Greater Manchester',
            ),
        ],
        location_request_period = 600,
        display_to_user = False,
    ),
    
    Application('molly.apps.feedback', 'feedback', 'Feedback',
        display_to_user = False,
    ),

    Application('molly.external_media', 'external-media', 'External Media',
        display_to_user = False,
    ),

    Application('molly.wurfl', 'device-detection', 'Device detection',
        display_to_user = False,
        expose_view = True,
    ),

    Application('molly.url_shortener', 'url-shortener', 'URL Shortener',
        display_to_user = False,
    ),

    Application('molly.utils', 'utils', 'Molly utility services',
        display_to_user = False,
    ),

    Application('molly.apps.feature_vote', 'feature-suggestions', 'Feature suggestions',
        display_to_user = False,
    ),
    
    Application('molly.favourites', 'favourites', 'Favourite pages',
        display_to_user = False,
    ),
    
    Application('molly.routing', 'routing', 'Routing',
        display_to_user = False,
    ),
    
    Application('molly.routing', 'routing', 'Routing',
        display_to_user = False,
    ),

]

# This is where any non-Molly apps are added to the configuration
INSTALLED_APPS = extract_installed_apps(APPLICATIONS) + (
    'django.contrib.auth',
    'django.contrib.admin',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.gis',
    'django.contrib.comments',
    'django.contrib.staticfiles',
    'pipeline',
    'south',
    'djcelery',
)

SENTRY_DSN = local_secrets.SENTRY

try:
    from mancunia.settings_local import *
except:
    pass
