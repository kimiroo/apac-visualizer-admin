import os
import shutil
import json
from datetime import datetime

import streamlit as st
from bs4 import BeautifulSoup
import requests

from const.file_path import *


@st.cache_data(ttl=3600 * 24)
def get_latest_country_list():
    """
    Fetch the list of countries from GADM website.
    This function is cached to prevent redundant network requests.
    """
    latest_country_list = []
    resp = requests.get('https://gadm.org/download_country.html')
    soup = BeautifulSoup(resp.text, 'html.parser')

    for choice in soup.select('#countrySelect option'):
        value = choice.get('value').split('_')
        if len(value) != 3:
            continue

        country_id = value[0]
        country_name = value[1]
        max_level = int(value[-1])
        level = 1 if max_level > 1 else 0

        latest_country_list.append({
            'id': country_id,
            'name': country_name,
            'level': level
        })
    return latest_country_list

@st.dialog('Download GeoJSON')
def dialog_geojson():

    if not os.path.exists(PATH_COUNTRY_LIST):
        shutil.copy2(PATH_COUNTRY_LIST_DEFAULT, PATH_COUNTRY_LIST)

    with open(PATH_COUNTRY_LIST, 'r', encoding='utf-8') as f:
        last_country_list = json.load(f)

    latest_country_list = get_latest_country_list()

    st.write('#### Select countries to download')

    selected_country = {}

    for country in latest_country_list:
        selected_country[country['id']] = st.checkbox(
            country['name'],
            key=f'select_{country['id']}',
            value=(country['id'] in last_country_list)
        )

    is_downloading = False

    if st.button(
        'Download',
        key='btn_download_geojson',
        use_container_width=True,
        disabled=is_downloading
    ):
        is_downloading = True

        tmp_geojson_path = '/tmp/geojson' if IS_CONTAINER else './tmp_geojson'
        old_geojson_path = BASE_PATH / 'geojson.old'

        with st.spinner('Downloading GeoJSON...'):

            if os.path.exists(tmp_geojson_path):
                shutil.rmtree(tmp_geojson_path)

            os.makedirs(tmp_geojson_path, exist_ok=True)

            for country_id, is_selected in selected_country.items():

                if not is_selected:
                    continue

                country_obj = next((c for c in latest_country_list if c['id'] == country_id), None)

                if not country_obj:
                    continue

                target_level = country_obj['level']
                url = f'https://geodata.ucdavis.edu/gadm/gadm4.1/json/gadm41_{country_id}_{target_level}.json'
                resp = requests.get(url)

                with open(f'{tmp_geojson_path}/{country_id}_{target_level}.json', 'w') as f:
                    f.write(resp.text)

            selected_country_json = [
                country_id for country_id, is_selected in selected_country.items() if is_selected
            ]

            if os.path.exists(PATH_GEOJSON):
                shutil.move(PATH_GEOJSON, old_geojson_path)
            shutil.move(tmp_geojson_path, PATH_GEOJSON)
            if os.path.exists(old_geojson_path):
                shutil.rmtree(old_geojson_path)

            with open(PATH_COUNTRY_LIST, 'w', encoding='utf-8') as f:
                f.write(json.dumps(selected_country_json))

            with open(PATH_GEOJSON_MARKER, 'w', encoding='utf-8') as f:
                f.write(datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

        is_downloading = False

        st.success('GeoJSON Downloaded. You may now close this dialog.')
