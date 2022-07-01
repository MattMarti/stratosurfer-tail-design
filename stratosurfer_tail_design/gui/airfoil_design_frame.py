from enum import Enum
import tkinter as tk

import numpy as np

from . import ButtonSizes
from stratosurfer_tail_design import DesignData


class AirfoilDesignFrame:

    class Options(Enum):
        m = "m"
        p = "p"
        t = "t"

    def __init__(self, gui_handle, parent_frame:tk.Frame, design_data:DesignData):
        self.gui_handle = gui_handle
        self.airfoil_design_data = design_data.airfoil

        naca_digit_label = tk.Label(
            master=parent_frame,
            text="Tail Aifoil\nNACA 4-digit")
        naca_digit_label.pack(side=tk.TOP)

        Options = AirfoilDesignFrame.Options
        self.entries = {}
        self.__add_entry(parent_frame, Options.m, f"{self.airfoil_design_data.m}")
        self.__add_entry(parent_frame, Options.p, f"{self.airfoil_design_data.p}")
        self.__add_entry(parent_frame, Options.t, f"{self.airfoil_design_data.t}")

    def __add_entry(self, parent_frame:tk.Frame, label_enum, default_value:str):
        frame = tk.Frame(master=parent_frame)
        frame.pack(side=tk.TOP)

        label = tk.Label(
            master=frame,
            text=label_enum.value,
            width=round(ButtonSizes.GUI_BUTTON_WIDTH/2))
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
        Options = AirfoilDesignFrame.Options
        self.airfoil_design_data.m = int(self.entries[Options.m].get())
        self.airfoil_design_data.p = int(self.entries[Options.p].get())
        self.airfoil_design_data.t = int(self.entries[Options.t].get())

    def update_entry_boxes(self):
        Options = AirfoilDesignFrame.Options
        for option in Options:
            self.entries[option].delete(0, tk.END)
        self.entries[Options.m].insert(0, f"{self.airfoil_design_data.m}")
        self.entries[Options.p].insert(0, f"{self.airfoil_design_data.p}")
        self.entries[Options.t].insert(0, f"{self.airfoil_design_data.t}")
