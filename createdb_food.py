import sqlite3
import openpyxl

wb1 = openpyxl.load_workbook('inspections.xlsx', read_only=True)
wb2 = openpyxl.load_workbook('violations.xlsx', read_only=True)

inspections = wb1['inspections']
violations = wb2['violations']

connection = sqlite3.connect('inspection_violations.db')
cursor = connection.cursor()    

drop_inspections = 'DROP TABLE IF EXISTS inspections';
drop_violations = 'DROP TABLE IF EXISTS violations';

create_inspections_table = """
                        CREATE TABLE inspections(
                        activity_date DATE,
                        employee_id VARCHAR(20),
                        facility_address VARCHAR(50),
                        facility_city VARCHAR(20),
                        facility_id VARCHAR(20),
                        facility_name VARCHAR(50),
                        facility_state VARCHAR(6),
                        facility_zip VARCHAR(10),
                        grade CHAR(1),
                        owner_id VARCHAR(20),
                        owner_name VARCHAR(50),
                        pe_description VARCHAR(50),
                        program_element_pe CHAR(4),
                        program_name VARCHAR(50),
                        program_status VARCHAR(10),
                        record_id CHAR(9),
                        score VARCHAR(3),
                        serial_number VARCHAR(10),
                        service_code VARCHAR(3),
                        service_description VARCHAR(20),
                        PRIMARY KEY(serial_number)
                        );"""

create_violations_table = """
                        CREATE TABLE violations(
                        id INTEGER PRIMARY KEY AUTOINCREMENT,
                        points VARCHAR(2),
                        serial_number VARCHAR(10),
                        violation_code VARCHAR(10),
                        violation_description VARCHAR(50),
                        violation_status VARCHAR(30),
                        FOREIGN KEY (serial_number) REFERENCES inspections(serial_number)
                        );"""
cursor.execute(drop_inspections)
cursor.execute(drop_violations)
cursor.execute(create_inspections_table)
cursor.execute(create_violations_table)

inspection_data = tuple(inspections.rows)
violation_data = tuple(violations.rows)

for row in inspection_data[1:]:
    insert_inspections = 'INSERT INTO inspections VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);' 
    cursor.execute(insert_inspections, (row[0].value, row[1].value, row[2].value, row[3].value, row[4].value,row[5].value,row[6].value, row[7].value, row[8].value, row[9].value, row[10].value,row[11].value, row[12].value, row[13].value, row[14].value, row[15].value, row[16].value, row[17].value, row[18].value, row[19].value));
  
for row in violation_data[1:]:
    insert_violations = 'INSERT INTO violations VALUES(NULL, ?, ?, ?, ?, ?);'
    cursor.execute(insert_violations, (row[0].value, row[1].value, row[2].value, row[3].value, row[4].value));  
    
connection.commit()
connection.close()

    
    
