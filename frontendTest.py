import pandas as pd
import numpy as np
import dearpygui.dearpygui as dpg

def ms_to_mmss(ms):
    seconds = ms // 1000
    minutes = seconds // 60
    sec = seconds % 60
    return f"{int(minutes):02}:{int(sec):02}"


df = pd.read_csv(r"C:\dev\Virtual-Telemetry-Software\telem3.csv")
df["Gear"] = df["Gear"].apply(lambda x: np.nan if x > 6 else x)

# Get range from your data
min_x = df["TimestampMS"].min()
max_x = df["TimestampMS"].max()

# Create ticks every 30 seconds (30000 ms for example)
tick_interval = 30000  # or 60000 for 1-minute steps
custom_ticks = list(range(min_x, max_x + 1, tick_interval))
tick_labels = [ms_to_mmss(ms) for ms in custom_ticks]
ticks = tuple(zip(tick_labels, custom_ticks))


dpg.create_context()
dpg.create_viewport()
dpg.setup_dearpygui()

def on_drag_rect(sender, app_data, user_data):
    if "rect" not in app_data:
        return
    x1, _, x2, _ = app_data["rect"]
    if x1 == x2:
        return

    # Ensure x1 < x2
    if x2 < x1:
        x1, x2 = x2, x1

    zoomed_df = df[(df["TimestampMS"] >= x1) & (df["TimestampMS"] <= x2)]

    dpg.set_value("Gear", [zoomed_df["TimestampMS"].tolist(), zoomed_df["Gear"].tolist()])
    dpg.set_value("Torque", [zoomed_df["TimestampMS"].tolist(), zoomed_df["Torque"].tolist()])
    dpg.set_value("CurrentEngineRpm", [zoomed_df["TimestampMS"].tolist(), zoomed_df["CurrentEngineRpm"].tolist()])


with dpg.window(label="Signal Viewer",width=1000, height=600):
    dpg.add_text("Drag a region on the top plot to zoom below")


    with dpg.plot(label="Main Plot", height=250, width=-1):
        dpg.add_plot_axis(dpg.mvXAxis, label="TimestampMS", tag="main_x_axis")
        # Set your custom formatted ticks
        dpg.set_axis_ticks(dpg.last_item(), ticks)

        dpg.add_plot_axis(dpg.mvYAxis, label="Amplitude", tag="main_y_axis")

        dpg.add_line_series(df["TimestampMS"].to_list(), df["Gear"].to_list(), parent="main_y_axis")
        dpg.add_line_series(df["TimestampMS"].to_list(), df["Torque"].to_list(), parent="main_y_axis")
        dpg.add_line_series(df["TimestampMS"].to_list(), df["CurrentEngineRpm"].to_list(), parent="main_y_axis")

        try:
            
            
            dpg.add_drag_rect(
                callback=on_drag_rect,
                tag="dragrect",
                color=[0, 255, 0, 200],
                fill=[0, 255, 0, 60]           
            )


        except Exception as e:
            print(e)

    with dpg.plot(label="Zoomed Plot", height=250, width=-1):
        dpg.add_plot_axis(dpg.mvXAxis, label="TimestampMS", tag="zoom_x_axis")
        dpg.add_plot_axis(dpg.mvYAxis, label="Amplitude", tag="zoom_y_axis")

        dpg.add_line_series([],[],parent="zoom_y_axis")
        dpg.add_line_series([],[],parent="zoom_y_axis")
        dpg.add_line_series([],[],parent="zoom_y_axis")


if __name__ == "__main__":
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
