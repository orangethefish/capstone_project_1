import math
import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

pi = math.pi
g_value = 9.80665
RAD_TO_DEG = 57.2957795131
COMPLE_ALPHA = 0.05

class RCFilter:
    def __init__(self, cutoffFreqHz, sampleTimeS):
        # Compute equivalent 'RC' constant from cut-off frequency
        RC = 1.0 / (pi * 2 * cutoffFreqHz)

        # Pre-compute filter coefficients for the first-order low-pass filter
        self.coeff = [sampleTimeS / (sampleTimeS + RC), RC / (sampleTimeS + RC)]

        # Clear output buffer
        self.out = [0.0, 0.0]

    def update(self, inp):
        # Shift output samples
        self.out[1] = self.out[0]

        # Compute new output sample
        self.out[0] = self.coeff[0] * inp + self.coeff[1] * self.out[1]

        # Return filtered sample
        return self.out[0]


# Load the CSV file
file_path = "sensor_data.csv"  # Replace with the actual file path
data = pd.read_csv(file_path)
time = range(len(data))


# Initialise roll and pitch for complementary filter
roll = 0.0
pitch = 0.0

# Initialise input
input_acce = [data['Accelerometer X (g)'].values,
              data['Accelerometer Y (g)'].values,
              data['Accelerometer Z (g)'].values]
input_gyro = [data['Gyroscope X (rad/s)'].values,
              data['Gyroscope Y (rad/s)'].values,
              data['Gyroscope Z (rad/s)'].values]


# Initialise low-pass filters
lpfAcc = [RCFilter(5.0, 0.01) for _ in range(3)]
lpfGyr = [RCFilter(25.0, 0.01) for _ in range(3)]


# Filter accelerometer data
filtered_acc_x = lpfAcc[0].update(input_acce[0])
filtered_acc_y = lpfAcc[1].update(input_acce[1])
filtered_acc_z = lpfAcc[2].update(input_acce[2])


# Filter gyroscope data
filtered_gyr_x = lpfGyr[0].update(input_gyro[0])
filtered_gyr_y = lpfGyr[1].update(input_gyro[1])
filtered_gyr_z = lpfGyr[2].update(input_gyro[2])


# Calculate pitch and roll angles using accelerometer data
roll_acc = np.arctan2(filtered_acc_y, filtered_acc_z)*RAD_TO_DEG
pitch_acc = np.arcsin(filtered_acc_x / g_value)*RAD_TO_DEG
# No filter
# roll_acc = np.arctan(filtered_acc_y / filtered_acc_z)*RAD_TO_DEG
# pitch_acc = np.arcsin(filtered_acc_x / g_value)*RAD_TO_DEG

roll_gyr = filtered_gyr_x + np.tan(pitch) * (np.sin(roll) * filtered_gyr_y + np.cos(roll) * filtered_gyr_z)
pitch_gyr = np.cos(roll) * filtered_gyr_y - np.sin(roll) * filtered_gyr_z

roll = (COMPLE_ALPHA * roll_acc + (1.0 - COMPLE_ALPHA) * (roll + 0.01 * roll_gyr)) * RAD_TO_DEG
pitch = (COMPLE_ALPHA * pitch_acc + (1.0 - COMPLE_ALPHA) * (pitch + 0.01 * pitch_gyr)) * RAD_TO_DEG



# Create subplots for roll and pitch
plt.figure(figsize=(12, 6))
plt.subplot(2, 1, 1)
plt.plot(time, roll, label='Roll (degrees)')
plt.title('Roll Angle')
plt.xlabel('Time')
plt.ylabel('Degrees')
plt.legend()

plt.subplot(2, 1, 2)
plt.plot(time, pitch, label='Pitch (degrees)')
plt.title('Pitch Angle')
plt.xlabel('Time')
plt.ylabel('Degrees')
plt.legend()

plt.tight_layout()
plt.show()


# See PyCharm help at https://www.jetbrains.com/help/pycharm/
