# -*- coding:utf8 -*-
# @author: Tiancheng Guo
# @contact: skyerguo97@gmail.com
# @file: first-version.py
# @time: 12/11/18
# @description: This is the second version of bfs algorithm for netlist_1
#               Try to settle down the problem for first-version. Just search the nodes as the priority "more degree required nodes search first"
#               Sadly. It don't work out a solution yet.

import random

netlist_length = 30
nodes_number = 25

# define in tuple form(unable to be modified)
netlist_1_unordered = [(23, 4), (5, 7), (1, 0), (15, 21), (3, 5), (7, 13), (3, 23), (23, 8), (22, 13), (15, 17), (20, 10), (15, 8), (13, 18), (19, 2), (22, 11), (10, 4), (11, 24), (3, 15), (2, 20), (3, 4), (20, 19), (16, 9), (19, 5), (3, 0), (15, 5), (6, 14), (7, 9), (9, 13), (22, 16), (10, 7)]

coordinate = [(1, 11), (6, 11), (10, 11), (15, 11), (3, 10),
              (12, 10), (14, 10), (12, 9), (8, 8), (1, 7),
              (4, 7), (11, 7), (16, 7), (13, 5), (16, 5),
              (2, 4), (6, 4), (9, 4), (11, 4), (15, 4),
              (1, 3), (2, 2), (9, 2), (1, 1), (12, 1)]

# define as list form(able to be modified)
netlist_1_ordered = [[[] for j in range(2)] for i in range(netlist_length)]


used_wired = [[[0 for i in range(13)] for j in range(18)] for k in range(7)]
visit = [[[0 for i in range(13)] for j in range(18)] for k in range(7)]
cost_list = []
nodes_degree = [0 for i in range(nodes_number)]

fx = [-1, 0, 0, 1]
fy = [0, 1, -1, 0]


def swap(t1, t2):
    return t2, t1


def bfs(st, en):
    st = st
    en = en
    queue = []
    # tuple with 4 elements(level, x, y, cost, last) presents level, x-axis, y-axis and last point
    left = 0
    right = 1
    queue.append([0, coordinate[st][0], coordinate[st][1], -1])

    print(st, en)

    for i in range(7):
        for j in range(18):
            for k in range(13):
                visit[i][j][k] = 0

    for i in range(nodes_number):
        visit[0][coordinate[i][0]][coordinate[i][1]] = 1
        used_wired[0][coordinate[i][0]][coordinate[i][1]] = 0
    visit[0][coordinate[en][0]][coordinate[en][1]] = 0

    # f = open("test.txt", "a")
    # for i0 in range(2):
    #     for i2 in range(12, 0, -1):
    #         for i1 in range(18):
    #             print(used_wired[i0][i1][i2], end="", file=f)
    #         print("", file=f)
    #     print("\n", file=f)
    # print('-------', file=f)
    while left < right:
        u = queue[left]
        # f = open("test.txt", "a")
        if u[0] == 0 and u[1] == coordinate[en][0] and u[2] == coordinate[en][1]:
            current_cost = 0
            used_wired[u[0]][u[1]][u[2]] = 1
            tmp = u[3]
            while tmp != -1:
                used_wired[queue[tmp][0]][queue[tmp][1]][queue[tmp][2]] = 1
                current_cost = current_cost + 1
                tmp = queue[tmp][3]
            #print(current_cost, file=f)
            #
            # for i0 in range(2):
            #     for i2 in range(12, 0, -1):
            #         for i1 in range(18):
            #             print(used_wired[i0][i1][i2], end="", file=f)
            #         print("", file=f)
            #     print("\n", file=f)
            # print('-------', file=f)

            return current_cost

        # 4 directions in same level
        for i in range(4):
            tx = u[1] + fx[i]
            ty = u[2] + fy[i]
            if tx < 0 or tx > 17 or ty < 0 or ty > 12:
                continue

            if visit[u[0]][tx][ty] == 0 and used_wired[u[0]][tx][ty] == 0:
                queue.append([u[0], tx, ty, left])
                visit[u[0]][tx][ty] = 1
                right = right + 1

        # down level
        if u[0] > 0:
            if visit[u[0] - 1][u[1]][u[2]] == 0 and used_wired[u[0] - 1][u[1]][u[2]] == 0:
                queue.append([u[0] - 1, u[1], u[2], left])
                visit[u[0] - 1][u[1]][u[2]] = 1
                right = right + 1

        # up level
        if u[0] < 6:
            if visit[u[0] + 1][u[1]][u[2]] == 0 and used_wired[u[0] + 1][u[1]][u[2]] == 0:
                queue.append([u[0] + 1, u[1], u[2], left])
                visit[u[0] + 1][u[1]][u[2]] = 1
                right = right + 1

        left = left + 1


def work():
    for i in range(7):
        for j in range(18):
            for k in range(13):
                used_wired[i][j][k] = 0

    for i in range(netlist_length):
        for j in range(i + 1, netlist_length):
            if nodes_degree[netlist_1_ordered[j][1]] >= nodes_degree[netlist_1_ordered[i][1]] or \
                    (nodes_degree[netlist_1_ordered[j][1]] == nodes_degree[netlist_1_ordered[i][1]] and
                     nodes_degree[netlist_1_ordered[j][0]] >= nodes_degree[netlist_1_ordered[i][0]]):
                netlist_1_ordered[i], netlist_1_ordered[j] = swap(netlist_1_ordered[i], netlist_1_ordered[j])
            # if nodes_degree[netlist_1_ordered[j][1]] > nodes_degree[netlist_1_ordered[i][1]]:
            #     netlist_1_ordered[i], netlist_1_ordered[j] = swap(netlist_1_ordered[i], netlist_1_ordered[j])

    total_cost = 0
    # f = open("test.txt", "a")
    for i in range(netlist_length):
        total_cost = total_cost + bfs(netlist_1_ordered[i][0], netlist_1_ordered[i][1])

    cost_list.append(total_cost)
    print(total_cost)


def calc_degree():
    for i in range(netlist_length):
        nodes_degree[netlist_1_unordered[i][0]] = nodes_degree[netlist_1_unordered[i][0]] + 1
        nodes_degree[netlist_1_unordered[i][1]] = nodes_degree[netlist_1_unordered[i][1]] + 1

    for i in range(netlist_length):
        if nodes_degree[netlist_1_unordered[i][0]] > nodes_degree[netlist_1_unordered[i][1]]:
            netlist_1_ordered[i][0] = netlist_1_unordered[i][1]
            netlist_1_ordered[i][1] = netlist_1_unordered[i][0]
        else:
            netlist_1_ordered[i][0] = netlist_1_unordered[i][0]
            netlist_1_ordered[i][1] = netlist_1_unordered[i][1]


if __name__ == '__main__':
    calc_degree()
    for i in range(100):
        random.shuffle(netlist_1_unordered)
        work()
        print(min(cost_list))


