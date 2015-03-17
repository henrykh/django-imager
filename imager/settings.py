"""
Django settings for imager project.

For more information on this file, see
https://docs.djangoproject.com/en/1.7/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.7/ref/settings/
"""

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
import os
import dj_database_url
from configurations import Configuration


class Base(Configuration):
    BASE_DIR = os.path.dirname(os.path.dirname(__file__))
    USER_NAME = os.environ.get('USER')


    # Quick-start development settings - unsuitable for production
    # See https://docs.djangoproject.com/en/1.7/howto/deployment/checklist/

    # SECURITY WARNING: keep the secret key used in production secret!
    SECRET_KEY = 'i4jz)*^p(o@s32p1)wdq@yonk$d+pdx_b0t%b4(7vn4hztdwrf'

    # SECURITY WARNING: don't run with debug turned on in production!
    # if USER_NAME == 'ubuntu':
    #     DEBUG = False
    #     TEMPLATE_DEBUG = False
    # else:
    #     DEBUG = True
    #     TEMPLATE_DEBUG = True


    ALLOWED_HOSTS = []

    SITE_ID = 1

    # IPs
    INTERNAL_IPS = ('127.0.0.1',
                    '::1'
                    )

    # Application definition

    INSTALLED_APPS = (
        'grappelli',
        'django.contrib.admin',
        'django.contrib.auth',
        'django.contrib.contenttypes',
        'django.contrib.sessions',
        'django.contrib.messages',
        'django.contrib.staticfiles',
        # 'django.contrib.sites',
        'imager_user',
        'imager_images',
        'sorl.thumbnail',
        'registration',
    )

    MIDDLEWARE_CLASSES = (
        'django.contrib.sessions.middleware.SessionMiddleware',
        'django.middleware.common.CommonMiddleware',
        'django.middleware.csrf.CsrfViewMiddleware',
        'django.contrib.auth.middleware.AuthenticationMiddleware',
        'django.contrib.auth.middleware.SessionAuthenticationMiddleware',
        'django.contrib.messages.middleware.MessageMiddleware',
        'django.middleware.clickjacking.XFrameOptionsMiddleware',
        'debug_toolbar.middleware.DebugToolbarMiddleware',
    )

    ROOT_URLCONF = 'imager.urls'

    WSGI_APPLICATION = 'imager.wsgi.application'


    DATABASES = {
        'default': dj_database_url.config(
         default='postgres://'+USER_NAME+':@localhost:5432/django_imager')
        }

    # Internationalization
    # https://docs.djangoproject.com/en/1.7/topics/i18n/

    LANGUAGE_CODE = 'en-us'

    TIME_ZONE = 'UTC'

    USE_I18N = True

    USE_L10N = True

    USE_TZ = True

    # Request context processor
    from django.conf.global_settings import TEMPLATE_CONTEXT_PROCESSORS
    TEMPLATE_CONTEXT_PROCESSORS += ("django.core.context_processors.request",)

    # Static files (CSS, JavaScript, Images)
    # https://docs.djangoproject.com/en/1.7/howto/static-files/

    STATIC_URL = '/static/'
    STATIC_ROOT = os.path.join(BASE_DIR, "static")
    STATICFILES_DIRS = (
        os.path.join(BASE_DIR, "imager/static/"),
        )

    MEDIA_URL = "/media/"
    MEDIA_ROOT = os.path.join(BASE_DIR, "media")

    TEMPLATE_DIRS = (
        os.path.join(BASE_DIR, "imager/templates/"),
        )

    # Email backend for development
    EMAIL_BACKEND = 'django.core.mail.backends.console.EmailBackend'

    # Registration settings
    ACCOUNT_ACTIVATION_DAYS = 7
    REGISTRATION_AUTO_LOGIN = True
    REGISTRATION_OPEN = True
    LOGIN_URL = '/accounts/login/'
    LOGIN_REDIRECT_URL = '/profile/'


class Dev(Base):
    DEBUG = True
    TEMPLATE_DEBUG = True
    # Debug toolbar settings
    DEBUG_TOOLBAR_PATCH_SETTINGS = False
    DEBUG_TOOLBAR_PANELS = (
        'debug_toolbar.panels.versions.VersionsPanel',
        'debug_toolbar.panels.timer.TimerPanel',
        'debug_toolbar.panels.settings.SettingsPanel',
        'debug_toolbar.panels.headers.HeadersPanel',
        'debug_toolbar.panels.request.RequestPanel',
        'debug_toolbar.panels.sql.SQLPanel',
        'debug_toolbar.panels.staticfiles.StaticFilesPanel',
        'debug_toolbar.panels.templates.TemplatesPanel',
        'debug_toolbar.panels.cache.CachePanel',
        'debug_toolbar.panels.signals.SignalsPanel',
        'debug_toolbar.panels.logging.LoggingPanel',
        'debug_toolbar.panels.redirects.RedirectsPanel',
    )

    Base.INSTALLED_APPS += ('debug_toolbar', )

    # Password hasher for development
    PASSWORD_HASHERS = ('django.contrib.auth.hashers.MD5PasswordHasher',
                        )


class Prod(Base):
    DEBUG = False
    TEMPLATE_DEBUG = False
