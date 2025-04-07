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
df.dropna(subset=["TimestampMS"], inplace=True)
df["Gear"] = df["Gear"].apply(lambda x: np.nan if x > 6 else x)

min_x = int(df["TimestampMS"].min())
max_x = int(df["TimestampMS"].max())

tick_interval = 30000 
custom_ticks = list(range(min_x, max_x + 1, tick_interval))
tick_labels = [ms_to_mmss(ms) for ms in custom_ticks]
ticks = tuple(zip(tick_labels, custom_ticks))

def on_drag_rect(sender, app_data, user_data):
    
    app_data = list(app_data)

    print(app_data[0][0])
    print(app_data[0][1])
    print(app_data[0][2])
    print(app_data[0][3])
    zoomed_df = df[(df["TimestampMS"] >= app_data[0][1]) & (df["TimestampMS"] <= app_data[0][0])]
    if zoomed_df.empty:
        print("No data in selected range.")
        return

    dpg.set_value("Gear", [zoomed_df["TimestampMS"].tolist(), zoomed_df["Gear"].tolist()])
    dpg.set_value("Torque", [zoomed_df["TimestampMS"].tolist(), zoomed_df["Torque"].tolist()])
    dpg.set_value("CurrentEngineRpm", [zoomed_df["TimestampMS"].tolist(), zoomed_df["CurrentEngineRpm"].tolist()])

    dpg.set_axis_ticks("zoom_x_axis", ticks)
    dpg.set_axis_limits("zoom_x_axis", app_data[0][1], app_data[0][0])
    dpg.set_axis_limits("zoom_y_axis", app_data[0][3], app_data[0][2])

with dpg.window(label="Signal Viewer",width=1000, height=600):
    dpg.add_text("Drag a region on the top plot to zoom below")

    with dpg.plot(label="Main Plot", no_title=True, height=200, callback=on_drag_rect, query=True, no_menus=True, width=-1):
        dpg.add_plot_axis(dpg.mvXAxis, label="TimestampMS", tag="main_x_axis")
        dpg.set_axis_ticks("main_x_axis", ticks)

        dpg.add_plot_axis(dpg.mvYAxis, label="Amplitude", tag="main_y_axis")

        dpg.add_line_series(df["TimestampMS"].to_list(), df["Gear"].to_list(), parent="main_y_axis")
        dpg.add_line_series(df["TimestampMS"].to_list(), df["Torque"].to_list(), parent="main_y_axis")
        dpg.add_line_series(df["TimestampMS"].to_list(), df["CurrentEngineRpm"].to_list(), parent="main_y_axis")

    # Zoomed plot
    with dpg.plot(label="Zoomed Plot",width=-1,height=200,no_menus=True):
        dpg.add_plot_axis(dpg.mvXAxis, label="TimestampMS", tag="zoom_x_axis")
        dpg.set_axis_ticks("zoom_x_axis", ticks)

        dpg.add_plot_axis(dpg.mvYAxis, label="Amplitude", tag="zoom_y_axis")

        dpg.add_line_series([], [], parent="zoom_y_axis", tag="Gear", label="Gear Label")
        dpg.add_line_series([], [], parent="zoom_y_axis", tag="Torque", label="Torque Label")
        dpg.add_line_series([], [], parent="zoom_y_axis", tag="CurrentEngineRpm", label="CurrentEngineRpm Label")

# Start the app
if __name__ == "__main__":
    dpg.create_viewport(title='Custom Title', width=800, height=600)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
