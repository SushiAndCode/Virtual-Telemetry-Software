import pandas as pd
import Model.Laps as lp
import dearpygui.dearpygui as dpg
import numpy as np

class Controller():
    def __init__(self):
        self.setUpUI()
        self.laps = lp(self.csvRetriever)
        self.df = self.laps.df

    def csvRetriever(self,sender, app_data):
        return pd.read_csv(app_data['file_path_name'])
    
    def toggle_line_series(self,sender, app_data, user_data):
        if dpg.is_item_shown(user_data):
            dpg.hide_item(user_data)
        else:
            dpg.show_item(user_data)

    def normalizeSeriesCallback(self):
        for channel in self.df.columns:
            if channel != "TimestampMS":
                data = self.df[channel].to_list()
                min_val = min(self.df[channel].to_list())
                max_val = max(self.df[channel].to_list())
                # Avoid division by zero
                if max_val - min_val == 0:
                    normalized = [0] * len(data)
                else:
                    normalized = [(x - min_val) / (max_val - min_val) for x in data]
                dpg.set_value(channel, [self.df["TimestampMS"].to_list(), normalized])

    def scaleUpSeriesCallback(self):
        for channel in self.df.columns:
            if channel != "TimestampMS":
                data = self.df[channel].to_list()
                dpg.set_value(channel, [self.df["TimestampMS"].to_list(), data])

    def on_mouse_move(self,sender, app_data):

        mouse_x, _ = dpg.get_plot_mouse_pos()
        if not np.isnan(mouse_x) and not np.isinf(mouse_x):
            idx = (np.abs(self.df["TimestampMS"] - mouse_x)).idxmin()
            pos_x = self.df.iloc[idx]["PositionX"]
            pos_y = self.df.iloc[idx]["PositionZ"]
            dpg.set_value("cursor_dot", [[pos_x], [pos_y]])

    def setUpUI(self):
        
        with dpg.file_dialog(directory_selector=False, show=False, callback= self.csvRetriever, id="file_dialog_id"):
            dpg.add_file_extension(".csv")

        with dpg.window(label="Telemetry Viewer",width=1000, height=600):

            with dpg.menu_bar():
                with dpg.menu(label="Channels"):
                    with dpg.menu(label="Channels", tag="channels_menu"):
                        for tag in self.df.columns:
                            if tag != "TimestampMS":
                                dpg.add_menu_item(parent="channels_menu", label=tag, callback=self.toggle_line_series, user_data=tag)

                dpg.add_menu_item(label="Normalize Channels", callback= self.normalizeSeriesCallback)

                dpg.add_menu_item(label = "Scale Up Channels", callback = self.scaleUpSeriesCallback)

                dpg.add_menu_item(label = "Load File", callback=lambda: dpg.show_item("file_dialog_id"))


        with dpg.group(horizontal=True):

            with dpg.child_window(width=200, autosize_y=True, border=True):
                dpg.add_text("Channel Visibility")
                for i in range(self.laps.laps):  # Example: 5 checkboxes
                    dpg.add_checkbox(label=f"Channel {i+1}", callback=lambda s,a,u=i: print(f"Toggled Channel {u+1}"))

            with dpg.group():
                with dpg.plot(label="Telemetry",height=400, width=-1, tag = "Main Plot"):
                    dpg.add_plot_legend()
                    dpg.add_plot_axis(dpg.mvXAxis, label="TimestampMS", tag="main_x_axis")
                    with dpg.plot_axis(dpg.mvYAxis, label="Amplitude", tag="main_y_axis"):
                        for channel in self.df.columns:
                            if channel != "TimestampMS" and not dpg.does_item_exist(channel):
                                dpg.add_line_series(
                                    self.df["TimestampMS"].to_list(),
                                    self.df[channel].to_list(),
                                    label=channel,
                                    tag=channel,
                                    parent="main_y_axis"
                                )
                                dpg.hide_item(channel)

                with dpg.plot(label = "Track",height=400, width=-1, tag="track_plot"):
                    dpg.add_plot_axis(dpg.mvXAxis, label="X position", tag = "positionX")
                    with dpg.plot_axis(dpg.mvYAxis, label="Y position", tag="positionY"):
                        
                        dpg.add_scatter_series(
                            [], [], label="Cursor Dot", parent="positionY", tag="cursor_dot"
                        )
                    # Automatically adjust axis limits to fit the data
                    dpg.set_axis_limits_auto("positionX")
                    dpg.set_axis_limits_auto("positionY")

        with dpg.handler_registry():
            dpg.add_mouse_move_handler(callback=self.on_mouse_move)