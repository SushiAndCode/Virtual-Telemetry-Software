import dearpygui.dearpygui as dpg
import numpy as np
import pandas as pd

dpg.create_context()

def ms_to_mmss(ms):
    seconds = ms // 1000
    minutes = seconds // 60
    sec = seconds % 60
    return f"{int(minutes):02}:{int(sec):02}"

# Load and sanitize the data
df = pd.read_csv(r"C:\dev\Virtual-Telemetry-Software\telem3.csv")

# Ensure TimestampMS is numeric
df["TimestampMS"] = pd.to_numeric(df["TimestampMS"], errors="coerce")
df.dropna(subset=["TimestampMS"], inplace=True)
df["Gear"] = df["Gear"].apply(lambda x: np.nan if x > 6 else x)

# Get range from your data
min_x = int(df["TimestampMS"].min())
max_x = int(df["TimestampMS"].max())

# Create ticks every 30 seconds
tick_interval = 30000  # in milliseconds
custom_ticks = list(range(min_x, max_x + 1, tick_interval))
tick_labels = [ms_to_mmss(ms) for ms in custom_ticks]
ticks = tuple(zip(tick_labels, custom_ticks))


with dpg.window(label="Tutorial", width=400, height=400):
    # create plot
    dpg.add_text("Right click a series in the legend!")
    with dpg.plot(label="Line Series", height=-1, width=-1):
        dpg.add_plot_legend()

        dpg.add_plot_axis(dpg.mvXAxis, label="x")
        dpg.add_plot_axis(dpg.mvYAxis, label="y", tag="yaxis")

        # series 1
        dpg.add_line_series(df["TimestampMS"].to_list(), df["Gear"].to_list(), label="Gear", parent="yaxis", tag="GearTag")
        dpg.add_button(label="Delete Gear", parent=dpg.last_item(), callback=lambda: dpg.delete_item("Gear"))

        # series 2
        dpg.add_line_series(df["TimestampMS"].to_list(), df["Torque"].to_list(), label="Torque", parent="yaxis", tag="TorqueTag")
        dpg.add_button(label="Delete Torque", parent=dpg.last_item(), callback=lambda: dpg.delete_item("Torque"))

        dpg.add_line_series(df["TimestampMS"].to_list(), df["CurrentEngineRpm"].to_list(), label="CurrentEngineRpm", parent="yaxis", tag="CurrentEngineRpmTag")
        dpg.add_button(label="Delete CurrentEngineRpm", parent=dpg.last_item(), callback=lambda: dpg.delete_item("CurrentEngineRpm"))

dpg.create_viewport(title='Custom Title', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()