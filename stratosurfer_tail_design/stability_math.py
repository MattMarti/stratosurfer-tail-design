import numpy as np

from . import DesignData


def calc_zero_aoa_moment_coefficient(dd:DesignData):
    aoa = 0
    wing_moment_coeff = calc_wing_total_moment_coeff(dd, aoa)
    tail_moment_coeff = calc_tail_total_moment_coeff(dd, aoa)
    return wing_moment_coeff + tail_moment_coeff


def calc_wing_total_moment_coeff(dd:DesignData, aoa:float):
    c_m = 0 # TODO How to get from XFOIL? I should probably cache these values
    c_f = 0 # TODO Might as well get from XFOIL
    c_d = 0 # TODO Might as well get from XFOIL

    return 0


def calc_tail_total_moment_coeff(dd:DesignData, aoa:float):
    return 0

