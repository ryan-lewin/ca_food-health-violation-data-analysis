import sqlite3

connection = sqlite3.connect('inspection_violations.db')
cursor = connection.cursor()

business_violations = """
                    SELECT facility_id , facility_name, facility_address, facility_city, facility_zip
                    FROM inspections
                    WHERE serial_number IN (SELECT serial_number FROM violations) 
                    GROUP BY facility_id
                    ORDER BY facility_name ASC;
                    """

cursor.execute(business_violations)
businesses = cursor.fetchall()

#for business in businesses:
    #print('\n{}, {}, {}, {}'.format(business[0], business[1], business[2], business[3]))
   
drop_pv_table = 'DROP TABLE IF EXISTS previous_violations'; 
 
create_pv_table = """
                CREATE TABLE IF NOT EXISTS previous_violations(
                facility_id VARCHAR(20) PRIMARY KEY,
                facility_name VARCHAR(50),                        
                facility_address VARCHAR(50),
                facility_city VARCHAR(20),
                facility_zip VARCHAR(10)
                );"""

cursor.execute(drop_pv_table)
cursor.execute(create_pv_table)

for business in businesses:
    insert_previous_violations = 'INSERT INTO previous_violations VALUES(?, ?, ?, ?, ?);'
    cursor.execute(insert_previous_violations, business); 
    
violation_count = """
                SELECT facility_name, COUNT(violations.id)
                FROM inspections
                LEFT OUTER JOIN violations ON inspections.serial_number = violations.serial_number
                GROUP BY facility_id
                ORDER BY facility_name ASC;
                """
cursor.execute(violation_count)

violation_count = cursor.fetchall()

for business in violation_count:
    print('\n{}, Violations: {}'.format(business[0], business[1]))

connection.commit()
connection.close()

