# -*- coding: utf-8 -*-
# Django settings for pycon project.
import os
import os.path
import sys

import dj_database_url
from decouple import config

from django.core.urlresolvers import reverse_lazy

from model_utils import Choices


# override ugettext
def _(x):
    return x


# Configure DEBUG settings
DEBUG = config('DEBUG', default=False, cast=bool)

# We want to use HTTPS for everything and not fiddle with docker or gunicorn
# setups.
#
# See http://security.stackexchange.com/questions/8964/ for details.
#
# Note: This doesn't really help all that much. In order to Django behave, you
# have to configure your proxy to send proper X-Forward-* headers and enable
# SECURE_PROXY_SSL_HEADER.
#
if not DEBUG:
    # Only set this in production mode, since debug servers typically don't
    # have HTTPS set up.
    os.environ['HTTPS'] = 'on'
    # HTTPS configuration
    HTTPS = True
    SECURE_PROXY_SSL_HEADER = ('HTTP_X_FORWARDED_PROTO', 'https')


ADMINS = (("web-wg", "web-wg@europython.eu"),)
MANAGERS = ADMINS

ALLOWED_HOSTS = config(
    "ALLOWED_HOSTS",
    default="*",
    cast=lambda v: [s.strip() for s in v.split(",")],
)
APPEND_SLASH = config("APPEND_SLASH", default=True, cast=bool)

PROJECT_DIR = config(
    "PROJECT_DIR",
    default=os.path.normpath(os.path.join(os.path.dirname(__file__), "..")),
)
DATA_DIR = config("DATA_DIR", default=os.path.join(PROJECT_DIR, "data"))
OTHER_STUFF = config(
    "OTHER_STUFF", default=os.path.join(PROJECT_DIR, "documents")
)

LOGS_DIR = os.path.join(PROJECT_DIR, "logs/")

SITE_DATA_ROOT = DATA_DIR + "/site"

# DATABASE
# --------
DATABASES = {
    'default': dj_database_url.config(
        default='sqlite:///{}/epcon.db'.format(SITE_DATA_ROOT)
    ),
}

# Email
# -----
EMAIL_BACKEND = 'django.core.mail.backends.smtp.EmailBackend'
# EuroPython outgoing mail server
EMAIL_HOST = "mail.europython.io"

# Email sender address to use for emails generated by Django for admins
SERVER_EMAIL = config('SERVER_EMAIL', default='noreply@europython.eu')

# Email sender address used per default for emails to e.g. attendees
DEFAULT_FROM_EMAIL = config('DEFAULT_FROM_EMAIL', default='info@europython.eu')


# Timezone and languages
# -----------------------
# If you set this to False, Django will make some optimizations so as not
# to load the internationalization machinery.
USE_I18N = True

# If you set this to False, Django will not format dates, numbers and
# calendars according to the current locale.
USE_L10N = True

# If you set this to False, Django will not use timezone-aware datetimes.
USE_TZ = True

TIME_ZONE = 'Europe/Zurich'
LANGUAGE_CODE = 'en'

LANGUAGES = (
    ('en', _('English')),
)

CONFERENCE_TALK_SUBMISSION_LANGUAGES = (
    ('en', _('English')),
)

# Site ID
SITE_ID = 1

# Absolute filesystem path to the directory that will hold user-uploaded files.
# Example: "/home/media/media.lawrence.com/media/"

MEDIA_ROOT = DATA_DIR + '/media_public'
SECURE_MEDIA_ROOT = DATA_DIR + '/media_private'

# URL that handles the media served from MEDIA_ROOT. Make sure to use a
# trailing slash.
# Examples: "http://media.lawrence.com/media/", "http://example.com/media/"
MEDIA_URL = '/media/'
SECURE_MEDIA_URL = '/p3/secure_media/'
# Absolute path to the directory static files should be collected to.
# Don't put anything in this directory yourself; store your static files
# in apps' "static/" subdirectories and in STATICFILES_DIRS.
# Example: "/home/media/media.lawrence.com/static/"
STATIC_ROOT = DATA_DIR + '/static/'

