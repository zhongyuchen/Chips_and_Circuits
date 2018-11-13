import numpy as np


# grid size: [layers, rows, cols]
SIZE_1 = [8, 13 ,18]
SIZE_2 = [8, 17, 18]

# Print 1
gates_1 = [(1, 1), (1, 6), (1, 10), (1, 15), (2, 3),
           (2, 12), (2, 14), (3, 12), (4, 8), (5, 1),
           (5, 4), (5, 11), (5, 16), (7, 13), (7, 16),
           (8, 2), (8, 6), (8, 9), (8, 11), (8, 15),
           (9, 1), (10, 2), (10, 9), (11, 1), (11, 12)]
# Print 2
gates_2 = [(1, 1), (1, 6), (1, 10), (1, 15), (2, 3),
           (2, 12), (2, 14), (3, 1), (3, 6), (3, 12),
           (3, 15), (4, 2), (4, 8), (5, 1), (5, 4),
           (5, 10), (5, 11), (5, 16), (6, 2), (6, 7),
           (6, 10), (6, 12), (6, 15), (7, 6), (7, 13),
           (7, 16), (8, 6), (8, 7), (8, 9), (8, 11),
           (8, 15), (9, 1), (9, 6), (10, 9), (11, 12),
           (12, 2), (12, 4), (12, 7), (12, 10), (12, 15),
           (13, 9), (13, 13), (14, 4), (14, 6), (15, 1),
           (15, 6), (15, 8), (15, 11), (15, 13), (15, 16)]


# data structure
class Chip:
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


if __name__ == "__main__":
    # chip
    chip = Chip(SIZE_1, gates_1)