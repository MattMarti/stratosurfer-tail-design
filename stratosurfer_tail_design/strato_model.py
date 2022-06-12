import json

import numpy as np


def calc_horizontal_tail_coefficient():
    pass


def calc_perturbation_analysis():
    pass



class StratoModel:

    def __init__(self, filename):
        self.load_model(filename)


    def load_model(self.filename):
        with open(filename, "r") as fid:
            self.settings = json.load(fid)
    

    def calc_forces_and_moments(self: v_freestream):
        pass









def main():
    pass


if __name__ == '__main__':
    main()
