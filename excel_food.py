import openpyxl
import sqlite3

connection = sqlite3.connect('inspection_violations.db')
cursor = connection.cursor()

ViolationTypes = openpyxl.Workbook()
sheet = ViolationTypes.active
sheet.title = 'Violation Types'

sql = """
    SELECT violation_code, violation_description, COUNT(violation_code)
    FROM violations
    GROUP BY violation_code
    """

cursor.execute(sql)
violations = cursor.fetchall()  

columns = ['Code', 'Description', 'Count']
violations.insert(0, columns)
    
for row in violations:
    sheet.append(row)

ViolationTypes.save('violation_types.xlsx')