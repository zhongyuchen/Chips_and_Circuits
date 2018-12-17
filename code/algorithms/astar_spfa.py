import random
from readjson import readjson
import sys
sys.path.append('../')
from classes.chip import Chip


four_direction = [[1, 0], [-1, 0], [0, 1], [0, -1]]


class AstarSpfa:
    """
        This is the method to find path in the chip.
    """

    def __init__(self):
        chip = Chip()

    def check_node_spfa(self, u, v, queue, left, dis, visit, en):
        if self.chip.used_wired[v[0]][v[1]][v[2]] == -1 and (
                    (v[0] == 0 and v[1] == self.chip.gate[en][0] and v[2] == self.chip.gate[en][1]) or  # the ending gate
                    (self.chip.grid[v[0]][v[1]][v[2]] != -1)  # not a gate
                ):
            if dis[u[0]][u[1]][u[2]] + self.chip.grid_value[v[0]][v[1]][v[2]] < dis[v[0]][v[1]][v[2]]:
                dis[v[0]][v[1]][v[2]] = dis[u[0]][u[1]][u[2]] + self.chip.grid_value[v[0]][v[1]][v[2]]

                if visit[v[0]][v[1]][v[2]] == 0:
                    visit[v[0]][v[1]][v[2]] = 1
                    queue.append([v[0], v[1], v[2], left])

                    return 1
        return 0

    def find_path(self, u, queue, net_num, st):
        current_cost = 0
        tmp = u[3]
        self.chip.map_line[net_num].append([u[0], u[1], u[2]])
        while tmp != -1:
            if self.chip.grid[queue[tmp][0]][queue[tmp][1]][queue[tmp][2]] != -1:
                self.chip.used_wired[queue[tmp][0]][queue[tmp][1]][queue[tmp][2]] = net_num
                self.chip.map_line[net_num].append([queue[tmp][0], queue[tmp][1], queue[tmp][2]])
            current_cost = current_cost + 1
            tmp = queue[tmp][3]
        self.chip.map_line[net_num].append([0, self.chip.gate[st][0], self.chip.gate[st][1]])
        return current_cost

    def addline_spfa(self, net_num):
        """
            Add a line.
            Use the algorithm spfa(an improvement of Bellman-Ford).
        """

        st = self.chip.net[net_num][0]
        en = self.chip.net[net_num][1]

        max_dis = 1000000

        queue = []
        # tuple with 4 elements(level, x, y, cost, last) presents level, x-axis, y-axis and last point

        visit = [[[0 for _ in range(self.chip.size[2])] for _ in range(self.chip.size[1])] for _ in range(self.chip.size[0])]
        dis = [[[max_dis for _ in range(self.chip.size[2])] for _ in range(self.chip.size[1])] for _ in range(self.chip.size[0])]

        left = 0
        right = 1
        queue.append([0, self.chip.gate[st][0], self.chip.gate[st][1], -1])
        dis[0][self.chip.gate[st][0]][self.chip.gate[st][1]] = 0
        visit[0][self.chip.gate[st][0]][self.chip.gate[st][1]] = 1

        for i in range(len(self.chip.gate)):
            self.chip.used_wired[0][self.chip.gate[i][0]][self.chip.gate[i][1]] = -1

        while left < right:
            u = queue[left]
            v = [0 for i in range(3)]

            visit[u[0]][u[1]][u[2]] = 0

            # find a path
            if u[0] == 0 and u[1] == self.chip.gate[en][0] and u[2] == self.chip.gate[en][1]:
                return self.find_path(u, queue, net_num, st)

            # up level
            if u[0] < 6:
                v[0], v[1], v[2] = u[0] + 1, u[1], u[2]
                right = right + self.check_node_spfa(u, v, queue, left, dis, visit, en)

            # 4 directions in same level
            for i in range(4):
                tx = u[1] + four_direction[i][0]
                ty = u[2] + four_direction[i][1]
                if tx < 0 or tx >= self.chip.size[1] or ty < 0 or ty >= self.chip.size[2]:
                    continue

                v[0], v[1], v[2] = u[0], tx, ty
                right = right + self.check_node_spfa(u, v, queue, left, dis, visit, en)

            # down level
            if u[0] > 0:
                v[0], v[1], v[2] = u[0] - 1, u[1], u[2]
                right = right + self.check_node_spfa(u, v, queue, left, dis, visit, en)

            left = left + 1
        return -1

    def del_and_add_spfa(self, delline_num, addline_num):
        # find a solution, return 0
        # else return 1

        if delline_num == -1:
            # do not need to delete anything
            return 1

        self.chip.delline(delline_num)
        cost1 = self.addline_spfa(addline_num)
        cost2 = self.addline_spfa(delline_num)
        if cost1 == -1 or cost2 == -1:
            # cannot find a replaced solution

            # back to last status
            if cost1 != -1:
                self.chip.delline(addline_num)
            if cost2 != -1:
                self.chip.delline(delline_num)
            self.addline_spfa(delline_num)
            return 1
        else:
            return 0

    def astar_spfa(self):
        cnt = 0
        for pair_gate in self.chip.net:
            cost = self.addline_spfa(cnt)
            flag_conflict = 0
            # If there is a conflict occurs, the 'flag_conflict' will be 1.

            if cost == -1:

                flag_conflict = 1

                # for pair_gate[0]
                # four points in level 0

                if flag_conflict == 1:
                    for i in range(4):
                        if flag_conflict == 0:
                            break
                        tx = self.chip.gate[pair_gate[0]][0] + four_direction[i][0]
                        ty = self.chip.gate[pair_gate[0]][1] + four_direction[i][1]

                        if tx < 0 or tx >= self.chip.size[1] or ty < 0 or ty >= self.chip.size[2]:
                            continue

                        net_num = self.chip.used_wired[0][tx][ty]

                        flag_conflict = self.del_and_add_spfa(net_num, cnt)

                if flag_conflict == 1:
                    # the point in level 1
                    net_num = self.chip.used_wired[1][self.chip.gate[pair_gate[0]][0]][self.chip.gate[pair_gate[0]][1]]
                    flag_conflict = self.del_and_add_spfa(net_num, cnt)

                # for pair_gate[1]
                if flag_conflict == 1:
                    for i in range(4):
                        if flag_conflict == 0:
                            break
                        tx = self.chip.gate[pair_gate[1]][0] + four_direction[i][0]
                        ty = self.chip.gate[pair_gate[1]][1] + four_direction[i][1]

                        if tx < 0 or tx >= self.chip.size[1] or ty < 0 or ty >= self.chip.size[2]:
                            continue

                        net_num = self.chip.used_wired[0][tx][ty]

                        flag_conflict = self.del_and_add_spfa(net_num, cnt)

                if flag_conflict == 1:
                    # the point in level 1
                    net_num = self.chip.used_wired[1][self.chip.gate[pair_gate[1]][0]][self.chip.gate[pair_gate[1]][1]]
                    flag_conflict = self.del_and_add_spfa(net_num, cnt)

            if flag_conflict == 0:
                cnt = cnt + 1
            else:
                return cnt

        return cnt

    def run(self, chip_input, use_spfa=1):
        self.chip = chip_input
        return self.astar_spfa()


if __name__ == "__main__":
    # size1 = readjson("gridsizes.json", 2)
    # gate1 = readjson("gatelists.json", 2)
    # netlist1 = readjson("netlists.json", 4)

    # ans = 0
    # total_wires = len(netlist1)
    # print(total_wires)
    # while ans != total_wires:
    #     chip_test = chip(size1, gate1, netlist1)
    #     random.shuffle(chip_test.net)
    #     ans = astar_spfa(chip_test)
    #
    #     print("wires: %f" % ans, end=" ")
    #     print("cost: %f" % chip_test.cost())
    #
    # chip_test.plot("2-4 for pre test")

    size1 = readjson("gridsizes.json", 1)
    gate1 = readjson("gatelists.json", 1)
    netlist1 = readjson("netlists.json", 1)
    chip_test = Chip(size1, gate1, netlist1)
    random.shuffle(chip_test.net)
    temp = AstarSpfa()
    ans = temp.run(chip_test)
    print(ans)
