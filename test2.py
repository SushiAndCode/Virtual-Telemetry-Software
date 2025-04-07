import dearpygui.dearpygui as dpg
from math import sin

dpg.create_context()

sindatax = []
sindatay = []
for i in range(0, 100):
    sindatax.append(i / 100)
    sindatay.append(0.5 + 0.5 * sin(50 * i / 100))

with dpg.window(label="Tutorial", width=400, height=600):
    dpg.add_text("Click and drag the middle mouse button over the top plot!")


    def query(sender, app_data, user_data):
        # Get zoomed region limits
        x_max, x_min = app_data[0][0], app_data[0][1]
        y_max, y_min = app_data[0][2], app_data[0][3]

        # Update the axis limits in second plot
        dpg.set_axis_limits("xaxis_tag2", x_min, x_max)
        dpg.set_axis_limits("yaxis_tag2", y_min, y_max)

        # Filter data within zoom range
        zoomed_x = [x for x in sindatax if x_min <= x <= x_max]
        zoomed_y = [y for x, y in zip(sindatax, sindatay) if x_min <= x <= x_max]

        print(zoomed_x)
        print(zoomed_y)

        # Update the second plot line series
        dpg.set_value("zoomed_line", [zoomed_x, zoomed_y])


    with dpg.plot(no_title=True, height=200, callback=query, query=True, no_menus=True, width=-1):
        dpg.add_plot_axis(dpg.mvXAxis, label="x")
        dpg.add_plot_axis(dpg.mvYAxis, label="y")
        dpg.add_line_series(sindatax, sindatay, parent=dpg.last_item())

    # plot 2
    with dpg.plot(no_title=True, height=200, no_menus=True, width=-1):
        dpg.add_plot_axis(dpg.mvXAxis, label="x1", tag="xaxis_tag2")
        dpg.add_plot_axis(dpg.mvYAxis, label="y1", tag="yaxis_tag2")
        dpg.add_line_series([], [], tag="zoomed_line", parent="yaxis_tag2")

dpg.create_viewport(title='Custom Title', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()