# URL prefix for static files.
# Example: "http://media.lawrence.com/static/"
STATIC_URL = '/static/'

# Additional locations of static files
STATICFILES_DIRS = [
    os.path.join(PROJECT_DIR, 'assets'),
]

# List of finder classes that know how to find static files in
# various locations.
STATICFILES_FINDERS = (
    'django.contrib.staticfiles.finders.FileSystemFinder',
    'django.contrib.staticfiles.finders.AppDirectoriesFinder',
    # 'django.contrib.staticfiles.finders.DefaultStorageFinder',
)

# Make this unique, and don't share it with anybody.
SECRET_KEY = config('SECRET_KEY', default='your-secret-key')

SOCIAL_AUTH_GOOGLE_OAUTH2_KEY = config(
    "SOCIAL_AUTH_GOOGLE_OAUTH2_KEY", default=""
)
SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET = config(
    "SOCIAL_AUTH_GOOGLE_OAUTH2_SECRET", default=""
)

SOCIAL_AUTH_PIPELINE = (
    'social_core.pipeline.social_auth.social_details',
    'social_core.pipeline.social_auth.social_uid',
    'social_core.pipeline.social_auth.auth_allowed',
    'social_core.pipeline.social_auth.social_user',
    'social_core.pipeline.user.get_username',
    'social_core.pipeline.mail.mail_validation',
    'social_core.pipeline.social_auth.associate_by_email',
    'social_core.pipeline.user.create_user',
    # THIS IS IMPORTANT!!!! Connect new authenticated users to profiles
    # of the important project apps!!
    'conference.accounts.social_connect_profile',

    'social_core.pipeline.social_auth.associate_user',
    'social_core.pipeline.social_auth.load_extra_data',
    'social_core.pipeline.user.user_details'
)

TEMPLATES = [
    {
        "BACKEND": "django.template.backends.django.DjangoTemplates",
        "DIRS": [os.path.join(PROJECT_DIR, "templates")],
        "OPTIONS": {
            "debug": DEBUG,
            "context_processors": [
                "django.contrib.auth.context_processors.auth",
                "django.contrib.messages.context_processors.messages",
                "django.template.context_processors.i18n",
                "django.template.context_processors.debug",
                "django.template.context_processors.request",
                "django.template.context_processors.media",
                "django.template.context_processors.csrf",
                "django.template.context_processors.request",
                "django.template.context_processors.tz",
                "p3.context_processors.settings",
                "conference.context_processors.current_url",
                "conference.context_processors.stuff",
                "sekizai.context_processors.sekizai",
                "cms.context_processors.cms_settings",
                "django.template.context_processors.static",
                "social_django.context_processors.backends",
                "social_django.context_processors.login_redirect",
            ],
            "loaders": [
                "django.template.loaders.filesystem.Loader",
                "django.template.loaders.app_directories.Loader",
            ],
        },
    }
]

MIDDLEWARE = (
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'django.middleware.http.ConditionalGetMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',

    'assopy.middleware.DebugInfo',

    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
)

ROOT_URLCONF = 'pycon.urls'

# Python dotted path to the WSGI application used by Django's runserver.
WSGI_APPLICATION = 'pycon.wsgi.application'


LOCALE_PATHS = (
    os.path.join(PROJECT_DIR, 'locale'),
)

INSTALLED_APPS = (
    'filebrowser',

    'djangocms_admin_style',
    'django_comments',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.sites',
    'django.contrib.messages',
    'django.contrib.admin',
    'django.contrib.staticfiles',
    'django.contrib.redirects',

    'p3',
    'assopy',
    'assopy.stripe',
    'conference',
    'hcomments',

    'djangocms_text_ckeditor',
    'cmsplugin_filer_file',
    'cmsplugin_filer_folder',
    'cmsplugin_filer_link',
    'cmsplugin_filer_image',
    'cmsplugin_filer_teaser',
    'cmsplugin_filer_video',
    'djangocms_grid',

    'treebeard',
    'cms',
    'menus',
    'sekizai',
    'tagging',
    'taggit',
    'taggit_labels',
    'authority',
    # 'pages',
    'mptt',
    'crispy_forms',

    'django_xmlrpc',
    'rosetta',

    'email_template',
    # 'paypal.standard.ipn',
    'filer',
    'easy_thumbnails',

    'django_crontab',
    'formstyle',

    'markitup',
    'cms_utils',
    'social_django',
)

