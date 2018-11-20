import numpy as np
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import random

import sys
sys.path.append("..")
from algorithms.readjson import readjson

plotly.tools.set_credentials_file(username='zhongyuchen', api_key='MVlLKp3ujiU1bFQImbKP')


MARKER = dict(size=3)
LINE = dict(size=3)
four_direction = [[1, 0], [-1, 0], [0, 1], [0, -1]]


class chip:
    # data structure
    # cnt_wire = 0
    grid = []
    gate = []
    net = []
    wire = []
    used_wired = []
    size = []

    def __init__(self, size, gatelist, netlist):
        # line number
        # self.cnt_wire = 0
        self.wire = []
        # 3D grid -> -1: gate, 0: available, > 0: wire number

        self.net = netlist

        self.grid = np.zeros([size[0], size[1], size[2]])
        self.size = size
        # size[0] shows level, size[1] shows row, size[2] shows column

        self.used_wired = [[[-1 for i in range(size[2])] for j in range(size[1])] for k in range(size[0])]

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
                    range=(0, self.size[1]),
                    dtick=1
                ),
                yaxis=dict(
                    gridcolor='rgb(255, 255, 255)',
                    zerolinecolor='rgb(255, 255, 255)',
                    showbackground=True,
                    backgroundcolor='rgb(230, 230,230)',
                    range=(0, self.size[2]),
                    dtick=1
                ),
                zaxis=dict(
                    gridcolor='rgb(255, 255, 255)',
                    zerolinecolor='rgb(255, 255, 255)',
                    showbackground=True,
                    backgroundcolor='rgb(230, 230,230)',
                    range=(0, self.size[0]),
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
        py.plot(fig, filename='chip-3d', height=700, validate=False)

    def addline(self, gate_num):

        st = self.net[gate_num][0]
        en = self.net[gate_num][1]
        # add a line

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
            self.used_wired[0][self.gate[i][0]][self.gate[i][1]] = -1
        visit[0][self.gate[en][0]][self.gate[en][1]] = 0

        while left < right:
            u = queue[left]
            if u[0] == 0 and u[1] == self.gate[en][0] and u[2] == self.gate[en][1]:
                current_cost = 0
                tmp = u[3]
                while tmp != -1:
                    if self.grid[queue[tmp][0]][queue[tmp][1]][queue[tmp][2]] != -1:
                        self.used_wired[queue[tmp][0]][queue[tmp][1]][queue[tmp][2]] = gate_num
                    current_cost = current_cost + 1
                    tmp = queue[tmp][3]

                return current_cost

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

            # up level
            if u[0] < 6:
                if visit[u[0] + 1][u[1]][u[2]] == 0 and self.used_wired[u[0] + 1][u[1]][u[2]] == -1:
                    queue.append([u[0] + 1, u[1], u[2], left])
                    visit[u[0] + 1][u[1]][u[2]] = 1
                    right = right + 1

            left = left + 1
        return -1

    def output_map(self, f):
        for i in range(2):
            print("nn", file=f, end=" ")
            for k in range(self.size[2]):
                print("%02d" % k, file=f, end=" ")
            print(file=f)

            for j in range(self.size[1]):
                print("%02d" % j, file=f, end=" ")
                for k in range(self.size[2]):
                    if self.used_wired[i][j][k] >= 0:
                        print("%02d" % self.used_wired[i][j][k], file=f, end=" ")
                    else:
                        print(self.used_wired[i][j][k], file=f, end=" ")
                print(file=f)

            print(file=f)

    def delline(self, lab_number):
        # delete a line

        for i in range(self.size[0]):
            for j in range(self.size[1]):
                for k in range(self.size[2]):
                    if self.used_wired[i][j][k] == lab_number:
                        self.used_wired[i][j][k] = -1

    def del_and_add(self, delline_num, addline_num):
        # find a solution, return 0
        # else return 1

        if delline_num == -1:
            # do not need to delete anything
            return 1

        self.delline(delline_num)
        cost1 = self.addline(addline_num)
        cost2 = self.addline(delline_num)
        if cost1 == -1 or cost2 == -1:
            # cannot find a replaced solution

            # back to last status
            if cost1 != -1:
                self.delline(addline_num)
            if cost2 != -1:
                self.delline(delline_num)
            self.addline(delline_num)
            return 1
        else:
            return 0

    def output_line(self):
        # output each line to be visualized

        line_list = []
        line_x = []
        line_y = []
        line_z = []

        visit = [[[0 for i in range(self.size[2])] for j in range(self.size[1])] for k in range(self.size[0])]

        self.output_map(open("data.txt", "w"))

        for i in range(len(self.net)):
            u = [0, self.gate[self.net[i][0]][0], self.gate[self.net[i][0]][1]]
            v = [0, self.gate[self.net[i][1]][0], self.gate[self.net[i][1]][1]]
            while u != v:
                line_z.append(u[0])
                line_x.append(u[1])
                line_y.append(u[2])

                u_is_changed = 0
                for t in range(4):
                    tx = u[1] + four_direction[t][0]
                    ty = u[2] + four_direction[t][1]
                    if self.used_wired[u[0]][tx][ty] == i and \
                            (visit[u[0]][tx][ty] == 0 or self.used_wired[u[0]][tx][ty] == -1):
                        u = [u[0], tx, ty]
                        visit[u[0]][tx][ty] = 1
                        u_is_changed = 1
                        break

                if u_is_changed == 0:
                    if u[0] > 0 and self.used_wired[u[0] - 1][u[1]][u[2]] == i and \
                            (visit[u[0] - 1][u[1]][u[2]] == 0 or self.used_wired[u[0] - 1][u[1]][u[2]] == -1):
                        u = [u[0] - 1, u[1], u[2]]
                        visit[u[0] - 1][u[1]][u[2]] = 1
                        u_is_changed = 1

                if u_is_changed == 0:
                    if u[0] < 6 and self.used_wired[u[0] + 1][u[1]][u[2]] == i and \
                            (visit[u[0] + 1][u[1]][u[2]] == 0 or self.used_wired[u[0] + 1][u[1]][u[2]] == -1):
                        u = [u[0] + 1, u[1], u[2]]
                        visit[u[0] + 1][u[1]][u[2]] = 1
                        u_is_changed = 1

                if u_is_changed == 0:
                    print("error")
                    return []

            line_z.append(v[0])
            line_x.append(v[1])
            line_y.append(v[2])

            line_list.append([line_x, line_y, line_z])
            print([line_x, line_y, line_z])

        return line_list

    def find_solution(self):

        random.shuffle(self.net)

        ans = 0
        cnt = 0
        for pair_gate in self.net:
            cost = self.addline(cnt)
            flag_conflict = 0
            # if there is a solution, flag_conflict = 0
            # else flag_conflict = 1

            if cost == -1:

                flag_conflict = 1

                # for pair_gate[0]
                # four points in level 0
                for i in range(4):
                    if flag_conflict == 0:
                        break
                    tx = self.gate[pair_gate[0]][0] + four_direction[i][0]
                    ty = self.gate[pair_gate[0]][1] + four_direction[i][1]

                    if tx < 0 or tx >= self.size[1] or ty < 0 or ty >= self.size[2]:
                        continue

                    gate_num = self.used_wired[0][tx][ty]

                    flag_conflict = self.del_and_add(gate_num, cnt)

                if flag_conflict == 1:
                    # the point in level 1
                    gate_num = self.used_wired[1][self.gate[pair_gate[0]][0]][self.gate[pair_gate[0]][1]]
                    flag_conflict = self.del_and_add(gate_num, cnt)

                # for pair_gate[1]
                if flag_conflict == 1:
                    for i in range(4):
                        if flag_conflict == 0:
                            break
                        tx = self.gate[pair_gate[1]][0] + four_direction[i][0]
                        ty = self.gate[pair_gate[1]][1] + four_direction[i][1]

                        if tx < 0 or tx >= self.size[1] or ty < 0 or ty >= self.size[2]:
                            continue

                        gate_num = self.used_wired[0][tx][ty]

                        flag_conflict = self.del_and_add(gate_num, cnt)

                if flag_conflict == 1:
                    # the point in level 1
                    gate_num = self.used_wired[1][self.gate[pair_gate[1]][0]][self.gate[pair_gate[1]][1]]
                    flag_conflict = self.del_and_add(gate_num, cnt)

            if flag_conflict == 0:
                cnt = cnt + 1

        return cnt


if __name__ == "__main__":
    size1 = readjson("gridsizes.json", 1)
    gate1 = readjson("gatelists.json", 1)
    netlist1 = readjson("netlists.json", 1)
    chip = chip(size1, gate1, netlist1)

    # ans = 0
    # while ans != 30:
    #     ans = chip.find_solution()
    #     print(ans)
    # print(chip.output_line())

    chip.plot()
