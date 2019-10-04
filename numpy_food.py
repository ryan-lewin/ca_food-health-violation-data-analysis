import numpy as np
import matplotlib.pyplot as plt
import openpyxl
import sqlite3

connection = sqlite3.connect('inspection_violations.db')
cursor = connection.cursor()

sql = """
    SELECT strftime('%m', activity_date), facility_zip, COUNT(facility_zip)
    FROM inspections as i
    WHERE i.serial_number IN (SELECT serial_number FROM violations)
    GROUP BY facility_zip
    ORDER BY COUNT(facility_zip) DESC
    """
    
monthly_data = []
months = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10','11', '12']

cursor.execute(sql)

data = cursor.fetchall()

for month in months:
    x = [d for d in data if d[0] == month]
    monthly_data.append(x)

objects = ('Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec')
y_pos = np.arange(len(objects))

highest = [x[0][2] for x in monthly_data]
plt.bar(y_pos, highest, align='center', alpha=0.5)
plt.xticks(y_pos, objects, rotation=90)
plt.ylabel('Violations')
plt.title('Highest violations by month')
plt.savefig('high.png')
plt.show()

lowest = [x[-1][2] for x in monthly_data]
plt.bar(y_pos, lowest, align='center', alpha=0.5)
plt.xticks(y_pos, objects)
plt.ylabel('Violations')
plt.title('Lowest violations by month')
plt.savefig('low.png')
plt.show()

average_monthly_violations = []

for i in range (len(months)):
    count = 0
    for row in monthly_data[i]:
        count += row[2] / len(monthly_data[i])
    average_monthly_violations.append(count)
      
plt.bar(y_pos, average_monthly_violations, align='center', alpha=0.5)
plt.xticks(y_pos, objects)
plt.ylabel('Violations')
plt.title('Average monthly violations over all postcodes')
plt.savefig('avg.png')
plt.show()

sql = """
    SELECT facility_id, facility_name, strftime('%m', activity_date), COUNT(facility_id)
    FROM inspections as i
    WHERE i.serial_number IN (SELECT serial_number FROM violations)
    AND (facility_name LIKE '%MCDONALD%' OR facility_name LIKE '%BURGER KING%')
    GROUP BY facility_id
    ORDER BY activity_date ASC
    """

cursor.execute(sql)

data = cursor.fetchall()
    
mc = [d for d in data if 'MCDONALD' in d[1]]
bk = [d for d in data if 'BURGER KING' in d[1]]

monthly_mc = []
monthly_bk = []

for month in months:
    x = [d for d in mc if d[2] == month]
    y = [d for d in bk if d[2] == month]
    monthly_mc.append(x)
    monthly_bk.append(y)

avg_mc = []
avg_bk = []

for i in range (len(months)):
    mc_count = 0
    bk_count = 0
    for row in monthly_mc[i]:
        mc_count += row[3] / len(monthly_mc[i])
    for row in monthly_bk[i]:
        bk_count += row[3] / len(monthly_bk[i])
    avg_mc.append(mc_count)
    avg_bk.append(bk_count)

x = np.arange(len(objects))
width = 0.35 
fig, ax = plt.subplots(figsize=(7, 7))
rects1 = ax.bar(x - width/2, avg_mc, width, label='MCDONALDS')
rects2 = ax.bar(x + width/2, avg_bk, width, label='BURGER KING')
plt.xticks(y_pos, objects)
plt.legend(loc='best')
plt.ylabel('Average vioaltions per store')
plt.title('MC vs BK')
plt.savefig('mcbk.png')
plt.show()