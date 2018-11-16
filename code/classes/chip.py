import numpy as np
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import random

import sys
sys.path.append('../')
from algorithms.readjson import readjson

plotly.tools.set_credentials_file(username='zhongyuchen', api_key='MVlLKp3ujiU1bFQImbKP')


MARKER = dict(size=3)
LINE = dict(size=3)


class chip:
    # data structure
    cnt_wire = 0
    grid = []
    gate = []
    wire = []
    used_wired = []
    size = []

    def __init__(self, size, gatelist):
        # line number
        self.cnt_wire = 0
        self.wire = []
        # 3D grid -> -1: gate, 0: available, > 0: line number

        self.grid = np.zeros([size[0], size[1], size[2]])
        self.size = size
        # size[0] shows level, size[1] shows row, size[2] shows column

        used_wired = [[[0 for i in range(size[2])] for j in range(size[1])] for k in range(size[0])]

        for gate in gatelist:
            self.grid[0][gate[0]][gate[1]] = -1
        # list of the gates' coordinates
        self.gate = gatelist

    def plot(self):
        data = []
        # gates
        i = 1
        for g in self.gate:
            gate = go.Scatter3d(
                x=[g[0]],
                y=[g[1]],
                z=[0],
                marker=dict(size=8, color='#000000'),
                name='Gate ' + str(i)
            )
            i += 1
            data.append(gate)

        """
        # wires
        wire = go.Scatter3d(
            x=range(0, len(self.grid[0][0])),
            y=range(0, len(self.grid[0])),
            z=range(0, len(self.grid)),
            marker=MARKER,
            line=LINE,
            name='wire1'
        )
        """

        # layout
        layout = dict(
            width=800,
            height=700,
            autosize=False,
            title='chip',
            scene=dict(
                xaxis=dict(
                    gridcolor='rgb(255, 255, 255)',
                    zerolinecolor='rgb(255, 255, 255)',
                    showbackground=True,
                    backgroundcolor='rgb(230, 230,230)',
                    range=(0, len(self.grid[0]))
                ),
                yaxis=dict(
                    gridcolor='rgb(255, 255, 255)',
                    zerolinecolor='rgb(255, 255, 255)',
                    showbackground=True,
                    backgroundcolor='rgb(230, 230,230)',
                    range=(0, len(self.grid[0][0]))
                ),
                zaxis=dict(
                    gridcolor='rgb(255, 255, 255)',
                    zerolinecolor='rgb(255, 255, 255)',
                    showbackground=True,
                    backgroundcolor='rgb(230, 230,230)',
                    range=(0, len(self.grid))
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
        py.plot(fig, filename='test-3d', height=700, validate=False)

    def addline(self, st, en):
        # add a line

        fx = [-1, 0, 0, 1]
        fy = [0, 1, -1, 0]

        queue = []
        # tuple with 4 elements(level, x, y, cost, last) presents level, x-axis, y-axis and last point
        left = 0
        right = 1
        queue.append([0, self.gate[st][0], self.gate[st][1], -1])

        visit = [[[0 for i in range(self.size[2])] for j in range(self.size[1])] for k in range(self.size[0])]

        for i in range(self.size[0]):
            for j in range(self.size[1]):
                for k in range(self.size[2]):
                    visit[i][j][k] = 0

        for i in range(len(self.gate)):
            visit[0][self.gate[i][0]][self.gate[i][1]] = 1
            self.used_wired[0][self.gate[i][0]][self.gate[i][1]] = 0
        visit[0][self.gate[en][0]][self.gate[en][1]] = 0

        while left < right:
            u = queue[left]
            if u[0] == 0 and u[1] == self.gate[en][0] and u[2] == self.gate[en][1]:
                current_cost = 0
                self.cnt_wire = self.cnt_wire + 1
                self.used_wired[u[0]][u[1]][u[2]] = self.cnt_wire
                tmp = u[3]
                while tmp != -1:
                    self.used_wired[queue[tmp][0]][queue[tmp][1]][queue[tmp][2]] = self.cnt_wire
                    current_cost = current_cost + 1
                    tmp = queue[tmp][3]

                return current_cost

            # 4 directions in same level
            for i in range(4):
                tx = u[1] + fx[i]
                ty = u[2] + fy[i]
                if tx < 0 or tx >= self.size[1] or ty < 0 or ty >= self.size[2]:
                    continue

                if visit[u[0]][tx][ty] == 0 and self.used_wired[u[0]][tx][ty] == 0:
                    queue.append([u[0], tx, ty, left])
                    visit[u[0]][tx][ty] = 1
                    right = right + 1

            # down level
            if u[0] > 0:
                if visit[u[0] - 1][u[1]][u[2]] == 0 and self.used_wired[u[0] - 1][u[1]][u[2]] == 0:
                    queue.append([u[0] - 1, u[1], u[2], left])
                    visit[u[0] - 1][u[1]][u[2]] = 1
                    right = right + 1

            # up level
            if u[0] < 6:
                if visit[u[0] + 1][u[1]][u[2]] == 0 and self.used_wired[u[0] + 1][u[1]][u[2]] == 0:
                    queue.append([u[0] + 1, u[1], u[2], left])
                    visit[u[0] + 1][u[1]][u[2]] = 1
                    right = right + 1

            left = left + 1
        return -1

    def delline(self, lab_number):
        # delete a line

        for i in range(self.size[0]):
            for j in range(self.size[1]):
                for k in range(self.size[2]):
                    if self.used_wired[i][j][k] == lab_number:
                        self.used_wired[i][j][k] = 0
        self.wire.remove(lab_number)


    def find_solution(self):

        fx = [-1, 0, 0, 1]
        fy = [0, 1, -1, 0]

        random.shuffle(self.gate)

        ans = 0
        for pair_gate in self.gate:
            cost = self.addline(self, pair_gate[0], pair_gate[1])
            if cost == -1:
                for i in range(4):
                    tx = pair_gate[0] + fx[i]
                    ty = pair_gate[0] + fy[i]

                    if tx < 0 or tx >= self.size[1] or ty < 0 or ty >= self.size[2]:
                        continue

                    self.delline(self, self.used_wired[0][tx][ty])
                    self.addline(self, pair_gate[0], pair_gate[1])

                    '''TODO'''



if __name__ == "__main__":
    size1 = readjson("gridsizes.json", 1)
    gate1 = readjson("gatelists.json", 1)
    chip = chip(size1, gate1)
    chip.plot()
