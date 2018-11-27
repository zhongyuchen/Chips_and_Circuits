import random
from readjson import readjson
import sys
sys.path.append('../')
from classes.chip import chip


four_direction = [[1, 0], [-1, 0], [0, 1], [0, -1]]


def astar(chip):
    random.shuffle(chip.net)

    cnt = 0
    for pair_gate in chip.net:
        cost = chip.addline(cnt)
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

                    flag_conflict = chip.del_and_add(net_num, cnt)

            if flag_conflict == 1:
                # the point in level 1
                net_num = chip.used_wired[1][chip.gate[pair_gate[0]][0]][chip.gate[pair_gate[0]][1]]
                flag_conflict = chip.del_and_add(net_num, cnt)

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

                    flag_conflict = chip.del_and_add(net_num, cnt)

            if flag_conflict == 1:
                # the point in level 1
                net_num = chip.used_wired[1][chip.gate[pair_gate[1]][0]][chip.gate[pair_gate[1]][1]]
                flag_conflict = chip.del_and_add(net_num, cnt)

        if flag_conflict == 0:
            cnt = cnt + 1

    return cnt


if __name__ == "__main__":
    size1 = readjson("gridsizes.json", 1)
    gate1 = readjson("gatelists.json", 1)
    netlist1 = readjson("netlists.json", 1)

    ans = 0
    while ans != 30:
        chip_test = chip(size1, gate1, netlist1)
        ans = astar(chip_test)
        print(ans)

    # wirelist = chip.output_line()
    # i = 1
    # for wire in wirelist:
    #     print(i)
    #     print(wire)
    #     i += 1
    chip_test.plot()