# A sample logging configuration. The only tangible logging
# performed by this configuration is to send an email to
# the site admins on every HTTP 500 error when DEBUG=False.
# See http://docs.djangoproject.com/en/dev/topics/logging for
# more details on how to customize your logging configuration.
LOGGING = {
    'version': 1,
    'disable_existing_loggers': False,
    'formatters': {
        'verbose': {
            'format': (
                '%(asctime)s [%(process)d] '
                '%(levelname)s - %(name)s - %(module)s -'
                '%(funcName)s: %(message)s'
            )
        },
        'simple': {
            'format': (
                '%(levelname)s - %(name)s - %(module)s -'
                '%(funcName)s: %(message)s'
            )
        },
    },
    'filters': {
        'require_debug_false': {
            '()': 'django.utils.log.RequireDebugFalse'
        }
    },
    'handlers': {
        'mail_admins': {
            'level': 'ERROR',
            'filters': ['require_debug_false'],
            'class': 'django.utils.log.AdminEmailHandler'
        },
        'console': {
            'level': 'DEBUG',
            'class': 'logging.StreamHandler',
            'formatter': 'simple',
        },
        'file': {
            'level': 'DEBUG',
            'class': 'logging.FileHandler',
            'filename': os.path.join(LOGS_DIR, 'conference.log'),
            'encoding': 'utf-8',
            'formatter': 'verbose',
        },
    },
    'loggers': {
        'django.request': {
            'handlers': ['file', 'mail_admins'],
            'level': 'ERROR',
            'propagate': True,
        },
        'conference.tags': {
            'handlers': ['console', 'file'],
            'level': 'DEBUG',
            'propagate': False,
        },
        'assopy.views': {
            'handlers': ['file'],
            'level': 'DEBUG',
            'propagate': False,
        },
    }
}

AUTHENTICATION_BACKENDS = (
    'assopy.auth_backends.IdBackend',
    'assopy.auth_backends.EmailBackend',
    'django.contrib.auth.backends.ModelBackend',

    'social_core.backends.google.GoogleOAuth2',
)


# URL prefix for admin media -- CSS, JavaScript and images. Make sure to use a
# trailing slash.
# Examples: "http://foo.com/media/", "/media/".
ADMIN_MEDIA_PREFIX = '/static/admin/'
FILEBROWSER_URL_FILEBROWSER_MEDIA = '/static/filebrowser/'

PAGE_USE_SITE_ID = False
DEFAULT_PAGE_TEMPLATE = 'cms/content.html'
PAGE_UNIQUE_SLUG_REQUIRED = False
PAGE_TAGGING = True
PAGE_LANGUAGES = (
    ('en-us', _('English')),
)
PAGE_DEFAULT_LANGUAGE = PAGE_LANGUAGES[0][0]
PAGE_LANGUAGE_MAPPING = lambda lang: PAGE_LANGUAGES[0][0]  # NOQA

PAGE_REAL_TIME_SEARCH = False

PAGE_USE_STRICT_URL = True

ROSETTA_EXCLUDED_APPLICATIONS = (
    'debug_toolbar',
    'filebrowser',
    'pages',
    'rosetta',
)

