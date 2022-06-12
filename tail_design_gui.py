import tkinter as tk

import numpy as np

from matplotlib.backends.backend_tkagg import (
    FigureCanvasTkAgg, NavigationToolbar2Tk)
from matplotlib.backend_bases import key_press_handler
from matplotlib.figure import Figure

from stratosurfer_tail_design.submodules.airfoil_defs.naca_four_digit_airfoil import NacaFourDigitAirfoil


GUI_BUTTON_WIDTH = 10
GUI_BUTTON_PADDING = 20


class AirfoilDesignControlFrame:

    def __init__(self, parent_frame):
        naca_digit_label = tk.Label(
            master=parent_frame,
            text="Tail Aifoil\nNACA 4-digit")
        naca_digit_label.pack(side=tk.TOP)

        m_frame = tk.Frame(master=parent_frame)
        m_frame.pack(side=tk.TOP)

        m_label = tk.Label(
            m_frame,
            text='M',
            width=round(GUI_BUTTON_WIDTH/2))
        m_label.pack(side=tk.LEFT)

        self.m_entry = tk.Entry(
            m_frame,
            width=GUI_BUTTON_WIDTH)
        self.m_entry.pack(side=tk.RIGHT)
        self.m_entry.insert(0, "4")

        p_frame = tk.Frame(master=parent_frame)
        p_frame.pack(side=tk.TOP)

        p_label = tk.Label(
            p_frame,
            text='P',
            width=round(GUI_BUTTON_WIDTH/2))
        p_label.pack(side=tk.LEFT)

        self.p_entry = tk.Entry(
            p_frame,
            width=GUI_BUTTON_WIDTH)
        self.p_entry.pack(side=tk.RIGHT)
        self.p_entry.insert(0, "4")

        t_frame = tk.Frame(master=parent_frame)
        t_frame.pack(side=tk.TOP)

        t_label = tk.Label(
            t_frame,
            text='T',
            width=round(GUI_BUTTON_WIDTH/2))
        t_label.pack(side=tk.LEFT)

        self.t_entry = tk.Entry(
            t_frame,
            width=GUI_BUTTON_WIDTH)
        self.t_entry.pack(side=tk.RIGHT)
        self.t_entry.insert(0, "10")

    @property
    def m(self):
        return int(self.m_entry.get())

    @property
    def p(self):
        return int(self.p_entry.get())

    @property
    def t(self):
        return int(self.t_entry.get())

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


class AirfoilPlotter:

    def __init__(self, parent_frame):
        self.fig = Figure(figsize=(5,4), dpi=100)
        self.ax = self.fig.add_subplot(111)

        canvas = FigureCanvasTkAgg(self.fig, master=parent_frame)
        canvas.draw()

        toolbar = NavigationToolbar2Tk(canvas, parent_frame, pack_toolbar=False)
        toolbar.update()

        canvas.get_tk_widget().pack(side=tk.TOP, fill=tk.BOTH, expand=1)
        toolbar.pack(side=tk.TOP, fill=tk.X)

    def refresh_plot(self, airfoil_design_frame):
        xu, yu = airfoil_design_frame.get_upper_surface()
        xl, yl = airfoil_design_frame.get_lower_surface()

        self.ax.clear()
        self.ax.plot(np.concatenate((xu,xl)), np.concatenate((yu, yl), 0), color="orange")
        self.ax.axis('equal')
        self.ax.grid(which='major')
        self.ax.minorticks_on()
        self.ax.grid(which='minor', linestyle='--', linewidth=0.3)
        self.fig.canvas.draw()


class GuiManager:

    def __init__(self):
        self.plot_frames = {}
        self.root = tk.Tk()
        self.gui_data = None

        self.root.title('Airfoil Plotter')
        self.initialize_design_control_frame()
        self.initialize_figure()
        self.refresh_plot()

    def run(self):
        self.root.mainloop()

    def quit(self):
        self.root.quit()
        self.root.destroy()

    def refresh_plot(self):
        self.plotter.refresh_plot(self.plot_frames["airfoil frame"])

    def initialize_figure(self):
        self.figure_frame = tk.Frame(master=self.root)
        self.figure_frame.pack(side=tk.TOP)
        self.plotter = AirfoilPlotter(self.figure_frame)

        refresh_button = tk.Button(
            master=self.figure_frame,
            text="Refresh",
            width=GUI_BUTTON_WIDTH,
            command=lambda: self.refresh_plot()
        )
        refresh_button.pack(side=tk.TOP, anchor=tk.NW)

    def initialize_design_control_frame(self):

        # Settings
        design_control_frame = tk.Frame(master=self.root)
        design_control_frame.pack(side=tk.BOTTOM, anchor=tk.NE)

        # Digit Settings
        naca_digit_frame = tk.Frame(
            master=design_control_frame,
            highlightbackground="grey",
            highlightthickness=1)
        naca_digit_frame.pack(side=tk.RIGHT)
        airfoil_design_frame = AirfoilDesignControlFrame(naca_digit_frame)
        self.plot_frames["airfoil frame"] = airfoil_design_frame


def main():
    gui = GuiManager()
    gui.run()


if __name__ == '__main__':
    main()
