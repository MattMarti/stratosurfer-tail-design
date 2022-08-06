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


class DimensionsPlotFrame(InfoFrameBase):

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

    def _get_flat_constrained_surface(self):
        td = self.design_data.tail_dimensions
        fs = self.design_data.flat_section
        x = [
            td.base_chord * fs.c1,
            td.sweep + (td.base_chord - td.tip_chord) + td.tip_chord * fs.c1,
            np.nan,
            td.base_chord * fs.c2,
            td.sweep + (td.base_chord - td.tip_chord) + td.tip_chord * fs.c2,
        ]
        y = [
            0,
            td.span,
            np.nan,
            0,
            td.span,
        ]
        return x, y

    def _get_servo_points(self):
        sp = self.design_data.servo_parameters

        servo_width = 24
        servo_height = 23
        control_horn_x_offset = 10
        control_horn_y_offset = 5

        x = [
            sp.x,
            sp.x,
            sp.x + servo_width,
            sp.x + servo_width,
            sp.x,
            np.nan,
            sp.x + control_horn_x_offset,
            sp.x + control_horn_x_offset + sp.ctrl_horn_len,
        ]
        y = [
            sp.y,
            sp.y + servo_height,
            sp.y + servo_height,
            sp.y,
            sp.y,
            np.nan,
            sp.y + servo_height + control_horn_y_offset,
            sp.y + servo_height + control_horn_y_offset,
        ]
        return x, y

    def _get_elevator_flap_points(self):
        td = self.design_data.tail_dimensions
        ef = self.design_data.elevator_flap
        slope = td.sweep / td.span
        x = [
            td.base_chord,
            td.base_chord - ef.width,
            td.base_chord - ef.width,
            td.base_chord,
        ]
        y = [
            ef.span_begin,
            ef.span_begin,
            ef.span_begin + ef.span,
            ef.span_begin + ef.span,
        ]
        for i in range(len(x)):
            x[i] += y[i] * slope
        return x, y


    def refresh(self):
        self.ax.clear()

        x, y = self._get_surface()
        self.ax.plot(x, y, color="b")

        x_flat, y_flat = self._get_flat_constrained_surface()
        self.ax.plot(x_flat, y_flat)

        x_servo, y_servo = self._get_servo_points()
        self.ax.plot(x_servo, y_servo, color="red")

        x_ef, y_ef = self._get_elevator_flap_points()
        self.ax.plot(x_ef, y_ef)

        apply_pretty_plot_settings(self.ax)
        self.ax.axis("equal")
        self.fig.canvas.draw()


class AirfoilPlotFrame(InfoFrameBase):

    def __init__(self, parent_frame:tk.Frame, design_data:DesignData):
        super().__init__(parent_frame, design_data)

        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.airfoil_ax = self.fig.add_subplot(2, 1, 1)
        self.flatness_ax = self.fig.add_subplot(2, 1, 2)

        canvas = FigureCanvasTkAgg(self.fig, master=parent_frame)
        canvas.draw()
        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, parent_frame, pack_toolbar=False)
        toolbar.update()
        toolbar.pack(side=tk.TOP, fill=tk.X)

    def refresh(self):
        x_flatness, y_flatness = self._get_flat_surface_weights()
        self.flatness_ax.clear()
        self.flatness_ax.plot(x_flatness, y_flatness)
        apply_pretty_plot_settings(self.flatness_ax)

        x_airfoil, y_airfoil = self._get_airfoil_surface()

        weights = np.concatenate((y_flatness[::-1], y_flatness), axis=0)
        signs = np.ones(weights.shape)
        signs[y_airfoil < 0] = -1
        y = (1 - weights) * y_airfoil +  weights * signs * (0.5 * 0.01 * self.design_data.airfoil.t)

        self.airfoil_ax.clear()
        self.airfoil_ax.plot(x_airfoil, y)
        self.airfoil_ax.axis("equal")
        apply_pretty_plot_settings(self.airfoil_ax)

        self.fig.canvas.draw()

    @property
    def _num_points(self):
        return 50000

    def _get_flat_surface_weights(self):
        c = np.linspace(0, 1, int(self._num_points/2))
        y = np.zeros(c.shape)

        flat_params = self.design_data.flat_section

        rising_slope = (1 - 0) / (flat_params.c1 - flat_params.c0)
        indeces = np.logical_and(flat_params.c0 < c, c < flat_params.c1)
        y[indeces] = rising_slope * (c[indeces] - flat_params.c0)

        y[np.logical_and(flat_params.c1 < c, c < flat_params.c2)] = 1

        descending_slope = (0 - 1) / (flat_params.c3 - flat_params.c2)
        indeces = np.logical_and(flat_params.c2 < c, c < flat_params.c3)
        y[indeces] = 1 + descending_slope * (c[indeces] - flat_params.c2)

        return c, y

    def _get_airfoil_surface(self):
        airfoil = NacaFourDigitAirfoil(
            self.design_data.airfoil.m,
            self.design_data.airfoil.p,
            self.design_data.airfoil.t
        )
        xu = np.linspace(1, 0, int(self._num_points/2))
        xu, yu = airfoil.get_upper(xu)
        xl = np.linspace(0, 1, int(self._num_points/2))
        xl, yl = airfoil.get_lower(xl)
        return np.concatenate((xu,xl)), np.concatenate((yu, yl))

