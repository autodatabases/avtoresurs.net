from django.apps import AppConfig

DE_LANG = 1
EN_LANG = 3
RU_LANG = 16


class TecdocConfig(AppConfig):
    name = 'tecdoc'

    DATABASE = 'tecdoc'
    DB_PREFIX = ''

    LANG_ID = RU_LANG

    CACHE_TIMEOUT = 60 * 60  # one hour

    # Host for generation absolute path for images and pdf
    FILE_HOST = 'http://avtoresurs.net/'