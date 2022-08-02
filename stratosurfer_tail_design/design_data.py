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
class FlatSection:
    c0: float
    c1: float
    c2: float
    c3: float

@dataclass
class DesignData:
    airfoil: Airfoil
    tail_dimensions: TailDimensions
    tail_position: TailPosition
    flat_section: FlatSection

    @classmethod
    def from_dict(cls, raw_data):
        flat_section_dict = raw_data.get("flat_section", {
                "c0" : 0.1,
                "c1" : 0.2,
                "c2" : 0.4,
                "c3" : 0.5,
            }
        )
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
            ),
            flat_section = FlatSection(
                c0 = flat_section_dict["c0"],
                c1 = flat_section_dict["c1"],
                c2 = flat_section_dict["c2"],
                c3 = flat_section_dict["c3"]
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
            },
            "flat_section": {
                "c0": self.flat_section.c0,
                "c1": self.flat_section.c1,
                "c2": self.flat_section.c2,
                "c3": self.flat_section.c3,
            }
        }
