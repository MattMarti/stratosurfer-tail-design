from enum import Enum
import tkinter as tk

import numpy as np

from . import ButtonSizes
from stratosurfer_tail_design import DesignData


class Options(Enum):
    span = "span"
    width = "width"
    span_begin = "span_begin"


class ElevatorFlapDesignFrame:

    def __init__(self, gui_handle, parent_frame:tk.Frame, design_data:DesignData):
        self.gui_handle = gui_handle
        self.elevator_flap = design_data.elevator_flap

        design_frame_label = tk.Label(
            master=parent_frame,
            text="Servo Params\nUnits: mm")
        design_frame_label.pack(side=tk.TOP)

        self.entries = {}
        self._add_entry(parent_frame, Options.span, f"{self.elevator_flap.span}")
        self._add_entry(parent_frame, Options.width, f"{self.elevator_flap.width}")
        self._add_entry(parent_frame, Options.span_begin, f"{self.elevator_flap.span_begin}")

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
        self.elevator_flap.span = float(self.entries[Options.span].get())
        self.elevator_flap.width = float(self.entries[Options.width].get())
        self.elevator_flap.span_begin = float(self.entries[Options.span_begin].get())

    def update_entry_boxes(self):
        for option in Options:
            self.entries[option].delete(0, tk.END)
        self.entries[Options.span].insert(0, f"{self.elevator_flap.span}")
        self.entries[Options.width].insert(0, f"{self.elevator_flap.width}")
        self.entries[Options.span_begin].insert(0, f"{self.elevator_flap.span_begin}")