CMS_LANGUAGES = {
    1: [
        {
            'code': 'en',
            'name': _('English'),
        },
    ],
    'default': {
        'fallbacks': ['en'],
        'redirect_on_fallback': True,
        'public': True,
        'hide_untranslated': False,

    }
}
CMS_TEMPLATES = (
    # ('django_cms/p5_homepage.html', 'Homepage'),
    # ('django_cms/content.html', 'Content page'),
    # ('django_cms/content-1col.html', 'Content page, single column'),
    # ('django_cms/p5_home_splash.html', 'Homepage, splash'),
    # ('ep19/bs/content/generic_content_page.html', 'Generic Content Page'),
    # ('ep19/bs/homepage/home.html', 'Homepage'),
    ('ep19/bs/content/generic_content_page_with_sidebar.html',
     'Generic Content Page (with sidebar)'),
)
PAGE_TEMPLATES = (
    ('ep19/bs/content/generic_content_page_with_sidebar.html',
     'Generic Content Page (with sidebar)'),
)
CMS_PLUGIN_PROCESSORS = (
    'cms_utils.processors.process_templatetags',
)
MARKITUP_FILTER = ('markdown2.markdown', {'safe_mode': False})

CKEDITOR_SETTINGS = {
    'height': 300,
    'stylesSet': 'default:/static/p6/javascripts/ckeditor.wysiwyg.js',
    'contentsCss': ['/static/css/base.css'],
    'language': '{{ language }}',
    'toolbar': 'CMS',
    'extraPlugins': 'cmsplugins',
    'basicEntities': False,
    'entities': False,
}

# html5lib sanitizer settings
TEXT_ADDITIONAL_TAGS = ('iframe',)
TEXT_ADDITIONAL_ATTRIBUTES = (
    "scrolling",
    "allowfullscreen",
    "frameborder",
    "src",
    "height",
    "width",
)

#
# We're not going to use this feature for EuroPython 2015+:
#
THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters',
)
THUMBNAIL_HIGH_RESOLUTION = True

DJANGOCMS_GRID_CONFIG = {
    'COLUMNS': 100,
    'TOTAL_WIDTH': 960,
    'GUTTER': 20,
}


CRISPY_TEMPLATE_PACK = "bootstrap4"

# Override the message class to get it to work with bootstrap styles.
from django.contrib.messages import constants as messages
MESSAGE_TAGS = {
    messages.ERROR: 'danger',
}
# TODO umgelurgel: this is only required for ep2019;
#  remove this after ep2019 and before ep2020
MESSAGE_STORAGE = 'conference.messages.CustomFallbackStorage'


#
# Session management
#
SESSION_COOKIE_NAME = 'sid'
SESSION_SERIALIZER = 'django.contrib.sessions.serializers.PickleSerializer'

CONFERENCE_CONFERENCE = 'ep2019'
CONFERENCE_NAME = "EuroPython 2019"
CONFERENCE_SEND_EMAIL_TO = ["helpdesk@europython.eu"]
CONFERENCE_TALK_SUBMISSION_NOTIFICATION_EMAIL = []
CONFERENCE_VOTING_DISALLOWED = 'https://ep2019.europython.eu/en/talk-voting/'
CONFERENCE_TALK_VOTING_ELIGIBLE = (
    "ep2015",
    "ep2016",
    "ep2017",
    "ep2018",
    "ep2019",
)

CONFERENCE_FORMS = {
    'PaperSubmission': 'p3.forms.P3SubmissionForm',
    'AdditionalPaperSubmission': 'p3.forms.P3SubmissionAdditionalForm',
    'Profile': 'p3.forms.P3ProfileForm',
    'EventBooking': 'p3.forms.P3EventBookingForm',
}

CONFERENCE_TALKS_RANKING_FILE = SITE_DATA_ROOT + '/rankings.txt'
CONFERENCE_ADMIN_TICKETS_STATS_EMAIL_LOG = (
    SITE_DATA_ROOT + "/admin_ticket_emails.txt"
)
CONFERENCE_ADMIN_TICKETS_STATS_EMAIL_LOAD_LIBRARY = ['p3', 'conference']

# Conference sub-communities
CONFERENCE_TALK_SUBCOMMUNITY = (
    ('', _('All')),
    ('pydata', _('PyData')),
)

