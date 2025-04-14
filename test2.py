import dearpygui.dearpygui as dpg
import pandas as pd

def file_selected_callback(sender, app_data):
    print("Selected file:", app_data['file_path_name'])
    df = pd.read_csv(app_data['file_path_name'])
    print(df)

dpg.create_context()

with dpg.file_dialog(directory_selector=False, show=False, callback=file_selected_callback, id="file_dialog_id"):
    dpg.add_file_extension(".csv")

with dpg.window(label="Main Window"):
    dpg.add_button(label="Select File", callback=lambda: dpg.show_item("file_dialog_id"))

dpg.create_viewport(title="File Picker Example", width=600, height=300)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()