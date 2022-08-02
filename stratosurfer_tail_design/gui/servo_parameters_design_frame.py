from enum import Enum
import tkinter as tk

import numpy as np

from . import ButtonSizes
from stratosurfer_tail_design import DesignData


class Options(Enum):
    x = "x"
    y = "y"
    length = "length"
    width = "width"
    ctrl_horn_x = "ctrl_horn_x"
    ctrl_horn_y = "ctrl_horn_y"


class ServoParametersDesignFrame:

    def __init__(self, gui_handle, parent_frame:tk.Frame, design_data:DesignData):
        self.gui_handle = gui_handle
        self.servo_parameters = design_data.servo_parameters

        design_frame_label = tk.Label(
            master=parent_frame,
            text="Servo Params\nUnits: mm")
        design_frame_label.pack(side=tk.TOP)

        self.entries = {}
        self._add_entry(parent_frame, Options.x, f"{self.servo_parameters.x}")
        self._add_entry(parent_frame, Options.y, f"{self.servo_parameters.y}")
        self._add_entry(parent_frame, Options.length, f"{self.servo_parameters.length}")
        self._add_entry(parent_frame, Options.width, f"{self.servo_parameters.width}")
        self._add_entry(parent_frame, Options.ctrl_horn_x, f"{self.servo_parameters.ctrl_horn_x}")
        self._add_entry(parent_frame, Options.ctrl_horn_y, f"{self.servo_parameters.ctrl_horn_y}")


    def _add_entry(self, parent_frame:tk.Frame, label_enum, default_value:str):
        frame = tk.Frame(master=parent_frame)
        frame.pack(side=tk.TOP, expand=True)

        label = tk.Label(
            master=frame,
            text=label_enum.value,
            width=ButtonSizes.GUI_BUTTON_WIDTH)
        label.pack(side=tk.LEFT)

        string_var = tk.StringVar()
        string_var.set(default_value)

        entry = tk.Entry(
            master=frame,
            width=round(ButtonSizes.GUI_BUTTON_WIDTH/2),
            textvariable=string_var)
        entry.pack(side=tk.RIGHT)

        self.entries[label_enum] = entry

    def read_design_data(self):
        self.servo_parameters.x = float(self.entries[Options.x].get())
        self.servo_parameters.y = float(self.entries[Options.y].get())
        self.servo_parameters.length = float(self.entries[Options.length].get())
        self.servo_parameters.width = float(self.entries[Options.width].get())
        self.servo_parameters.ctrl_horn_x = float(self.entries[Options.ctrl_horn_x].get())
        self.servo_parameters.ctrl_horn_y = float(self.entries[Options.ctrl_horn_y].get())


    def update_entry_boxes(self):
        for option in Options:
            self.entries[option].delete(0, tk.END)
        self.entries[Options.x].insert(0, f"{self.servo_parameters.x}")
        self.entries[Options.y].insert(0, f"{self.servo_parameters.y}")
        self.entries[Options.length].insert(0, f"{self.servo_parameters.length}")
        self.entries[Options.width].insert(0, f"{self.servo_parameters.width}")
        self.entries[Options.ctrl_horn_x].insert(0, f"{self.servo_parameters.ctrl_horn_x}")
        self.entries[Options.ctrl_horn_y].insert(0, f"{self.servo_parameters.ctrl_horn_y}")
