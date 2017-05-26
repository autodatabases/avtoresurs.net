"""
Django settings for avtoresurs_new project.

Generated by 'django-admin startproject' using Django 1.10.2.

For more information on this file, see
https://docs.djangoproject.com/en/1.10/topics/settings/

For the full list of settings and their values, see
https://docs.djangoproject.com/en/1.10/ref/settings/
"""

import os

# Build paths inside the project like this: os.path.join(BASE_DIR, ...)
from avtoresurs_new.local_settings import DB

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

# Quick-start development settings - unsuitable for production
# See https://docs.djangoproject.com/en/1.10/howto/deployment/checklist/

# SECURITY WARNING: keep the secret key used in production secret!
SECRET_KEY = 'f9vp_6q99r9gk$ptg2j@8p0eifib+64)+6+i&g-5g5#7#1tfxk'

# SECURITY WARNING: don't run with debug turned on in production!
DEBUG = True

ALLOWED_HOSTS = ['avtoresurs.net', 'localhost']

# Application definition

INSTALLED_APPS = [
    'djangocms_admin_style',
    'main',
    # 'material',
    # 'material.admin',
    'registration',
    # 'grappelli',
    'filebrowser',
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',

    'django.contrib.sites',
    'cms',
    'menus',
    'treebeard',
    'sekizai',
    'filer',
    'easy_thumbnails',
    'mptt',
    'djangocms_text_ckeditor',
    'djangocms_link',
    'djangocms_file',
    'djangocms_picture',
    'djangocms_video',
    'djangocms_googlemap',
    'djangocms_snippet',
    'djangocms_style',
    'djangocms_column',
    # 'pagination',

    'profile',
    # 'panel',
    'news',
    'tecdoc',
    'shop',
    # 'cart',
    # 'order',
    'bonus',
    # 'products',
    'service',
    'postman',

]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'django.middleware.locale.LocaleMiddleware',
    'cms.middleware.user.CurrentUserMiddleware',
    'cms.middleware.page.CurrentPageMiddleware',
    'cms.middleware.toolbar.ToolbarMiddleware',
    'cms.middleware.language.LanguageCookieMiddleware',
    'cms.middleware.utils.ApphookReloadMiddleware',
    # 'pagination.middleware.PaginationMiddleware',

]

ROOT_URLCONF = 'avtoresurs_new.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR), 'main', 'templates', ],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
                'postman.context_processors.inbox',
                'sekizai.context_processors.sekizai',
                'cms.context_processors.cms_settings',

            ],
        },
    },
]

settings_dir = os.path.dirname(__file__)
PROJECT_ROOT = os.path.abspath(os.path.dirname(settings_dir))
UNIT_TEST_FOLDER = os.path.join(PROJECT_ROOT, 'unit_tests/')

WSGI_APPLICATION = 'avtoresurs_new.wsgi.application'

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = DB

DATABASE_ROUTERS = ['avtoresurs_new.routers.TecdocRouter']

# Password validation
# https://docs.djangoproject.com/en/1.10/ref/settings/#auth-password-validators

AUTH_PASSWORD_VALIDATORS = [
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator',
    },
    {
        'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator',
    },
]

# Internationalization
# https://docs.djangoproject.com/en/1.10/topics/i18n/

LANGUAGES = [
    ('en', 'English'),
    ('ru', 'Russian'),
]

LANGUAGE_CODE = 'ru'

TIME_ZONE = 'Europe/Kaliningrad'

USE_I18N = True

USE_L10N = True

USE_TZ = True

# Static files (CSS, JavaScript, Images)
# https://docs.djangoproject.com/en/1.10/howto/static-files/

STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'static')
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# <<<<<<< HEAD
# LOGGING_CONFIG = None
# =======
# >>>>>>> e52f779225d2c433b1c57baa7434f31464cabaa8
STATICFILES_DIRS = (
    os.path.join(BASE_DIR, 'main', 'static'),
)

# "Поисковики" статики. Первый ищет статику в STATICFILES_DIRS,
# второй в папках приложений.
# STATICFILES_FINDERS = (
#     'django.contrib.staticfiles.finders.FileSystemFinder',
#     'django.contrib.staticfiles.finders.AppDirectoriesFinder',
# )


ACCOUNT_ACTIVATION_DAYS = 7

# EMAIL_USE_TLS = True
EMAIL_USE_SSL = True
EMAIL_HOST = 'smtp.yandex.ru'
EMAIL_PORT = 465
EMAIL_HOST_USER = 'no-reply@avtoresurs.net'
EMAIL_HOST_PASSWORD = 'Iddqd31337'
DEFAULT_FROM_EMAIL = 'no-reply@avtoresurs.net'
EMAIL_NOREPLY = 'no-reply@avtoresurs.net'
EMAIL_NOREPLY_LIST = ['no-reply@avtoresurs.net']
EMAIL_TO = ['avtoresurs@mail.ru']
EMAIL_BCC = ['oleg_a@outlook.com']


# POSTMAN CONFIG
POSTMAN_DISALLOW_ANONYMOUS = True
POSTMAN_DISALLOW_MULTIRECIPIENTS = True
POSTMAN_DISALLOW_COPIES_ON_REPLY = True
POSTMAN_AUTO_MODERATE_AS = True

SITE_ID = 1

CMS_TEMPLATES = [
    ('main/base.html', 'Home page template'),
]

CMS_PERMISSION = True

THUMBNAIL_HIGH_RESOLUTION = True

THUMBNAIL_PROCESSORS = (
    'easy_thumbnails.processors.colorspace',
    'easy_thumbnails.processors.autocrop',
    'filer.thumbnail_processors.scale_and_crop_with_subject_location',
    'easy_thumbnails.processors.filters'
)

TEXT_ADDITIONAL_TAGS = ('iframe',)
TEXT_ADDITIONAL_ATTRIBUTES = ('scrolling', 'allowfullscreen', 'frameborder', 'src', 'height', 'width')