CONFERENCE_TALK_DOMAIN = Choices(
    ('business_track', _('Business Track')),
    ('devops', _('DevOps')),
    ('django', _('Django Track')),
    ('education', _('Educational Track')),
    ('general', _('General Python')),
    ('hw_iot', _('Hardware/IoT Track')),
    ('pydata', _('PyData Track')),
    ('science', _('Science Track')),
    ('web', _('Web Track')),
    ('', 'other', _('Other'))
)


# T-shirt sizes
# TODO: Make that into Choices
CONFERENCE_TICKET_CONFERENCE_SHIRT_SIZES = (
    ('fs', 'S (female)'),
    ('fm', 'M (female)'),
    ('fl', 'L (female)'),
    ('fxl', 'XL (female)'),
    ('fxxl', 'XXL (female)'),
    ('fxxxl', '3XL (female)'),
    ('s', 'S (male)'),
    ('m', 'M (male)'),
    ('l', 'L (male)'),
    ('xl', 'XL (male)'),
    ('xxl', 'XXL (male)'),
    ('xxxl', '3XL (male)'),
    ('xxxxl', '4XL (male)'),
)

# Available diets
CONFERENCE_TICKET_CONFERENCE_DIETS = (
    ("omnivorous", _("Omnivorous")),
    ("vegetarian", _("Vegetarian")),
    # ('vegan', _('Vegan')),
    # ('kosher', _('Kosher')),
    # ('halal', _('Halal')),
    ("other", _("Other")),
)

# Python experience
CONFERENCE_TICKET_CONFERENCE_EXPERIENCES = (
    (0, _('no comment')),
    (1, _('1 star  (just starting)')),
    (2, _('2 stars (beginner)')),
    (3, _('3 stars (intermediate)')),
    (4, _('4 stars (expert))')),
    (5, _('5 stars (guru level)')),
)


def CONFERENCE_TICKETS(conf, ticket_type=None, fare_code=None):
    from p3 import models

    tickets = models.Ticket.objects \
        .filter(fare__conference=conf, orderitem__order___complete=True)
    if ticket_type:
        tickets = tickets.filter(fare__ticket_type=ticket_type)
    if fare_code:
        if fare_code.endswith('%'):
            tickets = tickets.filter(fare__code__startswith=fare_code[:-1])
        else:
            tickets = tickets.filter(fare__code=fare_code)
    return tickets


def CONFERENCE_VOTING_OPENED(conf, user):
    # Can access the page:
    #   anyone during community voting
    #   superusers
    #   speakers (of current conference)
    #   who is in the special "pre_voting" group
    if user.is_superuser:
        return True

    # Only allow access during talk voting period
    if conf.voting():
        return True
    else:
        return False

    # XXX Disabled these special cases, since it's not clear
    #     what they are used for
    if 0:
        from p3.models import TalkSpeaker, Speaker
        try:
            count = TalkSpeaker.objects.filter(
                talk__conference=CONFERENCE_CONFERENCE,
                speaker=user.speaker).count()
        except (AttributeError, Speaker.DoesNotExist):
            pass
        else:
            if count > 0:
                return True

        # Special case for "pre_voting" group members;
        if user.groups.filter(name='pre_voting').exists():
            return True

    return False


def CONFERENCE_VOTING_ALLOWED(user):

    """ Determine whether user is allowed to participate in talk voting.

    """
    if not user.is_authenticated:
        return False
    if user.is_superuser:
        return True

    # Speakers of the current conference are always allowed to vote
    from conference.models import TalkSpeaker, Speaker
    try:
        count = TalkSpeaker.objects.filter(
            talk__conference=CONFERENCE_CONFERENCE,
            speaker=user.speaker).count()
    except Speaker.DoesNotExist:
        pass
    else:
        if count > 0:
            return True

    # People who have a ticket for the current conference assigned to
    # them can vote
    from p3 import models

    # Starting with EP2017, we allow people who have bought tickets in the
    # past, to also participate in talk voting.
    tickets = (
        models.TicketConference
        .objects
        .filter(
            ticket__fare__conference__in=CONFERENCE_TALK_VOTING_ELIGIBLE,
            assigned_to=user.email
        )
    )
    if tickets.count() > 0:
        return True

    # Starting with EP2017, we know that all assigned tickets have
    # .assigned_to set correctly
    # tickets = models.TicketConference.objects \
    #          .filter(ticket__fare__conference=CONFERENCE_CONFERENCE,
    #                  assigned_to=user.email)

    # Old query (for tickets bought before 2017)
    from django.db.models import Q
    for conf in CONFERENCE_TALK_VOTING_ELIGIBLE:
        tickets = (
            models.TicketConference
            .objects
            .available(user, conf)
            .filter(
                Q(orderitem__order___complete=True)
                | Q(orderitem__order__method='admin')
            )
            .filter(
                Q(p3_conference=None)
                | Q(p3_conference__assigned_to='')
                | Q(p3_conference__assigned_to=user.email)
            )
        )

        if tickets.count() > 0:
            return True
    return False


