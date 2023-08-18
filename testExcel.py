# from openpyxl import Workbook, load_workbook
# wb = load_workbook('test.xlsx')
# ws = wb.active
# print(ws)
# ws['A1'].value = "test"

# wb.save('test.xlsx')



import pandas as pd
df = pd.read_csv("data/data.csv")
print(df)