from enum import Enum
import tkinter as tk

import numpy as np

from . import ButtonSizes
from stratosurfer_tail_design import DesignData

class Options(Enum):
    c0 = "c0"
    c1 = "c1"
    c2 = "c2"
    c3 = "c3"

class FlatSectionDesignFrame:

    def __init__(self, gui_handle, parent_frame:tk.Frame, design_data:DesignData):
        self.gui_handle = gui_handle
        self.airfoil_design_data = design_data

        naca_digit_label = tk.Label(
            master=parent_frame,
            text="Flatness\nParameters")
        naca_digit_label.pack(side=tk.TOP)

        self.entries = {}
        self._add_entry(parent_frame, Options.c0, f"{self.airfoil_design_data.flat_section.c0}")
        self._add_entry(parent_frame, Options.c1, f"{self.airfoil_design_data.flat_section.c1}")
        self._add_entry(parent_frame, Options.c2, f"{self.airfoil_design_data.flat_section.c2}")
        self._add_entry(parent_frame, Options.c3, f"{self.airfoil_design_data.flat_section.c3}")

    def _add_entry(self, parent_frame:tk.Frame, label_enum, default_value:str):
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
        self.airfoil_design_data.flat_section.c0 = float(self.entries[Options.c0].get())
        self.airfoil_design_data.flat_section.c1 = float(self.entries[Options.c1].get())
        self.airfoil_design_data.flat_section.c2 = float(self.entries[Options.c2].get())
        self.airfoil_design_data.flat_section.c3 = float(self.entries[Options.c3].get())

    def update_entry_boxes(self):
        for option in Options:
            self.entries[option].delete(0, tk.END)
        self.entries[Options.c0].insert(0, f"{self.airfoil_design_data.flat_section.c0}")
        self.entries[Options.c1].insert(0, f"{self.airfoil_design_data.flat_section.c1}")
        self.entries[Options.c2].insert(0, f"{self.airfoil_design_data.flat_section.c2}")
        self.entries[Options.c3].insert(0, f"{self.airfoil_design_data.flat_section.c3}")