def CONFERENCE_SCHEDULE_ATTENDEES(schedule, forecast):
    from p3.stats import presence_days
    from conference.models import Schedule

    if not isinstance(schedule, Schedule):
        output = {}
        for s in Schedule.objects.filter(conference=schedule):
            output[s.id] = CONFERENCE_SCHEDULE_ATTENDEES(s, forecast)
        return output
    d = schedule.date.strftime('%Y-%m-%d')
    s = presence_days(schedule.conference)
    for row in s['data']:
        if row['title'] == '%s (no staff)' % d:
            if forecast:
                return row['total_nc']
            else:
                return row['total']
    return 0


CONFERENCE_ADMIN_ATTENDEE_STATS = (
    'p3.stats.tickets_status',
    'p3.stats.conference_speakers',
    'p3.stats.conference_speakers_day',
    'p3.stats.speaker_status',
    'p3.stats.presence_days',
    'p3.stats.shirt_sizes',
    'p3.stats.diet_types',
    'p3.stats.pp_tickets',
)


CONFERENCE_TICKET_BADGE_ENABLED = True
CONFERENCE_TICKET_BADGE_PROG_ARGS = ['-e', '0', '-p', 'A4', '-n', '1']


def CONFERENCE_TICKET_BADGE_PREPARE_FUNCTION(tickets):
    from p3.utils import conference_ticket_badge

    return conference_ticket_badge(tickets)


def CONFERENCE_TALK_VIDEO_ACCESS(request, talk):
    return True
    if talk.conference != CONFERENCE_CONFERENCE:
        return True
    u = request.user
    if u.is_anonymous:
        return False
    from p3.models import Ticket

    qs = Ticket.objects \
        .filter(id__in=[x.id for x in u.assopy_user.tickets()]) \
        .filter(orderitem__order___complete=True,
                fare__ticket_type='conference')
    return qs.exists()


def ASSOPY_ORDERITEM_CAN_BE_REFUNDED(user, item):
    if user.is_superuser:
        return True
    return False
    if not item.ticket:
        return False
    ticket = item.ticket
    if ticket.user != user:
        return False
    if ticket.fare.conference != CONFERENCE_CONFERENCE:
        return False
    if item.order.total() == 0:
        return False
    return item.order._complete


#
# XXX What is this AssoPy stuff ?
#
ASSOPY_BACKEND = 'https://assopy.europython.eu/conference/externalcall'
ASSOPY_SEARCH_MISSING_USERS_ON_BACKEND = False
ASSOPY_TICKET_PAGE = 'p3-tickets'
ASSOPY_SEND_EMAIL_TO = ['billing-log@europython.io']
ASSOPY_REFUND_EMAIL_ADDRESS = {
    'approve': ['billing@europython.eu'],
    'execute': {
        None: ['billing@europython.eu'],
        'bank': ['billing@europython.eu'],
    },
    'credit-note': ['billing@europython.eu'],
}

#
# This URL needs to be set to the main URL of the site.
#
# It is used for generating URLs pointing back to the site
# in quite a few places.
#
DEFAULT_URL_PREFIX = 'https://ep2019.europython.eu'
LOGIN_REDIRECT_URL = reverse_lazy("user_panel:dashboard")

COMMENTS_APP = 'hcomments'

