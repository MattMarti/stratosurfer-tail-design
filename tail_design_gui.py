import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod

import numpy as np

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

from stratosurfer_tail_design.submodules.airfoil_defs.naca_four_digit_airfoil import NacaFourDigitAirfoil


GUI_BUTTON_WIDTH = 10
GUI_BUTTON_PADDING = 20


def apply_pretty_plot_settings(ax):
    ax.grid(which="major")
    ax.minorticks_on()
    ax.grid(which="minor", linestyle="--", linewidth=0.3)


class Plotter(ABC):

    def __init__(self, parent_frame:tk.Frame):
        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)

        canvas = FigureCanvasTkAgg(self.fig, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, parent_frame, pack_toolbar=False)
        toolbar.update()
        toolbar.pack(side=tk.TOP, fill=tk.X)

    @abstractmethod
    def refresh_plot(self, design_frames:dict):
        ...


class PositionalDesignControlFrame:
    pass


class StaticMarginPlotter(Plotter):

    def refresh_plot(self, design_frames):
        pass


class AirfoilDesignControlFrame:

    def __init__(self, parent_frame):
        naca_digit_label = tk.Label(
            master=parent_frame,
            text="Tail Aifoil\nNACA 4-digit")
        naca_digit_label.pack(side=tk.TOP)

        self.entries = {}
        self.add_entry(parent_frame, "m", "0")
        self.add_entry(parent_frame, "p", "5")
        self.add_entry(parent_frame, "t", "12")

    def add_entry(self, parent_frame, label_text, default_value:str):
        frame = tk.Frame(master=parent_frame)
        frame.pack(side=tk.TOP)

        label = tk.Label(
            master=frame,
            text=label_text,
            width=round(GUI_BUTTON_WIDTH/2))
        label.pack(side=tk.LEFT)

        entry = tk.Entry(
            master=frame,
            width=round(GUI_BUTTON_WIDTH/2))
        entry.pack(side=tk.RIGHT)
        entry.insert(0, default_value)

        self.entries[label_text] = entry

    @property
    def m(self):
        return int(self.entries["m"].get())

    @property
    def p(self):
        return int(self.entries["p"].get())

    @property
    def t(self):
        return int(self.entries["t"].get())

    def get_upper_surface(self):
        airfoil = NacaFourDigitAirfoil(self.m, self.p, self.t)
        xu = np.linspace(1, 0, 10000)
        xu, yu = airfoil.get_upper(xu)
        return xu, yu

    def get_lower_surface(self):
        airfoil = NacaFourDigitAirfoil(self.m, self.p, self.t)
        xl = np.linspace(0, 1, 10000)
        xl, yl = airfoil.get_lower(xl)
        return xl, yl


class AirfoilPlotter(Plotter):

    def refresh_plot(self, design_frames):
        xu, yu = design_frames["Airfoil"].get_upper_surface()
        xl, yl = design_frames["Airfoil"].get_lower_surface()

        self.ax.clear()
        self.ax.plot(np.concatenate((xu,xl)), np.concatenate((yu, yl), 0))
        self.ax.axis("equal")
        apply_pretty_plot_settings(self.ax)
        self.fig.canvas.draw()


class TailDesignControlFrame:

    def __init__(self, parent_frame):
        naca_digit_label = tk.Label(
            master=parent_frame,
            text="Tail Dimensions\nUnits: mm")
        naca_digit_label.pack(side=tk.TOP)

        self.entries = {}
        self.add_entry(parent_frame, "Span", "250")
        self.add_entry(parent_frame, "Base chord", "200")
        self.add_entry(parent_frame, "Tip chord", "150")
        self.add_entry(parent_frame, "Sweep", "50")

    def add_entry(self, parent_frame, label_text, default_value:str):
        frame = tk.Frame(master=parent_frame)
        frame.pack(side=tk.TOP, expand=True)

        label = tk.Label(
            master=frame,
            text=label_text,
            width=GUI_BUTTON_WIDTH)
        label.pack(side=tk.LEFT)

        entry = tk.Entry(
            master=frame,
            width=round(GUI_BUTTON_WIDTH/2))
        entry.pack(side=tk.RIGHT)
        entry.insert(0, default_value)

        self.entries[label_text] = entry

    @property
    def span(self):
        return float(self.entries["Span"].get())

    @property
    def base_chord(self):
        return float(self.entries["Base chord"].get())

    @property
    def tip_chord(self):
        return float(self.entries["Tip chord"].get())

    @property
    def sweep(self):
        return float(self.entries["Sweep"].get())

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


class TailPlotter(Plotter):

    def refresh_plot(self, design_frames):
        x, y = design_frames["Dimensions"].get_surface()

        self.ax.clear()
        self.ax.plot(x, y, 0)
        apply_pretty_plot_settings(self.ax)
        self.ax.axis("equal")
        self.fig.canvas.draw()


class GuiManager:

    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Stratosurfer Tail Design Tool")

        self.plotters = {}
        self.design_frames = {}
        self.initialize_design_control_frames()
        self.initialize_figures()

        self.refresh_plot()

    def run(self):
        self.root.mainloop()

    def quit(self):
        self.root.quit()
        self.root.destroy()

    def refresh_plot(self):
        for tab_index in self.figure_control.tabs():
            tab = self.figure_control.tab(tab_index)
            tab_name = tab["text"]
            plotter = self.plotters[tab_name]
            plotter.refresh_plot(self.design_frames)

    def initialize_figures(self):
        figure_frame = tk.Frame(master=self.root)
        figure_frame.pack(side=tk.TOP)

        self.figure_control = ttk.Notebook(master=figure_frame)
        self.figure_control.pack(side=tk.TOP)

        dimensions_plotter_frame = tk.Frame(master=self.figure_control)
        self.plotters["Dimensions"] = TailPlotter(dimensions_plotter_frame)
        self.figure_control.add(dimensions_plotter_frame, text="Dimensions")

        airfoil_plotter_frame = tk.Frame(master=self.figure_control)
        self.plotters["Airfoil"] = AirfoilPlotter(airfoil_plotter_frame)
        self.figure_control.add(airfoil_plotter_frame, text="Airfoil")

        refresh_button = tk.Button(
            master=figure_frame,
            text="Refresh",
            width=GUI_BUTTON_WIDTH,
            command=lambda: self.refresh_plot()
        )
        refresh_button.pack(side=tk.TOP, anchor=tk.NW)

    def initialize_design_control_frames(self):
        design_control_frame = tk.Frame(master=self.root)
        design_control_frame.pack(side=tk.BOTTOM, anchor=tk.NE)

        airfoil_design_parent = tk.Frame(
            master=design_control_frame,
            highlightbackground="grey",
            highlightthickness=1
        )
        airfoil_design_parent.pack(side=tk.RIGHT)
        airfoil_design_frame = AirfoilDesignControlFrame(airfoil_design_parent)
        self.design_frames["Airfoil"] = airfoil_design_frame

        tail_dimensions_parent = tk.Frame(
            master=design_control_frame,
            highlightbackground="grey",
            highlightthickness=1
        )
        tail_dimensions_parent.pack(side=tk.RIGHT)
        tail_dimensions = TailDesignControlFrame(tail_dimensions_parent)
        self.design_frames["Dimensions"] = tail_dimensions


def main():
    gui = GuiManager()
    gui.run()


if __name__ == '__main__':
    main()
