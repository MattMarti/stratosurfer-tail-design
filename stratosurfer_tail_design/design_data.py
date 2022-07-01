import json
import dataclasses

import numpy as np

@dataclasses.dataclass
class Airfoil:
    m: int
    p: int
    t: int

@dataclasses.dataclass
class TailDimensions:
    span: float
    base_chord: float
    tip_chord: float
    sweep: float

@dataclasses.dataclass
class TailPosition:
    pos: np.array
    aoa: float
    dihedral: float

@dataclasses.dataclass
class DesignData:
    airfoil: Airfoil
    tail_dimensions: TailDimensions
    tail_position: TailPosition

    @classmethod
    def from_dict(cls, raw_data):
        return cls(
            airfoil = Airfoil(
                m = raw_data["airfoil"]["m"],
                p = raw_data["airfoil"]["p"],
                t = raw_data["airfoil"]["t"]
            ),
            tail_dimensions = TailDimensions(
                span = raw_data["tail_dimensions"]["span"],
                base_chord = raw_data["tail_dimensions"]["base_chord"],
                tip_chord = raw_data["tail_dimensions"]["tip_chord"],
                sweep = raw_data["tail_dimensions"]["sweep"]
            ),
            tail_position = TailPosition(
                pos = np.array(raw_data["tail_position"]["pos"]),
                aoa = raw_data["tail_position"]["aoa"],
                dihedral = raw_data["tail_position"]["dihedral"]
            )
        )

    def to_dict(self):
            return {
                "airfoil": {
                    "m": self.airfoil.m,
                    "p": self.airfoil.p,
                    "t": self.airfoil.t,
                },
                "tail_dimensions": {
                    "span": self.tail_dimensions.span,
                    "base_chord": self.tail_dimensions.base_chord,
                    "tip_chord": self.tail_dimensions.tip_chord,
                    "sweep": self.tail_dimensions.sweep,
                },
                "tail_position": {
                    "pos": self.tail_position.pos.tolist(),
                    "aoa": self.tail_position.aoa,
                    "dihedral": self.tail_position.dihedral,
                }
            }
