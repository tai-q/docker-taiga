from .common import *

def getenv_boolean(name: str) -> bool:
    return name in os.environ and os.getenv(name).lower() == 'true'

def getenv_or_none(name: str) -> str:
    return os.getenv(name) if (name in os.environ and os.getenv(name) != '') else None

def getenv_list(name: str) -> list:
    result = getenv_or_none(name)
    return result.split(",") if result else None

#################################################
#                   General                     #
#################################################

DEBUG = getenv_boolean('DEBUG')
SECRET_KEY = os.getenv('SECRET_KEY')


#################################################
#                   Database                    #
#################################################

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': os.getenv('DB_NAME', 'taiga'),
        'HOST': os.getenv('DB_HOST', 'postgres'),
        'USER': os.getenv('DB_USER', 'taiga'),
        'PASSWORD': os.getenv('DB_PASSWORD', 'taiga_pw'),
        'PORT': os.getenv('DB_PORT', '5432')
    }
}


#################################################
#                   URLs                        #
#################################################

_url_scheme = os.getenv('URL_SCHEME', 'http')
_url_host = os.getenv('URL_HOST', 'localhost')
_base_url = "{}://{}".format(_url_scheme, _url_host)

MEDIA_URL = "{}/media/".format(_base_url)
STATIC_URL = "{}/static/".format(_base_url)

MEDIA_ROOT = '/data/media'
STATIC_ROOT = '/app/taiga-back/static'

SITES = {
    "api": {
       "scheme": _url_scheme,
       "domain": _url_host,
       "name": "api"
    },
    "front": {
       "scheme": _url_scheme,
       "domain": _url_host,
       "name": "front"
    },
}


#################################################
#                   TAIGA                       #
#################################################

PUBLIC_REGISTER_ENABLED = getenv_boolean('PUBLIC_REGISTER_ENABLED')
USER_EMAIL_ALLOWED_DOMAINS = getenv_list('USER_EMAIL_ALLOWED_DOMAINS')
FEEDBACK_ENABLED = getenv_boolean('FEEDBACK_ENABLED')
FEEDBACK_EMAIL = getenv_or_none('FEEDBACK_EMAIL')

STATS_ENABLED = getenv_boolean('STATS_ENABLED')

MAX_PRIVATE_PROJECTS_PER_USER = getenv_or_none('MAX_PRIVATE_PROJECTS_PER_USER')
MAX_PUBLIC_PROJECTS_PER_USER = getenv_or_none('MAX_PUBLIC_PROJECTS_PER_USER')
MAX_MEMBERSHIPS_PRIVATE_PROJECTS = getenv_or_none('MAX_MEMBERSHIPS_PRIVATE_PROJECTS')
MAX_MEMBERSHIPS_PUBLIC_PROJECTS = getenv_or_none('MAX_MEMBERSHIPS_PUBLIC_PROJECTS')

FRONT_SITEMAP_ENABLED = getenv_boolean('FRONT_SITEMAP_ENABLED')
FRONT_SITEMAP_CACHE_TIMEOUT = int(os.getenv('FRONT_SITEMAP_CACHE_TIMEOUT', 24*60*60))


#################################################
#                   EMAIL                       #
#################################################

if getenv_boolean('EMAIL_ENABLED'):
    DEFAULT_FROM_EMAIL = os.getenv('DEFAULT_FROM_EMAIL')
    SERVER_EMAIL = DEFAULT_FROM_EMAIL

    CHANGE_NOTIFICATIONS_MIN_INTERVAL = os.getenv('CHANGE_NOTIFICATIONS_MIN_INTERVAL')

    EMAIL_BACKEND = "django.core.mail.backends.smtp.EmailBackend"
    EMAIL_USE_TLS = getenv_boolean('EMAIL_USE_TLS')
    EMAIL_USE_SSL = getenv_boolean('EMAIL_USE_SSL')
    EMAIL_HOST = os.getenv('EMAIL_HOST', 'localhost')
    EMAIL_PORT = int(os.getenv('EMAIL_PORT', 25))
    EMAIL_HOST_USER = os.getenv('EMAIL_HOST_USER', 'taiga@localhost')
    EMAIL_HOST_PASSWORD = os.getenv('EMAIL_HOST_PASSWORD', 'taiga_pw')


#################################################
#                ASYNC/EVENT                    #
#################################################

if getenv_boolean('EVENTS_ENABLED'):
    EVENTS_PUSH_BACKEND = "taiga.events.backends.rabbitmq.EventsPushBackend"
    EVENTS_PUSH_BACKEND_OPTIONS = {"url": os.getenv('RABBIT_MQ_URL', 'amqp://taiga:taiga_pw@rabbitmq:5672/taiga')}

if getenv_boolean('CELERY_ENABLED'):
    CELERY_ENABLED = True


#################################################
#                       LDAP                    #
#################################################

if getenv_boolean('LDAP_ENABLED'):
    INSTALLED_APPS += ['taiga_contrib_ldap_auth_ext']
    LDAP_SERVER = os.getenv('LDAP_URL', 'ldap://localhost')
    LDAP_PORT = int(os.getenv('LDAP_PORT', 389))
    LDAP_START_TLS = getenv_boolean('LDAP_USE_TLS')

    if getenv_boolean('LDAP_USE_BIND'):
        LDAP_BIND_DN = os.getenv('LDAP_BIND_DN', 'CN=taiga-bind,DC=localhost')
        LDAP_BIND_PASSWORD = os.getenv('LDAP_BIND_PW', 'taiga_pw')
    
    LDAP_SEARCH_BASE = os.getenv('LDAP_SEARCH_BASE', 'OU=users,DC=localhost')
    LDAP_SEARCH_FILTER_ADDITIONAL = os.getenv('LDAP_SEARCH_FILTER', '')
    LDAP_USERNAME_ATTRIBUTE = os.getenv('LDAP_ATTRIBUTE_USERNAME', 'uid')
    LDAP_EMAIL_ATTRIBUTE = os.getenv('LDAP_ATTRIBUTE_MAIL', 'mail')
    LDAP_FULL_NAME_ATTRIBUTE = os.getenv('LDAP_ATTRIBUTE_FULLNAME', 'displayName')

    if not getenv_boolean('LDAP_FALLBACK_LOCAL_USERS_ENABLED'):
        LDAP_FALLBACK = ""
