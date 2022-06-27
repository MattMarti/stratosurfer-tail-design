from dataclasses import dataclass

import numpy as np


@dataclass
class Airfoil:
    m: int
    p: int
    t: int

@dataclass
class TailDimensions:
    span: float
    base_chord: float
    tip_chord: float
    sweep: float

@dataclass
class TailPosition:
    pos: np.array
    aoa: float
    dihedral: float

@dataclass
class DesignData:
    airfoil: Airfoil
    tail_dimensions: TailDimensions
    tail_position: TailPosition
