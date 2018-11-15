import numpy as np


class chip:
    # data structure
    line = 0
    grid = []
    gate = []

    def __init__(self, size, gatelist):
        # line number
        self.line = 0
        # 3D grid -> -1: gate, 0: available, > 0: line number
        self.grid = np.zeros([size[0], size[1], size[2]])
        for gate in gatelist:
            self.grid[0][gate[0]][gate[1]] = -1
        # list of the gates' coordinates
        self.gate = gatelist
