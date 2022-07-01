from enum import Enum
import tkinter as tk

import numpy as np

from . import ButtonSizes
from stratosurfer_tail_design import DesignData


class TailPositionDesignFrame:

    class Options(Enum):
        longitudinal_pos = "Longitudinal pos (mm)"
        lateral_pos = "Lateral pos (mm)"
        vertical_pos = "Vertical pos (mm)"
        design_aoa = "Design AoA (deg)"
        dihedrial = "Dihedrial (deg)"

    def __init__(self, gui_handle, parent_frame:tk.Frame, design_data:DesignData):
        self.gui_handle = gui_handle
        self.tail_position = design_data.tail_position

        design_frame_label = tk.Label(
            master=parent_frame,
            text="Tail Position")
        design_frame_label.pack(side=tk.TOP)

        Options = TailPositionDesignFrame.Options
        self.entries = {}
        self.__add_entry(parent_frame, Options.longitudinal_pos, f"{-self.tail_position.pos[1]:.0f}")
        self.__add_entry(parent_frame, Options.lateral_pos, f"{self.tail_position.pos[0]:.0f}")
        self.__add_entry(parent_frame, Options.vertical_pos, f"{self.tail_position.pos[2]:.0f}")
        self.__add_entry(parent_frame, Options.design_aoa, f"{self.tail_position.aoa:.0f}")
        self.__add_entry(parent_frame, Options.dihedrial, f"{self.tail_position.dihedral:.0f}")

    def __add_entry(self, parent_frame:tk.Frame, label_enum, default_value:str):
        frame = tk.Frame(master=parent_frame)
        frame.pack(side=tk.TOP, expand=True)

        label = tk.Label(
            master=frame,
            text=label_enum.value,
            width=2*ButtonSizes.GUI_BUTTON_WIDTH)
        label.pack(side=tk.LEFT)

        string_var = tk.StringVar()
        string_var.set(default_value)

        entry = tk.Entry(
            master=frame,
            width=round(ButtonSizes.GUI_BUTTON_WIDTH/2))
        entry.pack(side=tk.RIGHT)

        self.entries[label_enum] = entry

    def read_design_data(self):
        Options = TailPositionDesignFrame.Options
        self.tail_position.pos = np.array([
            float(self.entries[Options.lateral_pos].get()),
            - float(self.entries[Options.longitudinal_pos].get()),
            float(self.entries[Options.vertical_pos].get()),
        ])
        self.tail_position.aoa = float(self.entries[Options.design_aoa].get())
        self.tail_position.dihedral = float(self.entries[Options.dihedrial].get())

    def update_entry_boxes(self):
        Options = TailPositionDesignFrame.Options
        for option in Options:
            self.entries[option].delete(0, tk.END)
        self.entries[Options.longitudinal_pos].insert(0, f"{-self.tail_position.pos[1]:.0f}")
        self.entries[Options.lateral_pos].insert(0, f"{self.tail_position.pos[0]:.0f}")
        self.entries[Options.vertical_pos].insert(0, f"{self.tail_position.pos[2]:.0f}")
        self.entries[Options.design_aoa].insert(0, f"{self.tail_position.aoa:.0f}")
        self.entries[Options.dihedrial].insert(0, f"{self.tail_position.dihedral:.0f}")

