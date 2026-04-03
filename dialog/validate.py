from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from openpyxl.workbook.workbook import _WorksheetOrChartsheetLike

import streamlit as st
import pandas as pd

from const.file_path import *
from util.validate_data import validate_data

@st.dialog('Data Validation', width='large')
def dialog_validate(doc: _WorksheetOrChartsheetLike, config: dict):

    with st.spinner('Validating spreadsheet data...'):
        result = validate_data(doc, config)
        df = pd.DataFrame(result)

    if not df.empty:
        st.dataframe(
            df,
            key='table_validation_error',
            hide_index=True,
            width='stretch',
            height='auto',
            column_config={
                'level': st.column_config.TextColumn('Error Level'),
                'sheet': st.column_config.TextColumn('Sheet Name'),
                'cell': st.column_config.TextColumn('Cell'),
                'message': st.column_config.TextColumn('Error Message', width=1600)
            }
        )

        with st.expander("📝 Data Validation Legend", expanded=True):
            st.markdown("""
                - **🚫 CRITICAL**: Validation failed. The app **will fail to run** with these errors.
                - **❌ ERROR**: Data mapping issues. Some records **might be missing or incomplete**.
                - **⚠️ WARNING**: Minor inconsistencies detected. These will be **auto-corrected** or ignored.
            """)

    else:
        st.success('Validation complete. All records passed the consistency check.')