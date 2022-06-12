import yaml
import numpy as np

TAIL_DESIGN_FILE = "data/tail-design.json"

def load_tail_design():
    with open(TAIL_DESIGN_FILE, "r") as fid:
        return yaml.load(fid)


def save_tail_design(tail_design:dict):
    with open(TAIL_DESIGN_FILE, "w") as fid:
        yaml.dump(tail_design, fid)


def load_airplane_config():

    with open("data/body-measurements/measurements.yaml", "r") as fid:
        measurements = yaml.load(fid)

    def convert_dim(pos_2d):
        return np.array([0, -pos_2d[0], pos_2d[1]])

    for key, position_2d in measurements["deck"].items():
        measurements["deck"][key] = convert_dim(position_2d)

    for key, position_2d in measurements["tail"].items():
        measurements["tail"][key] = convert_dim(position_2d)

    measurements["gnss mm"] = convert_dim(measurements["gnss mm"])

    measurements["wing"]["leading edge mm"] = convert_dim(measurements["wing"]["leading edge mm"])

    measurements["center of gravity mm"] = np.array(0, measurements["center of gravity mm"], 0)

    return measurements
