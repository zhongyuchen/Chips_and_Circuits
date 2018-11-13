import numpy as np

# data structure
class chip:
    line_cnt = 0
    grid = []
    gate_list = []
    gate_grid = []

    def __init__(self, size, gate_list):
        # 3D grid
        self.grid = np.zeros([size[0], size[1], size[2]])
        # list of the gates' coordinates
        self.gate_list = gate_list
        # gates in 2D
        self.gate_grid = np.zeros([size[1], size[2]])
        for gate in gate_list:
            self.gate_grid[gate] = 1
