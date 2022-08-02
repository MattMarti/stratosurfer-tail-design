from enum import Enum
import tkinter as tk

import numpy as np

from . import ButtonSizes
from stratosurfer_tail_design import DesignData
from stratosurfer_tail_design.submodules.airfoil_defs.naca_four_digit_airfoil import NacaFourDigitAirfoil


class TailDimensionsDesignFrame:

    class Options(Enum):
        span = "Span"
        base_chord = "Base chord"
        tip_chord = "Tip chord"
        sweep = "Sweep"

    def __init__(self, gui_handle, parent_frame:tk.Frame, design_data:DesignData):
        self.gui_handle = gui_handle
        self.tail_dimensions_data = design_data.tail_dimensions

        design_frame_label = tk.Label(
            master=parent_frame,
            text="Tail Dimensions\nUnits: mm")
        design_frame_label.pack(side=tk.TOP)

        Options = TailDimensionsDesignFrame.Options
        self.entries = {}
        self._add_entry(parent_frame, Options.span, f"{self.tail_dimensions_data.span}")
        self._add_entry(parent_frame, Options.base_chord, f"{self.tail_dimensions_data.base_chord}")
        self._add_entry(parent_frame, Options.tip_chord, f"{self.tail_dimensions_data.tip_chord}")
        self._add_entry(parent_frame, Options.sweep, f"{self.tail_dimensions_data.sweep}")


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
        Options = TailDimensionsDesignFrame.Options
        self.tail_dimensions_data.span = float(self.entries[Options.span].get())
        self.tail_dimensions_data.base_chord = float(self.entries[Options.base_chord].get())
        self.tail_dimensions_data.tip_chord = float(self.entries[Options.tip_chord].get())
        self.tail_dimensions_data.sweep = float(self.entries[Options.sweep].get())

    def get_surface(self):
        x = [
            0,
            self.sweep + (self.base_chord - self.tip_chord),
            self.sweep + (self.base_chord - self.tip_chord) + self.tip_chord,
            self.base_chord,
            0,
        ]
        y = [
            0,
            self.span,
            self.span,
            0,
            0,
        ]
        return np.array(x), np.array(y)

    def update_entry_boxes(self):
        Options = TailDimensionsDesignFrame.Options
        for option in Options:
            self.entries[option].delete(0, tk.END)
        self.entries[Options.span].insert(0, f"{self.tail_dimensions_data.span}")
        self.entries[Options.base_chord].insert(0, f"{self.tail_dimensions_data.base_chord}")
        self.entries[Options.tip_chord].insert(0, f"{self.tail_dimensions_data.tip_chord}")
        self.entries[Options.sweep].insert(0, f"{self.tail_dimensions_data.sweep}")
