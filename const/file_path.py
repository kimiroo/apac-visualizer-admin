from pathlib import Path

from util.is_container import IS_CONTAINER

BASE_PATH = Path('/data') if IS_CONTAINER else Path('.')
APP_PATH = Path('.')
DEFAULT_PATH = APP_PATH / 'default'

PATH_CONFIG = BASE_PATH / 'config.json'
PATH_CONFIG_DEFAULT = DEFAULT_PATH / 'config.json'
PATH_COUNTRY_LIST = BASE_PATH / 'country.json'
PATH_COUNTRY_LIST_DEFAULT = DEFAULT_PATH / 'country.json'
PATH_GEOJSON = BASE_PATH / 'geojson'
PATH_GEOJSON_DEFAULT = DEFAULT_PATH / 'geojson'
PATH_GEOJSON_MARKER = BASE_PATH / 'geojson' / 'LAST_MODIFIED'
PATH_EXCEL = BASE_PATH / 'data.xlsx'
PATH_ICON = BASE_PATH / 'icon.png'
PATH_ICON_DEFAULT = APP_PATH / 'assets' / 'icon.png'