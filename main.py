import os
import json
import shutil
from datetime import datetime

import streamlit as st

from const.file_path import *
from const.marker_color import MARKER_COLOR_LIST
from util.gen_template import gen_template
from util.auto_download import auto_download
from util.auto_refresh import auto_refresh


############
### Init ###
############

if not os.path.exists(PATH_CONFIG):
    shutil.copy2(PATH_CONFIG_DEFAULT, PATH_CONFIG)

with open(PATH_CONFIG, 'r', encoding='utf-8') as f:
    config = json.load(f)


st.title('Admin Console')

st.set_page_config(
    page_title='Admin Console',
    page_icon=PATH_ICON if os.path.exists(PATH_ICON) else PATH_ICON_DEFAULT
)


###############
### Dataset ###
###############

st.header('Manage Dataset')

st.write('#### Template File')

col1, _ = st.columns([1, 3])

with col1:
    if st.button(
        'Download Template',
        key='btn_download_template',
        use_container_width=True
    ):
        filetype = 'application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
        base64_string = gen_template(config)
        auto_download(base64_string, 'template.xlsx', filetype)

st.write('#### Current Dataset')

if os.path.exists(PATH_EXCEL):

    mtime_excel_float = os.path.getmtime(PATH_EXCEL)
    mtime_config_datetime = datetime.fromtimestamp(mtime_excel_float)

    st.html(f'''
    <style>
        .label {{
            font-size: 1rem;
            font-weight: 400;
        }}
        .data {{
            font-size: 1rem;
            font-weight: 700;
            padding-left: .3rem;
        }}
    </style>
    <span class="label">Upload Time:</span>
    <span class="data">{mtime_config_datetime.strftime('%Y-%m-%d %H:%M:%S')}</span>
    ''')

    col1, col2, col3, _ = st.columns([1, 1, 1, 1])

    with col1:
        if st.button(
            'Validate Data',
            key='btn_validate_current',
            use_container_width=True
        ):
            pass

    with col2:
        st.download_button(
            'Download Data',
            data=open(PATH_EXCEL, 'rb').read(),
            file_name='data.xlsx',
            mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet',
            key='btn_download_current',
            use_container_width=True
        )

    with col3:
        if st.button(
            'Delete Data',
            key='btn_delete_current',
            use_container_width=True
        ):
            os.remove(PATH_EXCEL)
            st.rerun()

else:
    st.text('No dataset')

st.write('#### New Dataset')

uploaded_dataset = st.file_uploader(
    'Upload',
    type='xlsx',
    key='uploader_dataset',
    accept_multiple_files=False
)

if uploaded_dataset is not None:

    # Read file as bytes
    bytes_data = uploaded_dataset.getvalue()

    temp_excel_path = '/tmp/data.temp.xlsx' if IS_CONTAINER else BASE_PATH / 'data.temp.xlsx'

    if os.path.exists(temp_excel_path):
        os.remove(temp_excel_path)

    with open(temp_excel_path, 'wb') as f:
        f.write(bytes_data)

    col1, col2, _ = st.columns([1, 1, 2])

    with col1:
        if st.button(
            'Validate Data',
            key='btn_validate_new',
            use_container_width=True
        ):
            pass

    with col2:
        if st.button(
            'Apply Changes',
            key='btn_apply_new',
            use_container_width=True
        ):
            shutil.move(temp_excel_path, PATH_EXCEL)
            auto_refresh()


##############
### Config ###
##############

st.header('Manage Config')

input_app_name = st.text_input(
    'App Name',
    key='input_app_name',
    value=config['app']['title']
)

st.write('#### Sheet Names')

input_sheet_name_region = st.text_input(
    'Region Sheet Name',
    key='input_sheet_name_region',
    value=config['source']['sheet']['region']['name']
)

input_sheet_name_dealer = st.text_input(
    'Dealer Sheet Name',
    key='input_sheet_name_dealer',
    value=config['source']['sheet']['dealer']['name']
)

input_sheet_name_dealer_customer = st.text_input(
    'Dealer Customer Sheet Name',
    key='input_sheet_name_dealer_customer',
    value=config['source']['sheet']['dealerCustomer']['name']
)

input_sheet_name_key_account = st.text_input(
    'Key Account Sheet Name',
    key='input_sheet_name_key_account',
    value=config['source']['sheet']['keyAccount']['name']
)

input_sheet_name_priority_target = st.text_input(
    'Priority Target Name',
    key='input_sheet_name_priority_target',
    value=config['source']['sheet']['priorityTarget']['name']
)

