import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv(r"C:\data\LogMoto\E23_CREMONA_20241023_Turno1\E23_CREMONA_20241023_Turno1.csv")

fig, axs = plt.subplots(2,2, figsize=(16, 8))

df['timestamps'] = pd.to_numeric(df['timestamps'], errors='coerce')

df['tps_lv'] = pd.to_numeric(df['tps_lv'], errors='coerce')
axs[0,0].plot(df["timestamps"],df["tps_lv"])
axs[0,0].set_title('tps_lv')
axs[0,0].set_ylabel('Tps Value')
axs[0,0].set_xlabel('Time [ms]')

df['brake_a'] = pd.to_numeric(df['brake_a'], errors='coerce')
axs[0,1].plot(df["timestamps"],df["brake_a"])
axs[0,1].set_title('brake_a')
axs[0,1].set_ylabel('m/s')
axs[0,1].set_xlabel('Time [ms]')

df['INV_Motor_Current'] = pd.to_numeric(df['INV_Motor_Current'], errors='coerce')
axs[1,0].plot(df["timestamps"],df["INV_Motor_Current"])
axs[1,0].set_title('INV_Motor_Current')
axs[1,0].set_ylabel('Ampere')
axs[1,0].set_xlabel('Time [ms]')

df['INV_Torque'] = pd.to_numeric(df['INV_Torque'], errors='coerce')
axs[1,1].plot(df["timestamps"],df["INV_Torque"])
axs[1,1].set_title('INV_Torque')
axs[1,1].set_ylabel('Nm')
axs[1,1].set_xlabel('Time [ms]')

plt.plot()
plt.show()