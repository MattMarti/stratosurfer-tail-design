import tkinter as tk
from tkinter import ttk
from abc import ABC, abstractmethod

import numpy as np
from matplotlib.pyplot import Axes
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)

from stratosurfer_tail_design import DesignData
from stratosurfer_tail_design.submodules.airfoil_defs.naca_four_digit_airfoil import NacaFourDigitAirfoil
from . import ButtonSizes

def apply_pretty_plot_settings(ax:Axes):
    ax.grid(which="major")
    ax.minorticks_on()
    ax.grid(which="minor", linestyle="--", linewidth=0.3)


class InfoFrameBase(ABC):

    def __init__(self, parent_frame:tk.Frame, design_data:DesignData):
        self.parent_frame = parent_frame
        self.design_data = design_data

    @abstractmethod
    def refresh(self):
        ...


class PlotterFrameBase(InfoFrameBase):

    def __init__(self, parent_frame:tk.Frame, design_data:DesignData):
        super().__init__(parent_frame, design_data)

        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.add_subplot(111)

        canvas = FigureCanvasTkAgg(self.fig, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, parent_frame, pack_toolbar=False)
        toolbar.update()
        toolbar.pack(side=tk.TOP, fill=tk.X)


class DimensionsPlotFrame(PlotterFrameBase):

    def _get_surface(self):
        td = self.design_data.tail_dimensions
        x = [
            0,
            td.sweep + (td.base_chord - td.tip_chord),
            td.sweep + (td.base_chord - td.tip_chord) + td.tip_chord,
            td.base_chord,
            0,
        ]
        y = [
            0,
            td.span,
            td.span,
            0,
            0,
        ]
        return np.array(x), np.array(y)

    def refresh(self):
        x, y = self._get_surface()

        self.ax.clear()
        self.ax.plot(x, y, 0)
        apply_pretty_plot_settings(self.ax)
        self.ax.axis("equal")
        self.fig.canvas.draw()


class AirfoilPlotFrame(PlotterFrameBase):

    def refresh(self):
        xu, yu = self._get_upper_surface()
        xl, yl = self._get_lower_surface()
        self.ax.clear()
        self.ax.plot(np.concatenate((xu,xl)), np.concatenate((yu, yl), 0))
        self.ax.axis("equal")
        apply_pretty_plot_settings(self.ax)
        self.fig.canvas.draw()

    def _get_upper_surface(self):
        airfoil = NacaFourDigitAirfoil(
            self.design_data.airfoil.m,
            self.design_data.airfoil.p,
            self.design_data.airfoil.t
        )
        xu = np.linspace(1, 0, 10000)
        xu, yu = airfoil.get_upper(xu)
        return xu, yu

    def _get_lower_surface(self):
        airfoil = NacaFourDigitAirfoil(
            self.design_data.airfoil.m,
            self.design_data.airfoil.p,
            self.design_data.airfoil.t
        )
        xl = np.linspace(0, 1, 10000)
        xl, yl = airfoil.get_lower(xl)
        return xl, yl


class StaticMarginInfoFrame(InfoFrameBase):

    def __init__(self, parent_frame:tk.Frame, design_data:DesignData):
        super().__init__(parent_frame, design_data)
        self.display_variables = {}

        tk.Label(
            master=self.parent_frame,
            text="Conditions for Static Stabilty",
            width=ButtonSizes.GUI_BUTTON_WIDTH * 4,
            font=("bold",),
        ).pack(side=tk.TOP)

        self._add_output("Moment Coefficient (0 aoa)")
        self._add_output("Moment Coefficient Positive?")
        self._add_output("C_M Derivative (0 aoa)")
        self._add_output("C_M Derivative Negative?")

        tk.Label(
            master=self.parent_frame,
            text="Additional Information",
            width=ButtonSizes.GUI_BUTTON_WIDTH * 4,
            font=("bold",),
        ).pack(side=tk.TOP)

        self._add_output("Volume Coefficient")
        self._add_output("Horizontal Volume Coef")
        self._add_output("Vertical Volume Coef")
        self._add_output("Static Margin")

    def _add_output(self, name):
        subframe = tk.Frame(master=self.parent_frame)
        subframe.pack(side=tk.TOP)

        label = tk.Label(
            master=subframe,
            text=name,
            width=round(ButtonSizes.GUI_BUTTON_WIDTH * 2.5),
        )
        label.pack(side=tk.LEFT)

        string_var = tk.StringVar()
        string_var.set("0")

        value_label = tk.Label(
            master=subframe,
            width=ButtonSizes.GUI_BUTTON_WIDTH,
            textvariable=string_var,
        )
        value_label.pack(side=tk.RIGHT)

        self.display_variables[name] = string_var

    def refresh(self):
        
        static_margin = self._calc_static_margin()
        
        self.display_variables["Static Margin"].set(f"{static_margin:.3f}")

    def _calc_static_margin(self):
        return 0

