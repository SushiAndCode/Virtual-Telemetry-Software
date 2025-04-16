import pandas as pd
import dearpygui.dearpygui as dpg
import Model.Laps as lp
import Controller.Controller as cl
# DearPyGui setup
dpg.create_context()


app = cl.Controller()
app.start()


dpg.create_viewport(title='Custom Title', width=800, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
