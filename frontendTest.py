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

df = pd.read_csv(r"C:\dev\Virtual-Telemetry-Software\telem5.csv")

df["TimestampMS"] = pd.to_numeric(df["TimestampMS"], errors="coerce")
df["TimestampMS"] = df["TimestampMS"] - min(df["TimestampMS"])
df.dropna(subset=["TimestampMS"], inplace=True)
df["Gear"] = df["Gear"].apply(lambda x: np.nan if x == 11 else x)

min_x = int(df["TimestampMS"].min())
max_x = int(df["TimestampMS"].max())

tick_interval = 5000 
custom_ticks = list(range(min_x, max_x + 1, tick_interval))
tick_labels = [ms_to_mmss(ms) for ms in custom_ticks]
ticks = tuple(zip(tick_labels, custom_ticks))

with dpg.window(label="Telemetry Viewer",width=1000, height=600):
    
    dpg.add_text("Telemetry Viewer")

    def toggle_line_series(sender, app_data, user_data):
        if dpg.is_item_shown(user_data):
            dpg.hide_item(user_data)
        else:
            dpg.show_item(user_data)

    def on_mouse_move(sender, app_data):

        mouse_x, mouse_y = dpg.get_plot_mouse_pos()
        if not np.isnan(mouse_x) and not np.isinf(mouse_x):
            idx = (np.abs(df["TimestampMS"] - mouse_x)).idxmin()
            pos_x = df.iloc[idx]["PositionX"]
            pos_y = df.iloc[idx]["PositionZ"]
            dpg.set_value("cursor_dot", [[pos_x], [pos_y]])

    def normalize_series_callback(sender, app_data, user_data):
        # Normalize each series (except timestamp)
        timestamps = df["TimestampMS"].to_list()
        for channel in df.columns:
            if channel != "TimestampMS":
                data = df[channel].to_list()
                min_val = min(data)
                max_val = max(data)
                # Avoid division by zero
                if max_val - min_val == 0:
                    normalized = [0] * len(data)
                else:
                    normalized = [(x - min_val) / (max_val - min_val) for x in data]
                dpg.set_value(channel, [timestamps, normalized])

    with dpg.menu_bar():
        with dpg.menu(label="Channels"):
            for tag in df.columns:
                if tag != "TimestampMS":
                    dpg.add_menu_item(label = tag,callback=toggle_line_series, user_data=tag)

        dpg.add_menu_item(label="Normalize Channels", callback=normalize_series_callback)

    with dpg.plot(label="Telemetry",height=400, width=-1):
        dpg.add_plot_legend()
        dpg.add_plot_axis(dpg.mvXAxis, label="TimestampMS", tag="main_x_axis")
        dpg.set_axis_ticks("main_x_axis", ticks)
        with dpg.plot_axis(dpg.mvYAxis, label="Amplitude"):
            for channel in df.columns:
                if channel != "TimestampMS":
                    dpg.add_line_series(df["TimestampMS"].to_list(), df[channel].to_list(),label = channel ,tag=channel)
                    dpg.hide_item(channel)

    with dpg.plot(label = "Track",height=400, width=-1, tag="track_plot"):
        
        dpg.add_plot_axis(dpg.mvXAxis, label="X position", tag = "positionX")
        with dpg.plot_axis(dpg.mvYAxis, label="Y position", tag="positionY"):
            dpg.add_line_series(df["PositionX"].tolist(), df["PositionZ"].tolist(), parent="positionY", label="Plotted Track")

            dpg.add_scatter_series(
                [], [], label="Cursor Dot", parent="positionY", tag="cursor_dot"
            )
        # Automatically adjust axis limits to fit the data
        dpg.set_axis_limits_auto("positionX")
        dpg.set_axis_limits_auto("positionY")

    with dpg.handler_registry():
        dpg.add_mouse_move_handler(callback=on_mouse_move)


if __name__ == "__main__":
    dpg.create_viewport(title='Custom Title', width=800, height=600)
    dpg.setup_dearpygui()
    dpg.show_viewport()
    dpg.start_dearpygui()
    dpg.destroy_context()