# Disabled until we find out how to use europython-announce for this:
#P3_NEWSLETTER_SUBSCRIBE_URL = "https://mail.python.org/mailman/subscribe/europython-announce"
P3_NEWSLETTER_SUBSCRIBE_URL = ""

P3_TWITTER_USER = 'europython'
P3_USER_MESSAGE_FOOTER = '''

This message was sent from a participant at the EuroPython conference.
Your email address is not disclosed to anyone, to stop receiving messages
from other users you can change your privacy settings from this page:
https://ep2019.europython.eu/accounts/profile/
'''


P3_ANONYMOUS_AVATAR = 'p5/images/headshot-default.jpg'

#
# These are probably meant for live streaming on-site servers. We don't
# use these at the moment...
#
P3_LIVE_INTERNAL_IPS = ('2.228.78.', '10.3.3.', '127.0.0.1')
P3_INTERNAL_SERVER = 'live.ep:1935'

P3_LIVE_TRACKS = {
    'track1': {
        'stream': {
            'external': 'WQnU7Qvy-xg',
            'internal': 'live/spaghetti',
        }
    },
    'track2': {
        'stream': {
            'external': 'urwOdSH3Tyg',
            'internal': 'live/lasagne',
        }
    },
    'track3': {
        'stream': {
            'external': 'tdGKPPlhqAI',
            'internal': 'live/ravioli',
        }
    },
    'track4': {
        'stream': {
            'external': 'IeKx5Qy_8lY',
            'internal': 'live/tagliatelle',
        }
    },
    'track-ita': {
        'stream': {
            'external': 'JSjXKGom9VI',
            'internal': 'live/bigmac',
        }
    },
    'training1': {
        'stream': {
            'external': '6CG-25uxPdI',
            'internal': 'live/pizzamargherita',
        }
    },
    'training2': {
        'stream': {
            'external': 'iy1phHF-mec',
            'internal': 'live/pizzanapoli',
        }
    },
}


def P3_LIVE_REDIRECT_URL(request, track):
    internal = False
    for check in P3_LIVE_INTERNAL_IPS:
        if request.META['REMOTE_ADDR'].startswith(check):
            internal = True
            break
    url = None
    if internal:
        import re

        ua = request.META['HTTP_USER_AGENT']

        base = '{0}/{1}'.format(P3_INTERNAL_SERVER,
                                P3_LIVE_TRACKS[track]['stream']['internal'])
        if re.search('Android', ua, re.I):
            url = 'rtsp://' + base
        elif re.search('iPhone|iPad|iPod', ua, re.I):
            url = 'http://%s/playlist.m3u8' % base
        else:
            url = 'rtmp://' + base
    else:
        try:
            url = 'https://www.youtube.com/watch?v={0}'.format(
                P3_LIVE_TRACKS[track]['stream']['external'])
        except KeyError:
            pass
    return url


