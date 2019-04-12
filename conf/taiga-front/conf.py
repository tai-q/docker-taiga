import os
import json

def getenv_boolean(name: str) -> bool:
    return name in os.environ and os.getenv(name).lower() == 'true'

def getenv_or_none(name: str) -> str:
    return os.getenv(name) if (name in os.environ and os.getenv(name) != '') else None

config = dict({
    'api': os.getenv('FRONT_API_URL', 'https://localhost/api/v1/'),
    'eventsUrl': getenv_or_none('FRONT_EVENTS_URL'),
    'eventsMaxMissedHeartbeats': 5,
    'eventsHeartbeatIntervalTime': 60000,
    'eventsReconnectTryInterval': 10000,
    'debug': getenv_boolean('DEBUG'),
    'debugInfo': False,
    'defaultLanguage': os.getenv('FRONT_DEFAULT_LANGUAGE', 'en'),
    'themes': ('taiga',),
    'defaultTheme': 'taiga',
    'publicRegisterEnabled': getenv_boolean('PUBLIC_REGISTER_ENABLED'),
    'feedbackEnabled': getenv_or_none('FEEDBACK_ENABLED'),
    'supportUrl': getenv_or_none('FRONT_SUPPORT_URL'),
    'privacyPolicyUrl': getenv_or_none('FRONT_PRIVACY_POLICY_URL'),
    'termsOfServiceUrl': getenv_or_none('FRONT_TERMS_OF_SERVICE_URL'),
    'GDPRUrl': getenv_or_none('FRONT_GDPR_URL'),
    'maxUploadFileSize': getenv_or_none('FRONT_MAX_FILESIZE'),
    'contribPlugins': [],
    'tribeHost': None,
    'importers': [],
    'gravatar': getenv_boolean('FRONT_GRAVATAR_ENABLED'),
    'rtlLanguages': ('fa', )
})

if getenv_boolean('LDAP_ENABLED'):
    config.update({'loginFormType': 'ldap'})

print(json.dumps(config))