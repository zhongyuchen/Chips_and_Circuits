import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import json
import random

import sys
sys.path.append('../')
from algorithms.astar_spfa import AstarSpfa

plotly.tools.set_credentials_file(username='chipsandcircuits', api_key='9A2KpJpwzbsL04AhXSTY')


RESULTS_PATH = "../../results/"

four_direction = [[1, 0], [-1, 0], [0, 1], [0, -1]]
diagonal_four_direction = [[-1, -1], [-1, 1], [1, -1], [1, 1]]
enclosure_level_2 = [[-2, 2], [-1, 2], [0, 2], [1, 2],
                     [2, 2], [2, 1], [2, 0], [2, -1],
                     [2, -2], [1, -2], [0, -2], [-1, -2],
                     [-2, -2], [-2, -1], [-2, 0], [-2, 1]]


class Chip:

    def __init__(self, size, gatelist, netlist):

        # Line list.
        self.wire = []

        self.net = netlist

        # Grid -> -1: gate, 0: available, > 0: wire number.
        self.grid = [[[0 for _ in range(size[2])] for _ in range(size[1])] for _ in range(size[0])]

        # Size[0] shows level, size[1] shows row, size[2] shows column.
        self.size = size

        self.used_wired = [[[-1 for _ in range(size[2])] for _ in range(size[1])] for _ in range(size[0])]

        self.map_line = [[] for _ in range(len(self.net))]

        for gate in gatelist:
            self.grid[0][gate[0]][gate[1]] = -1

        # List of the gates' coordinates.
        self.gate = gatelist

        # Use manhattan_distance to determine the grid_value.
        self.grid_value = [[[0 for _ in range(self.size[2])] for _ in range(self.size[1])] for _ in range(self.size[0])]
        self.manhattan_distance_weight()

    def clean(self):
        # Erase everything except size, gates and netlist(the same order)

        self.wire = []

        self.grid = [[[0 for _ in range(self.size[2])] for _ in range(self.size[1])] for _ in range(self.size[0])]

        self.used_wired = [[[-1 for _ in range(self.size[2])] for _ in range(self.size[1])] for _ in range(self.size[0])]

        self.map_line = [[] for _ in range(len(self.net))]

        for gate in self.gate:
            self.grid[0][gate[0]][gate[1]] = -1

        self.grid_value = [[[0 for _ in range(self.size[2])] for _ in range(self.size[1])] for _ in range(self.size[0])]

        self.manhattan_distance_weight()

    def manhattan_distance_weight(self):
        # Calculate the value of each grid.

        def mapping(distance):
            return - distance + 50

        def manhattan_distance(point, gate):
            return point[0] + abs(point[1] - gate[0]) + abs(point[2] - gate[1])

        for i in range(self.size[0]):
            for j in range(self.size[1]):
                for k in range(self.size[2]):
                    for gate in self.gate:
                        self.grid_value[i][j][k] += mapping(manhattan_distance([i, j, k], gate))

    def plot(self, figname=""):
        # visualization
        data = []
        # gates
        i = 1
        for g in self.gate:
            gate = go.Scatter3d(
                x=[g[0]],
                y=[g[1]],
                z=[0],
                mode="markers+text",
                marker=dict(size=8, color='#000000'),
                text=[str(i)],
                name='G' + str(i)
            )
            i += 1
            data.append(gate)

        # wires
        wires = self.output_line()
        i = 1
        for w in wires:
            wire = go.Scatter3d(
                x=w[0],
                y=w[1],
                z=w[2],
                mode="markers+lines",
                marker=dict(size=3),
                name='W' + str(i)
            )
            i += 1
            data.append(wire)

        # layout
        layout = dict(
            # width=800,
            # height=700,
            # autosize=False,
            title='chip (cost: ' + str(self.cost()) + ')',
            scene=dict(
                xaxis=dict(
                    gridcolor='rgb(255, 255, 255)',
                    zerolinecolor='rgb(255, 255, 255)',
                    showbackground=True,
                    backgroundcolor='rgb(230, 230,230)',
                    range=(0, self.size[1] - 1),
                    dtick=1
                ),
                yaxis=dict(
                    gridcolor='rgb(255, 255, 255)',
                    zerolinecolor='rgb(255, 255, 255)',
                    showbackground=True,
                    backgroundcolor='rgb(230, 230,230)',
                    range=(0, self.size[2] - 1),
                    dtick=1
                ),
                zaxis=dict(
                    gridcolor='rgb(255, 255, 255)',
                    zerolinecolor='rgb(255, 255, 255)',
                    showbackground=True,
                    backgroundcolor='rgb(230, 230,230)',
                    range=(0, self.size[0] - 1),
                    dtick=1
                ),
                camera=dict(
                    up=dict(
                        x=0,
                        y=0,
                        z=1
                    ),
                    eye=dict(
                        x=-1.7428,
                        y=1.0707,
                        z=0.7100,
                    )
                ),
                aspectratio=dict(x=1, y=1, z=0.7),
                aspectmode='manual'
            ),
        )

        # figure
        fig = go.Figure(data=data, layout=layout)
        # plot figure
        if figname == "":
            filename = "chip-3d"
        else:
            filename = figname
        py.plot(fig, filename=filename, validate=False)

    def calc_single_cost_impact(self, tx, ty, c):
        if tx < 0 or tx >= self.size[1] or ty < 0 or ty >= self.size[2]:
            return 0
        if self.grid[0][tx][ty] == -1:
            return c
        else:
            return 0

    def output_line(self):
        """
            Get the ordered coordinates of all the wires.
            For visualization.
        """
        line_list = []

        for i in range(len(self.net)):
            line_x = []
            line_y = []
            line_z = []

            for cor in self.map_line[i]:
                line_z.append(cor[0])
                line_x.append(cor[1])
                line_y.append(cor[2])

            line_list.append([line_x, line_y, line_z])

        return line_list

    def addline(self, net_num):
        """
            Try to add a line between the pair of certain net.
            Use the Breadth-First-Search try to find a path.
        """

        st = self.net[net_num][0]
        en = self.net[net_num][1]

        queue = []
        # tuple with 4 elements(level, x, y, cost, last) presents level, x-axis, y-axis and last point
        left = 0
        right = 1
        queue.append([0, self.gate[st][0], self.gate[st][1], -1])

        visit = [[[0 for _ in range(self.size[2])] for _ in range(self.size[1])] for _ in range(self.size[0])]

        for i in range(self.size[0]):
            for j in range(self.size[1]):
                for k in range(self.size[2]):
                    visit[i][j][k] = 0

        for i in range(len(self.gate)):
            visit[0][self.gate[i][0]][self.gate[i][1]] = 1
            self.used_wired[0][self.gate[i][0]][self.gate[i][1]] = -1
        visit[0][self.gate[en][0]][self.gate[en][1]] = 0

        while left < right:
            u = queue[left]
            if u[0] == 0 and u[1] == self.gate[en][0] and u[2] == self.gate[en][1]:
                current_cost = 0
                tmp = u[3]
                self.map_line[net_num].append([u[0], u[1], u[2]])
                while tmp != -1:
                    if self.grid[queue[tmp][0]][queue[tmp][1]][queue[tmp][2]] != -1:
                        self.used_wired[queue[tmp][0]][queue[tmp][1]][queue[tmp][2]] = net_num
                        self.map_line[net_num].append([queue[tmp][0], queue[tmp][1], queue[tmp][2]])
                    current_cost = current_cost + 1
                    tmp = queue[tmp][3]
                self.map_line[net_num].append([0, self.gate[st][0], self.gate[st][1]])

                return current_cost

            # up level
            if u[0] < 6:
                if visit[u[0] + 1][u[1]][u[2]] == 0 and self.used_wired[u[0] + 1][u[1]][u[2]] == -1:
                    queue.append([u[0] + 1, u[1], u[2], left])
                    visit[u[0] + 1][u[1]][u[2]] = 1
                    right = right + 1

            # 4 directions in same level
            for i in range(4):
                tx = u[1] + four_direction[i][0]
                ty = u[2] + four_direction[i][1]
                if tx < 0 or tx >= self.size[1] or ty < 0 or ty >= self.size[2]:
                    continue

                if visit[u[0]][tx][ty] == 0 and self.used_wired[u[0]][tx][ty] == -1:
                    queue.append([u[0], tx, ty, left])
                    visit[u[0]][tx][ty] = 1
                    right = right + 1

            # down level
            if u[0] > 0:
                if visit[u[0] - 1][u[1]][u[2]] == 0 and self.used_wired[u[0] - 1][u[1]][u[2]] == -1:
                    queue.append([u[0] - 1, u[1], u[2], left])
                    visit[u[0] - 1][u[1]][u[2]] = 1
                    right = right + 1

            left = left + 1
        return -1

    def delline(self, lab_number):
        """
            Delete a line of the certain pair, defined by 'lab_number'.
            Clear all the changes of this line.
        """

        for i in range(self.size[0]):
            for j in range(self.size[1]):
                for k in range(self.size[2]):
                    if self.used_wired[i][j][k] == lab_number:
                        self.used_wired[i][j][k] = -1

        self.map_line[lab_number] = []

    def del_and_add(self, delline_num, addline_num):
        """
            There are two different number of net('delline_num' and 'addline_num' must be different).
            Desires to delete the 'delline_num' line, and add the 'addline_num' line.
                After that, urges to add the 'delline_num' line, to check if the swap is effective.
            If find an alternative solution, the return number will be 0. Other cases, return 1.
        """

        if delline_num == -1:
            # Do not need to delete anything.
            return 1

        self.delline(delline_num)

        # The cost of each addline function presents whether it can add a line in such a chip.
        cost1 = self.addline(addline_num)
        cost2 = self.addline(delline_num)

        if cost1 == -1 or cost2 == -1:
            # Cannot find an alternative solution.

            # Back to last status.
            if cost1 != -1:
                self.delline(addline_num)
            if cost2 != -1:
                self.delline(delline_num)
            self.addline(delline_num)

            return 1
        else:
            # Find an alternative solution.
            return 0

    def cost(self):
        """
            Calculate the cost of total chip.
            Prepare for the heuristic algorithms which will somehow reduce the cost.
        """

        summary = 0
        for wire in self.map_line:
            if len(wire):
                summary += len(wire) - 1
        return summary

    def save(self, filename):
        # Save the chip as a file.

        filename = RESULTS_PATH + filename
        dic = {"grid": self.grid,
               "gate": self.gate,
               "net": self.net,
               "wire": self.wire,
               "used_wired": self.used_wired,
               "size": self.size,
               "map_line": self.map_line,
               "grid_value": self.grid_value}
        with open(filename, 'w') as f:
            json.dump(dic, f, indent=4)

    def load(self, filename):
        # Load a chip from the file.

        filename = RESULTS_PATH + filename
        with open(filename, 'r') as f:
            dic = json.load(f)
        self.size = dic["size"]
        self.gate = dic["gate"]
        self.net = dic["net"]
        self.grid = dic["grid"]
        self.wire = dic["wire"]
        self.used_wired = dic["used_wired"]
        self.map_line = dic["map_line"]
        self.grid_value = dic["grid_value"]

    def random_wires(self, amount):
        # randomly select a certain amount of wires
        length = len(self.net)
        wires = []
        for i in range(amount):
            wires.append(random.randint(0, length - 1))
        return wires
