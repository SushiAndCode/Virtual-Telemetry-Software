import pandas as pd
import numpy as np

def ms_to_mmss(ms):
    seconds = ms // 1000
    minutes = seconds // 60
    sec = seconds % 60
    return f"{int(minutes):02}:{int(sec):02}"


class Laps():
    def __init__(self,df=pd.DataFrame):
        self.df = df
        self.laps = {lap: group.reset_index(drop=True) for lap, group in self.df.groupby('Lap')}

    def getCustomTimeUnits(self, tick_interval):

        self.df["TimestampMS"] = pd.to_numeric(self.dfdf["TimestampMS"], errors="coerce")
        self.df["TimestampMS"] = self.df["TimestampMS"] - min(self.df["TimestampMS"])
        self.df.dropna(subset=["TimestampMS"], inplace=True)
        self.df["Gear"] = self.df["Gear"].apply(lambda x: np.nan if x == 11 else x)

        min_x = int(self.df["TimestampMS"].min())
        max_x = int(self.df["TimestampMS"].max())

        custom_ticks = list(range(min_x, max_x + 1, tick_interval))
        tick_labels = [ms_to_mmss(ms) for ms in custom_ticks]
        self.ticks = tuple(zip(tick_labels, custom_ticks))


