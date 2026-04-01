from pathlib import Path

from util.is_container import IS_CONTAINER

BASE_PATH = Path('/data') if IS_CONTAINER else Path('.')

PATH_CONFIG = BASE_PATH / 'config.json'
PATH_COUNTRY_LIST = BASE_PATH / 'country.json'
PATH_GEOJSON = BASE_PATH / 'geojson'
PATH_EXCEL = BASE_PATH / 'data.xlsx'
PATH_ICON = BASE_PATH / 'icon.png'