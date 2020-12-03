import xlwings as xw
file_path = '湖北_1_10月-移动个人-1.xlsx'
sheet_name = '整理后'
app = xw.App(visible = True, add_book = False)
workbook = app.books.open(file_path)
worksheet = workbook.sheets[sheet_name]
value = worksheet.range('A2').expand('table').value
data = dict()
for i in range(len(value)):
    product_name = value[i][3]
    if product_name not in data:
        data[product_name] = []
    data[product_name].append(value[i])
for key,value in data.items():
    new_workbook = xw.books.add()
    new_worksheet = new_workbook.sheets.add(key)
    new_worksheet['A1'].value = worksheet['A1:O1'].value#获取表头
    new_worksheet['A2'].value = value
    new_workbook.save('{}.xlsx'.format(key))
app.quit()