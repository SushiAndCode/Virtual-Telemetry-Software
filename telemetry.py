import matplotlib.pyplot as plt
import pandas as pd
import numpy as np

df = pd.read_csv(r"C:\dev\Virtual-Telemetry-Software\telem3.csv")
#df = df.dropna(axis=1, how='all')

print(df.columns)

df["Gear"] = df["Gear"].apply(lambda x: np.nan if x > 6 else x)

fig1, axs1 = plt.subplots(1,figsize=(16, 8))

axs1.plot(df["TimestampMS"],df["Gear"], label='Gear')
axs1.plot(df["TimestampMS"],df["Torque"]/max(df["Torque"]), label='Torque')
axs1.plot(df["TimestampMS"],df["CurrentEngineRpm"]/max(df["CurrentEngineRpm"]), label='CurrentEngineRpm')
axs1.set_title('Torque - RPM')
axs1.set_ylabel('Comparison')
axs1.set_xlabel('Time [ms]')
axs1.legend()

plt.show()
plt.plot()

fig, axs = plt.subplots(2,2, figsize=(16, 8))

axs[0,0].plot(df["TimestampMS"],df["SuspensionTravelMetersFrontLeft"])
axs[0,0].set_title('SuspensionTravelMetersFrontLeft')
axs[0,0].set_ylabel('Compression[m]')
axs[0,0].set_xlabel('Time [ms]')

axs[0,1].plot(df["TimestampMS"],df["SuspensionTravelMetersFrontRight"])
axs[0,1].set_title('SuspensionTravelMetersFrontRight')
axs[0,1].set_ylabel('Compression[m]')
axs[0,1].set_xlabel('Time [ms]')

axs[1,0].plot(df["TimestampMS"],df["SuspensionTravelMetersRearLeft"])
axs[1,0].set_title('SuspensionTravelMetersRearLeft')
axs[1,0].set_ylabel('Compression[m]')
axs[1,0].set_xlabel('Time [ms]')

axs[1,1].plot(df["TimestampMS"],df["SuspensionTravelMetersRearRight"])
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

axs1[1,0].plot(df["TimestampMS"],df["Torque"], label='Torque')
axs1[1,0].plot(df["TimestampMS"],df["CurrentEngineRpm"], label='CurrentEngineRpm')
axs1[1,0].set_title('Torque - RPM')
axs1[1,0].set_ylabel('Comparison')
axs1[1,0].set_xlabel('Time [ms]')
axs1[1,0].legend()


plt.plot()
plt.show()

plt.plot(df["PositionX"], df["PositionY"])
plt.show()

plt.plot(df["TimestampMS"], df["Gear"])
plt.show()



