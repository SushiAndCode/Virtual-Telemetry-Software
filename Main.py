import pandas as pd
import Model.Laps as lp

df = pd.read_csv(r"C:\data\logForzaMotor\telem5.csv")
giri = lp.Laps(df)

print(giri.laps)