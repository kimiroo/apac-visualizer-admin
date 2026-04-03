from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from openpyxl.workbook.workbook import _WorksheetOrChartsheetLike

import streamlit as st

from const.file_path import *
from util.validate_data import validate_data

@st.dialog('Data Validation')
def dialog_validate(doc: _WorksheetOrChartsheetLike, config: dict):
    result = validate_data(doc, config)

    print(result)