st.write('#### Optional Data Display')

is_show_projected_revenue = st.selectbox(
    'Projected Revenue',
    key='is_show_projected_revenue',
    options=[
        {'name': 'Show', 'value': True},
        {'name': 'Hide', 'value': False}
    ],
    format_func=lambda x: x['name'],
    index=(0 if config['showOptionalData']['projectedRevenue'] else 1)
)

st.write('#### Pin Colors')

current_color_priority_target_customer = 'beige'
current_color_priority_target_non_customer = 'beige'

for item in config['isCustomer']:
    if item['value']:
        current_color_priority_target_customer = item['color']
    else:
        current_color_priority_target_non_customer = item['color']

pin_color_priority_target_customer = st.selectbox(
    'Customer (Priority Target)',
    key='pin_color_priority_target_customer',
    options=MARKER_COLOR_LIST,
    index=MARKER_COLOR_LIST.index(current_color_priority_target_customer)
)

pin_color_priority_target_non_customer = st.selectbox(
    'Non-Customer (Priority Target)',
    key='pin_color_priority_target_non_customer',
    options=MARKER_COLOR_LIST,
    index=MARKER_COLOR_LIST.index(current_color_priority_target_non_customer)
)

pin_color_key_account = st.selectbox(
    'Key Account',
    key='pin_color_key_account',
    options=MARKER_COLOR_LIST,
    index=MARKER_COLOR_LIST.index(config['keyAccountColor'])
)

st.write('#### Miscellaneous')

input_app_note = st.text_area(
    'App Note',
    key='input_app_note',
    value=config['appMemo'],
)

col1, _ = st.columns([1, 3])

with col1:
    if st.button(
        'Apply Config',
        key='btn_apply_config',
        use_container_width=True
    ):
        # App Name
        config['app']['title'] = input_app_name

        # Sheet Names
        config['source']['sheet']['region']['name'] = input_sheet_name_region
        config['source']['sheet']['dealer']['name'] = input_sheet_name_dealer
        config['source']['sheet']['dealerCustomer']['name'] = input_sheet_name_dealer_customer
        config['source']['sheet']['keyAccount']['name'] = input_sheet_name_key_account
        config['source']['sheet']['priorityTarget']['name'] = input_sheet_name_priority_target

        # Optional Data Display
        config['showOptionalData']['projectedRevenue'] = is_show_projected_revenue['value']

        # Pin Colors
        config['isCustomer'] = [
            {'value': True, 'color': pin_color_priority_target_customer},
            {'value': False, 'color': pin_color_priority_target_non_customer}
        ]
        config['keyAccountColor'] = pin_color_key_account

        # Miscellaneous
        config['appMemo'] = input_app_note

        config_json = json.dumps(config, ensure_ascii=False)

        with open(PATH_CONFIG, 'w', encoding='utf-8') as f:
            f.write(config_json)
            auto_refresh()

st.divider()

st.write('#### App Icon')

if os.path.exists(PATH_ICON):

    st.text('Current Icon:')

    st.image(
        PATH_ICON,
        width=100
    )

    col1, _ = st.columns([1, 3])

    with col1:
        if st.button(
            'Delete Icon',
            key='btn_delete_icon',
            use_container_width=True
        ):
            os.remove(PATH_ICON)
            st.rerun()

uploaded_icon = st.file_uploader(
    'Upload',
    type='png',
    key='uploader_icon',
    accept_multiple_files=False,
)

if uploaded_icon is not None:

    # Read file as bytes
    bytes_data = uploaded_icon.getvalue()

    temp_icon_path = '/tmp/icon.temp.png' if IS_CONTAINER else BASE_PATH / 'icon.temp.png'

    if os.path.exists(temp_icon_path):
        os.remove(temp_icon_path)

    with open(temp_icon_path, 'wb') as f:
        f.write(bytes_data)

    col1, _ = st.columns([1, 3])

    with col1:
        if st.button(
            'Apply Changes',
            key='btn_apply_icon',
            use_container_width=True
        ):
            shutil.move(temp_icon_path, PATH_ICON)
            auto_refresh()

st.write('#### Edit List')

col1, col2, _ = st.columns([1, 1, 2])

with col1:
    if st.button(
        'Edit Vertical List',
        key='btn_edit_vertical',
        use_container_width=True
    ):
        pass

with col2:
    if st.button(
        'Edit Tier List',
        key='btn_edit_tier',
        use_container_width=True
    ):
        pass