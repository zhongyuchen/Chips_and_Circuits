import random
from readjson import readjson
import sys
sys.path.append('../')
from classes.chip import chip

four_direction = [[1, 0], [-1, 0], [0, 1], [0, -1]]


def check_node_spfa(chip, u, v, queue, left, right, dis, visit, en):
    if chip.used_wired[v[0]][v[1]][v[2]] == -1 and (
                (v[0] == 0 and v[1] == chip.gate[en][0] and v[2] == chip.gate[en][1]) or  # the ending gate
                (chip.grid[v[0]][v[1]][v[2]] != -1)  # not a gate
            ):
        if dis[u[0]][u[1]][u[2]] + chip.grid_value[v[0]][v[1]][v[2]] < dis[v[0]][v[1]][v[2]]:
            dis[v[0]][v[1]][v[2]] = dis[u[0]][u[1]][u[2]] + chip.grid_value[v[0]][v[1]][v[2]]

            if visit[v[0]][v[1]][v[2]] == 0:
                visit[v[0]][v[1]][v[2]] = 1
                queue.append([v[0], v[1], v[2], left])

                right = right + 1


def addline_spfa(chip, net_num):
    # add a line. using spfa(an improvement of Bellman-Ford)

    st = chip.net[net_num][0]
    en = chip.net[net_num][1]

    max_dis = 10000

    queue = []
    # tuple with 4 elements(level, x, y, cost, last) presents level, x-axis, y-axis and last point

    visit = [[[0 for i in range(chip.size[2])] for j in range(chip.size[1])] for k in range(chip.size[0])]
    dis = [[[max_dis for i in range(chip.size[2])] for j in range(chip.size[1])] for k in range(chip.size[0])]

    left = 0
    right = 1
    queue.append([0, chip.gate[st][0], chip.gate[st][1], -1])
    dis[0][chip.gate[st][0]][chip.gate[st][1]] = 0
    visit[0][chip.gate[st][0]][chip.gate[st][1]] = 1

    for i in range(len(chip.gate)):
        chip.used_wired[0][chip.gate[i][0]][chip.gate[i][1]] = -1

    while left < right:
        u = queue[left]
        v = [0 for i in range(3)]

        visit[u[0]][u[1]][u[2]] = 0

        # find a path
        if u[0] == 0 and u[1] == chip.gate[en][0] and u[2] == chip.gate[en][1]:
            current_cost = 0
            tmp = u[3]
            chip.map_line[net_num].append([u[0], u[1], u[2]])
            while tmp != -1:
                if chip.grid[queue[tmp][0]][queue[tmp][1]][queue[tmp][2]] != -1:
                    chip.used_wired[queue[tmp][0]][queue[tmp][1]][queue[tmp][2]] = net_num
                    chip.map_line[net_num].append([queue[tmp][0], queue[tmp][1], queue[tmp][2]])
                current_cost = current_cost + 1
                tmp = queue[tmp][3]
            chip.map_line[net_num].append([0, chip.gate[st][0], chip.gate[st][1]])

            return current_cost

        # up level
        if u[0] < 6:
            v[0] = u[0] + 1
            v[1] = u[1]
            v[2] = u[2]
            check_node_spfa(chip, u, v, queue, left, right, dis, visit, en)

        # 4 directions in same level
        for i in range(4):
            tx = u[1] + four_direction[i][0]
            ty = u[2] + four_direction[i][1]
            if tx < 0 or tx >= chip.size[1] or ty < 0 or ty >= chip.size[2]:
                continue

            v[0] = u[0]
            v[1] = tx
            v[2] = ty
            check_node_spfa(chip, u, v, queue, left, right, dis, visit, en)

        # down level
        if u[0] > 0:
            v[0] = u[0] - 1
            v[1] = u[1]
            v[2] = u[2]
            check_node_spfa(chip, u, v, queue, left, right, dis, visit, en)

        left = left + 1
    return -1


def del_and_add_spfa(chip, delline_num, addline_num):
    # find a solution, return 0
    # else return 1

    if delline_num == -1:
        # do not need to delete anything
        return 1

    chip.delline(delline_num)
    cost1 = addline_spfa(chip, addline_num)
    cost2 = addline_spfa(chip, delline_num)
    if cost1 == -1 or cost2 == -1:
        # cannot find a replaced solution

        # back to last status
        if cost1 != -1:
            chip.delline(addline_num)
        if cost2 != -1:
            chip.delline(delline_num)
        addline_spfa(chip, delline_num)
        return 1
    else:
        return 0


def astar_spfa(chip):
    random.shuffle(chip.net)

    cnt = 0
    for pair_gate in chip.net:
        cost = addline_spfa(chip, cnt)
        flag_conflict = 0
        # if there is a solution, flag_conflict = 0
        # else flag_conflict = 1

        if cost == -1:

            flag_conflict = 1

            # for pair_gate[0]
            # four points in level 0

            if flag_conflict == 1:
                for i in range(4):
                    if flag_conflict == 0:
                        break
                    tx = chip.gate[pair_gate[0]][0] + four_direction[i][0]
                    ty = chip.gate[pair_gate[0]][1] + four_direction[i][1]

                    if tx < 0 or tx >= chip.size[1] or ty < 0 or ty >= chip.size[2]:
                        continue

                    net_num = chip.used_wired[0][tx][ty]

                    flag_conflict = del_and_add_spfa(chip, net_num, cnt)

            if flag_conflict == 1:
                # the point in level 1
                net_num = chip.used_wired[1][chip.gate[pair_gate[0]][0]][chip.gate[pair_gate[0]][1]]
                flag_conflict = del_and_add_spfa(chip, net_num, cnt)

            # for pair_gate[1]
            if flag_conflict == 1:
                for i in range(4):
                    if flag_conflict == 0:
                        break
                    tx = chip.gate[pair_gate[1]][0] + four_direction[i][0]
                    ty = chip.gate[pair_gate[1]][1] + four_direction[i][1]

                    if tx < 0 or tx >= chip.size[1] or ty < 0 or ty >= chip.size[2]:
                        continue

                    net_num = chip.used_wired[0][tx][ty]

                    flag_conflict = del_and_add_spfa(chip, net_num, cnt)

            if flag_conflict == 1:
                # the point in level 1
                net_num = chip.used_wired[1][chip.gate[pair_gate[1]][0]][chip.gate[pair_gate[1]][1]]
                flag_conflict = del_and_add_spfa(chip, net_num, cnt)

        if flag_conflict == 0:
            cnt = cnt + 1
        else:
            return cnt

    return cnt


if __name__ == "__main__":
    size1 = readjson("gridsizes.json", 1)
    gate1 = readjson("gatelists.json", 1)
    netlist1 = readjson("netlists.json", 1)

    ans = 0
    total_wires = len(netlist1)
    print(total_wires)
    while ans != total_wires:
        chip_test = chip(size1, gate1, netlist1)
        ans = astar_spfa(chip_test)
        print("wires: %f" % ans, end=" ")
        print("cost: %f" % chip_test.cost())

    chip_test.plot()
