import pandas as pd
from openpyxl import load_workbook

file = "Data.xlsx"
wb = load_workbook(file)

constants = {
    '3d85c6': 'Very Good',
    '7eaeda': 'Good',
    'bfd7ed': 'Ok',
    'ffffff': 'Average',
    'ffaaaa': 'Poor',
    'ff5555': 'Bad',
    'ff0000': 'Very Bad'

}

sheet_names = wb.sheetnames[3:len(wb.sheetnames)-1]

sheet = wb.active

def get_cell_fill_color(cell):
    return cell.fill.start_color.index

limiter = 1

for sheet_name in sheet_names:
    data = pd.read_excel(file, sheet_name=sheet_name, engine='openpyxl')
    for row in sheet.iter_rows():
        for cell in row:
            print(cell.fill)
            limiter += 1
            if limiter > 10:
                break
        if limiter > 10:
            break
    if limiter > 10:
        break
