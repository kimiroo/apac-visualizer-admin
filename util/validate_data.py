from openpyxl import Workbook

from util.validate.region import check_region_sheet

def validate_data(doc:Workbook, config: dict) -> list:

    error_list = [] # {'level': level, 'sheet': sheet, 'cell': cell, 'message': message}

    sheet_names = [
        config['source']['sheet']['region']['name'],
        config['source']['sheet']['dealer']['name'],
        config['source']['sheet']['dealerCustomer']['name'],
        config['source']['sheet']['keyAccount']['name'],
        config['source']['sheet']['priorityTarget']['name']
    ]

    ##############
    ### Region ###
    ##############

    sheet_name = config['source']['sheet']['region']['name']
    if not sheet_name in doc.sheetnames:
        error_list.append({
            'level': 'CRITICAL',
            'sheet': '-',
            'cell': '-',
            'message': f'Required sheet "{sheet_name}" not found in the workbook. Ensure the sheet name matches the configuration.'
        })
    else:
        sheet = doc[sheet_name]

        result_region = check_region_sheet(sheet, config)

        error_list = error_list + result_region

    return error_list