def P3_LIVE_EMBED(request, track=None, event=None):
    from django.core.cache import cache

    if not any((track, event)) or all((track, event)):
        raise ValueError('track or event, not both')

    if event:
        # ep2012, all keynotes are recorded in track "lasagne"
        if 'keynote' in event['tags'] or len(event['tracks']) > 1:
            track = 'track2'
        else:
            track = event['tracks'][0]

    internal = False
    for check in P3_LIVE_INTERNAL_IPS:
        if request.META['REMOTE_ADDR'].startswith(check):
            internal = True
            break

    if internal:
        try:
            url = '{0}/{1}'.format(P3_INTERNAL_SERVER,
                                   P3_LIVE_TRACKS[track]['stream']['internal'])
        except KeyError:
            return None
        data = {
            'track': track,
            'stream': url.rsplit('/', 1)[1],
            'url': url,
        }
        html = ("""
        <div>
            <div class="button" style="float: left; margin-right: 20px;">
                <h5><a href="rtsp://%(url)s">RTSP</a></h5>
                For almost all<br/>Linux, Windows, Android
            </div>
            <div class="button" style="float: left; margin-right: 20px;">
                <h5><a href="http://%(url)s/playlist.m3u8">HLS&#xF8FF;</a></h5>
                Apple world (mainly)
            </div>
            <div class="button" style="float: left; margin-right: 20px;">
                <h5><a href="#" onclick="start_%(stream)s(); return false;">Flash</a></h5>
                Old good school
            </div>
            <div id="stream-%(track)s" style="clear: both();width:530px;height:298px;margin:0 auto;text-align:center"> </div>
            <script>
                function start_%(stream)s() {
                    $f("stream-%(track)s", "/static/p5/flowplayer/flowplayer-3.2.12.swf", {

                        clip: {
                            autoPlay: false,
                            url: 'mp4:%(stream)s',
                            scaling: 'fit',
                            // configure clip to use hddn as our provider, refering to our rtmp plugin
                            provider: 'hddn'
                        },

                        // streaming plugins are configured under the plugins node
                        plugins: {

                            // here is our rtmp plugin configuration
                            hddn: {
                                url: "/static/p5/flowplayer/flowplayer.rtmp-3.2.10.swf",

                                // netConnectionUrl defines where the streams are found
                                netConnectionUrl: 'rtmp://%(url)s'
                            }
                        }
                    });
                }
            </script>
        </div>
        """ % data) #" (makes emacs highlighting happy)
        return html
    else:
        data = cache.get('p3_live_embed_%s' % track)
        if data is not None:
            return data

        try:
            yurl = 'https://www.youtube.com/watch?v={0}'.format(
                P3_LIVE_TRACKS[track]['stream']['external'])
        except KeyError:
            return None

        import httplib2, json

        http = httplib2.Http()
        service = 'https://www.youtube.com/oembed'
        url = service + '?url=' + yurl + '&format=json&scheme=https'
        try:
            response, content = http.request(url)
            data = json.loads(content)
        except:
            return None
        cache.set('p3_live_embed_%s' % track, data['html'], 3600)
        return data['html']


# Stripe payment integration
# --------------------------
STRIPE_ENABLED = True
STRIPE_SECRET_KEY = config("STRIPE_SECRET_KEY", default='')
STRIPE_PUBLISHABLE_KEY = config("STRIPE_PUBLISHABLE_KEY", default='')
STRIPE_COMPANY_NAME = config("STRIPE_COMPANY_NAME", default='')
STRIPE_COMPANY_LOGO = config("STRIPE_COMPANY_LOGO", default='')
STRIPE_CURRENCY = "EUR"
STRIPE_ALLOW_REMEMBER_ME = False

# Paypl integration
# Paypal merchant email
PAYPAL_RECEIVER_EMAIL = config("PAYPAL_RECEIVER_EMAIL", default='')

# If the merchant account is a debug one set this flag to True
PAYPAL_TEST = config('PAYPAL_TEST', default=False, cast=bool)

# files under SECURE_MEDIA_BOOT must be served by django, this if
# is needed to avoid they end up in a subdir of MEDIA_ROOT that is
# normally served by an external webserver
check = os.path.commonprefix((MEDIA_ROOT, SECURE_MEDIA_ROOT))
if check.startswith(MEDIA_ROOT):
    if not DEBUG:
        raise RuntimeError('SECURE_MEDIA_ROOT cannot be a subdir of MEDIA_ROOT')
    else:
        print('WARN, SECURE_MEDIA_ROOT is a subdir of MEDIA_ROOT')


if not SECRET_KEY:
    if not DEBUG:
        raise RuntimeError('SECRET_KEY not set')
    else:
        print('WARN, SECRET_KEY not set')

# This is used just for tests
DISABLE_CACHING = False

# Complete project setup.
if not os.path.exists(LOGS_DIR):
    os.makedirs(LOGS_DIR)

# TODO: Remove the need for modifying python path in django settings.
sys.path.insert(0, os.path.join(PROJECT_DIR, 'deps'))


try:
    from pycon.settings_locale import *
except ImportError as reason:
    #import sys
    #sys.stderr.write('Could not import local settings: %s\n' % reason)
    pass
