import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv(r"C:\dev\Virtual-Telemetry-Software\telem3.csv")
#df = df.dropna(axis=1, how='all')

print(df.columns)

'''df["SuspensionTravelMetersFrontLeft"] = df["SuspensionTravelMetersFrontLeft"]/10000 
df["SuspensionTravelMetersFrontRight"] = df["SuspensionTravelMetersFrontRight"]/10000 
df["SuspensionTravelMetersRearLeft"] = df["SuspensionTravelMetersRearLeft"]/10000 
df["SuspensionTravelMetersRearRight"] = df["SuspensionTravelMetersRearRight"]/10000 
'''
fig, axs = plt.subplots(2,2, figsize=(16, 8))

axs[0,0].plot(df["TimestampMS"],df["SuspensionTravelMetersFrontLeft"])
axs[0,0].set_yscale('log') 
axs[0,0].set_title('SuspensionTravelMetersFrontLeft')
axs[0,0].set_ylabel('Compression[m]')
axs[0,0].set_xlabel('Time [ms]')

axs[0,1].plot(df["TimestampMS"],df["SuspensionTravelMetersFrontRight"])
axs[0,1].set_yscale('log')
axs[0,1].set_title('SuspensionTravelMetersFrontRight')
axs[0,1].set_ylabel('Compression[m]')
axs[0,1].set_xlabel('Time [ms]')

axs[1,0].plot(df["TimestampMS"],df["SuspensionTravelMetersRearLeft"])
axs[1,0].set_yscale('log')
axs[1,0].set_title('SuspensionTravelMetersRearLeft')
axs[1,0].set_ylabel('Compression[m]')
axs[1,0].set_xlabel('Time [ms]')

axs[1,1].plot(df["TimestampMS"],df["SuspensionTravelMetersRearRight"])
axs[1,1].set_yscale('log')
axs[1,1].set_title('SuspensionTravelMetersRearRight')
axs[1,1].set_ylabel('Compression[m]')
axs[1,1].set_xlabel('Time [ms]')

fig1, axs1 = plt.subplots(2,2, figsize=(16, 8))

axs1[0,0].plot(df["TimestampMS"],df["Brake"])
axs1[0,0].set_title('Brake')
axs1[0,0].set_ylabel('[N]')
axs1[0,0].set_xlabel('Time [ms]')

axs1[0,1].plot(df["TimestampMS"],df["Speed"])
axs1[0,1].set_title('Speed')
axs1[0,1].set_ylabel('m/s')
axs1[0,1].set_xlabel('Time [ms]')

axs1[1,0].plot(df["TimestampMS"],df["Accelerator"])
axs1[1,0].set_title('Accelerator')
axs1[1,0].set_ylabel('Value')
axs1[1,0].set_xlabel('Time [ms]')

axs1[1,1].plot(df["TimestampMS"],df["Torque"])
axs1[1,1].set_title('Torque')
axs1[1,1].set_ylabel('Nm')
axs1[1,1].set_xlabel('Time [ms]')

plt.plot()
plt.show()

plt.plot(df["PositionX"], df["PositionY"])
plt.show()



