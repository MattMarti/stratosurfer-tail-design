import tkinter as tk
from tkinter import ttk
from tkinter import filedialog

import numpy as np

from stratosurfer_tail_design import design_data
from stratosurfer_tail_design.gui import (
    ButtonSizes,
    info_frames,
    AirfoilDesignFrame,
    TailDimensionsDesignFrame,
    FlatSectionDesignFrame,
    ServoParametersDesignFrame,
    ElevatorFlapDesignFrame,
)
import stratosurfer_tail_design.data_loading as data_loading

class GuiManager:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Stratosurfer Tail Design Tool")

        self.design_data = None
        self.load_design()

        self.plot_frames = {}
        self.design_frames = {}
        self.initialize_design_control_frames()
        self.initialize_figures()

        self.update_entry_boxes()
        self.refresh_info_display()

    def run(self):
        self.root.mainloop()

    def quit(self):
        self.root.quit()
        self.root.destroy()

    def load_design(self):
        self.design_data = data_loading.load_tail_design()

    def load_design_and_refresh(self):
        self.load_design()
        self.update_entry_boxes()
        self.refresh_info_display()

    def save_design(self):
        data_loading.save_tail_design(self.design_data)

    def export_airfoil(self):

        x_airfoil, y_airfoil = self.plot_frames["Airfoil"].get_airfoil_surface(num_points=500)
        with filedialog.asksaveasfile(
            title="Export airfoil",
            filetypes=[("csv", "*.csv"), ("data", "*.dat"), ("Text", "*.txt")],
            initialdir="data",
            defaultextension=".csv",
            initialfile="elev_airfoil.csv"
        ) as fid:
            for x, y in zip(x_airfoil, y_airfoil):
                fid.write(f"{x:.6f}, {y:.6f}\n")

    def update_entry_boxes(self):
        for design_control in self.design_frames.values():
            design_control.update_entry_boxes()

    def refresh_info_display(self):
        for design_frame in self.design_frames.values():
            design_frame.read_design_data()
        for tab_index in self.figure_control.tabs():
            tab = self.figure_control.tab(tab_index)
            tab_name = tab["text"]
            self.plot_frames[tab_name].refresh()
        self.update_entry_boxes()

    def initialize_figures(self):
        figure_frame = tk.Frame(master=self.root)
        figure_frame.pack(side=tk.TOP)

        self.figure_control = ttk.Notebook(master=figure_frame)
        self.figure_control.pack(side=tk.TOP)

        airfoil_plotter_frame = tk.Frame(master=self.figure_control)
        self.plot_frames["Airfoil"] = info_frames.AirfoilPlotFrame(airfoil_plotter_frame, self.design_data)
        self.figure_control.add(airfoil_plotter_frame, text="Airfoil")

        dimensions_plotter_frame = tk.Frame(master=self.figure_control)
        self.plot_frames["Dimensions"] = info_frames.DimensionsPlotFrame(dimensions_plotter_frame, self.design_data)
        self.figure_control.add(dimensions_plotter_frame, text="Dimensions")

        plot_buttons_frame = tk.Frame(master=self.root)
        plot_buttons_frame.pack(side=tk.LEFT)

        refresh_button = tk.Button(
            master=plot_buttons_frame,
            text="Refresh",
            width=ButtonSizes.GUI_BUTTON_WIDTH,
            command=lambda: self.refresh_info_display()
        )
        refresh_button.pack(side=tk.TOP, anchor=tk.NW)

        utility_buttons_frame = tk.Frame(master=self.root)
        utility_buttons_frame.pack(side=tk.RIGHT)

        save_design_button = tk.Button(
            master=utility_buttons_frame,
            text="Save design",
            width=ButtonSizes.GUI_BUTTON_WIDTH,
            command=lambda: self.save_design()
        )
        save_design_button.pack(side=tk.TOP, anchor=tk.NW)

        load_design_button = tk.Button(
            master=utility_buttons_frame,
            text="Load design",
            width=ButtonSizes.GUI_BUTTON_WIDTH,
            command=lambda: self.load_design_and_refresh()
        )
        load_design_button.pack(side=tk.TOP, anchor=tk.NW)

        export_airfoil_button = tk.Button(
            master=utility_buttons_frame,
            text="Export Airfoil",
            width=ButtonSizes.GUI_BUTTON_WIDTH,
            command=lambda: self.export_airfoil()
        )
        export_airfoil_button.pack(side=tk.TOP, anchor=tk.NW)

    def initialize_design_control_frames(self):
        design_control_frame = tk.Frame(master=self.root)
        design_control_frame.pack(side=tk.BOTTOM, anchor=tk.NE)

        airfoil_design_parent = tk.Frame(
            master=design_control_frame,
            highlightbackground="grey",
            highlightthickness=1
        )
        airfoil_design_parent.pack(side=tk.RIGHT)
        self.design_frames["Airfoil"] = AirfoilDesignFrame(self, airfoil_design_parent, self.design_data)

        flat_section_parent = tk.Frame(
            master=design_control_frame,
            highlightbackground="grey",
            highlightthickness=1
        )
        flat_section_parent.pack(side=tk.RIGHT)
        self.design_frames["Flat Section"] = FlatSectionDesignFrame(self, flat_section_parent, self.design_data)

        tail_dimensions_parent = tk.Frame(
            master=design_control_frame,
            highlightbackground="grey",
            highlightthickness=1
        )
        tail_dimensions_parent.pack(side=tk.RIGHT)
        self.design_frames["Dimensions"] = TailDimensionsDesignFrame(self, tail_dimensions_parent, self.design_data)

        servo_parameters_parent = tk.Frame(
            master=design_control_frame,
            highlightbackground="grey",
            highlightthickness=1
        )
        servo_parameters_parent.pack(side=tk.RIGHT)
        self.design_frames["Servo Params"] = ServoParametersDesignFrame(self, servo_parameters_parent, self.design_data)

        elevator_flap_parent = tk.Frame(
            master=design_control_frame,
            highlightbackground="grey",
            highlightthickness=1
        )
        elevator_flap_parent.pack(side=tk.RIGHT)
        self.design_frames["Elevator Flap"] = ElevatorFlapDesignFrame(self, elevator_flap_parent, self.design_data)


def main():
    gui = GuiManager()
    gui.run()


if __name__ == '__main__':
    main()
