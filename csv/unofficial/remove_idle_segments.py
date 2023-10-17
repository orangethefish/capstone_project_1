import csv
import pandas as pd
import matplotlib.pyplot as plt
idle_threshold = 2 # threshold for detecting idle 

rows = []
with open('O.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        rows.append(row)

edited_rows = [rows[0]] 

for i in range(2, len(rows)):
    idle = False
    if abs(float(rows[i][0])) < idle_threshold: 
        idle = True
    if idle:
        if i == len(rows) - 1:
            edited_rows.append(rows[i])
        continue
    edited_rows.append(rows[i])
        
with open('edited_data.csv', 'w') as f:
    writer = csv.writer(f)
    for row in edited_rows:
        writer.writerow(row)
df = pd.read_csv('edited_data.csv')
df.to_csv('edited_data.csv', index=False)

time=0
x = []
y = []
z = []
with open('edited_data.csv') as f:
    reader = csv.reader(f)
    next(reader)
    for row in reader:
        x.append(float(row[0])) 
        y.append(float(row[1]))
        z.append(float(row[2]))
plt.plot(x, y)
plt.xlabel('X') 
plt.ylabel('Y')
plt.title('Data Plot')
plt.grid()
plt.show()