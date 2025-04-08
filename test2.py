import dearpygui.dearpygui as dpg
# DearPyGui setup
dpg.create_context()
line_series_data = {
    "Line A": "line_series_a",
    "Line B": "line_series_b",
    "Line C": "line_series_c"
}

with dpg.window(label="Demo", width=600, height=400):
    
    def toggle_line_series(sender, app_data, user_data):
        
        if dpg.is_item_shown(user_data):
            dpg.hide_item(user_data)
        else:
            dpg.show_item(user_data)

    # Menu bar
    with dpg.menu_bar():
        with dpg.menu(label="Edit"):
            for label, tag in line_series_data.items():
                print(tag)
                print(type(tag))
                dpg.add_menu_item(label = label, callback=toggle_line_series, user_data=tag)

    # Plot area
    with dpg.plot(label="My Plot", height=300, width=500):
        dpg.add_plot_legend()
        dpg.add_plot_axis(dpg.mvXAxis, label="X Axis")
        with dpg.plot_axis(dpg.mvYAxis, label="Y Axis"):
            for label, tag in line_series_data.items():
                dpg.add_line_series([0, 1, 2, 3], [0, 1, 4, 9], label=label, tag=tag)
                dpg.hide_item(tag)

dpg.create_viewport(title='Custom Title', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()