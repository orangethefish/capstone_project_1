import csv
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
idle_threshold = 0 # threshold for detecting idle 

rows = []
with open('O.csv') as f:
    reader = csv.reader(f)
    for row in reader:
        rows.append(row)

edited_rows = [rows[0]] 

for i in range(2, len(rows)):
    idle = False
    if (abs(float(rows[i][3])) < idle_threshold): 
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



##plottt

df = pd.read_csv('edited_data.csv')
df.to_csv('edited_data.csv', index=False)

time=[]
x = []
y = []
z = []
with open('edited_data.csv') as f:
    reader = csv.reader(f)
    next(reader)
    time_stamp = 0
    for row in reader:
        time.append(time_stamp)
        time_stamp += 20
        x.append(float(row[3])) 
        y.append(float(row[4]))
        z.append(float(row[5]))
fig, ax = plt.subplots()
ax.set_xlabel('Time (ms)')
ax.set_ylabel('Acceleration (m/s^2)')
# ax.grid(True)
# time = time[:500]
# x = x[:500]
# y = y[:500]
# z = z[:500]
dxdt = np.diff(x) / np.diff(time)
dxdt = dxdt[:500]
# ax.plot(time, x, label='X')
# ax.plot(time, y, label='Y')
# ax.plot(time, z, label='Z')
# ax.legend()
ax.plot(time[:500], dxdt, label='Derivative of x')
ax.legend()

plt.show()