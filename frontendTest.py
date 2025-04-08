import pandas as pd
import numpy as np
import dearpygui.dearpygui as dpg

# DearPyGui setup
dpg.create_context()

def ms_to_mmss(ms):
    seconds = ms // 1000
    minutes = seconds // 60
    sec = seconds % 60
    return f"{int(minutes):02}:{int(sec):02}"

df = pd.read_csv(r"C:\dev\Virtual-Telemetry-Software\telem3.csv")

df["TimestampMS"] = pd.to_numeric(df["TimestampMS"], errors="coerce")
df["TimestampMS"] = df["TimestampMS"] - min(df["TimestampMS"])
df.dropna(subset=["TimestampMS"], inplace=True)
df["Gear"] = df["Gear"].apply(lambda x: np.nan if x > 6 else x)

min_x = int(df["TimestampMS"].min())
max_x = int(df["TimestampMS"].max())

tick_interval = 30000 
custom_ticks = list(range(min_x, max_x + 1, tick_interval))
tick_labels = [ms_to_mmss(ms) for ms in custom_ticks]
ticks = tuple(zip(tick_labels, custom_ticks))

with dpg.window(label="Signal Viewer",width=1000, height=600):
    
    dpg.add_text("Jijjino")

    def toggle_line_series(sender, app_data, user_data):
        if dpg.is_item_shown(user_data):
            dpg.hide_item(user_data)
        else:
            dpg.show_item(user_data)

    with dpg.menu_bar():

        with dpg.menu(label="Channels"):
            for tag in df.columns:
                if tag != "TimestampMS":
                    dpg.add_menu_item(label = tag,callback=toggle_line_series, user_data=tag)

    with dpg.plot(label="Main Plot",height=-1, width=-1):
        dpg.add_plot_legend()
        dpg.add_plot_axis(dpg.mvXAxis, label="TimestampMS", tag="main_x_axis")
        dpg.set_axis_ticks("main_x_axis", ticks)
        with dpg.plot_axis(dpg.mvYAxis, label="Amplitude"):
            for channel in df.columns:
                if channel != "TimestampMS":
                    dpg.add_line_series(df["TimestampMS"].to_list(), df[channel].to_list(),label = channel ,tag=channel)
                    dpg.hide_item(channel)
    

if __name__ == "__main__":
    dpg.create_viewport(title='Custom Title', width=800, height=600)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
