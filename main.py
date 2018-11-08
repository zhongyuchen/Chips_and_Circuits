import numpy as np

# grid size
ROW = 13
COL = 18
LAYER = 8

# Print #1
gates = [(1, 1), (1, 6), (1, 10), (1, 15), (2, 3),
         (2, 12), (2, 14), (3, 12), (4, 8), (5, 1),
         (5, 4), (5, 11), (5, 16), (7, 13), (7, 16),
         (8, 2), (8, 6), (8, 9), (8, 11), (8, 15),
         (9, 1), (10, 2), (10, 9), (11, 1), (11, 12)]

# data structure
class chip:
    line_cnt = 0
    grid = np.zeros([LAYER, ROW, COL])
    gate_list = []
    gate_grid = np.zeros([ROW, COL])

    def __init__(self, gate_list):
        self.gate_list = gate_list
        for gate in gate_list:
            self.gate_grid[gate] = 1


chip = chip(gates)

