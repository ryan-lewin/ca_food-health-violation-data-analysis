import sqlite3

connection = sqlite3.connect('inspection_violations.db')
cursor = connection.cursor()

business_violations = """
                    SELECT DISTINCT facility_name, facility_address, facility_city, facility_zip facility_id FROM inspections 
                    WHERE serial_number IN (SELECT serial_number FROM violations) 
                    ORDER BY facility_name DESC;
                    """

cursor.execute(business_violations)
businesses = cursor.fetchall()

for business in businesses:
    print('\n{}, {}, {}, {}'.format(business[0], business[1], business[2], business[3]))
    
create_pv_table = """
                CREATE TABLE IF NOT EXISTS previous_violations(
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                facility_name VARCHAR(50),                        
                facility_address VARCHAR(50),
                facility_city VARCHAR(20),
                facility_zip VARCHAR(10)
                );"""

cursor.execute(create_pv_table)

for business in businesses:
    insert_previous_violations = 'INSERT INTO previous_violations VALUES(NULL, ?, ?, ?, ?);'
    cursor.execute(insert_previous_violations, business); 

connection.commit()
connection.close()

