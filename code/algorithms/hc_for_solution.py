from readjson import readjson, loadchip
import copy
import sys
sys.path.append('../')
from classes.chip import chip
import random
from hillclimbing import lineplot


four_direction = [[1, 0], [-1, 0], [0, 1], [0, -1]]


def astar(chip):
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


def wrapper(chip):
    # wrapper of the function that finds a solution
    # different function lead to different solution, even with the same sequence
    return astar(chip)


def shuffle_random_wires(chip, amount=2):
    # randomly select a piece of the sequence, with the length of amount
    # shuffle this piece

    start = random.randint(0, len(chip.net) - amount)
    print(f"[{start}, {start + amount}]: {chip.net[start: start + amount]} -> ", end="")
    l = chip.net[start: start + amount]
    random.shuffle(l)
    chip.net[start: start + amount] = l
    print(f"{chip.net[start: start + amount]}", end=" ")


def hc_solution(chip, steps=1000, amount=2, retry=1, filename="hc-"):
    # hill climbing for finding a solution
    print("Starting climbing for a solution...")
    success_num = 0
    connected = wrapper(chip)
    connected_list = [copy.deepcopy(connected)]
    print(f"Starting with a {connected}/{len(chip.net)}-connected chip...")

    # climb
    for i in range(steps):
        # retry
        print(f"Step {i},", end=" ")
        for j in range(retry):
            # new chip
            chip_test = copy.deepcopy(chip)
            chip_test.clean()
            # shuffle
            shuffle_random_wires(chip_test, amount=amount)
            connected_test = wrapper(chip_test)

            if connected_test > connected:
                connected = copy.deepcopy(connected_test)
                chip = copy.deepcopy(chip_test)
                success_num += 1
                break

        print(f"{connected}/{len(chip.net)}")
        connected_list.append(copy.deepcopy(connected))

        if connected == len(chip.net):
            break

    # save the best!
    filename += f"{connected}.json"
    chip.save(filename)

    print(f"All done! {len(connected_list) - 1} steps, {connected}/{len(chip.net)} connected, {success_num}/{len(connected_list) - 1} success.")
    return connected_list


if __name__ == "__main__":
    size1 = readjson("gridsizes.json", 1)
    gate1 = readjson("gatelists.json", 1)
    netlist3 = readjson("netlists.json", 3)

    chip_temp = loadchip("hc_for_solution/hc-3-000-26.json")
    chip_temp.clean()

    lines = []

    lines.append([hc_solution(chip_temp, steps=1000, amount=3, retry=1, filename="hc_for_solution/hc-3-002-"), "shuffle_random_wires"])
    lineplot(lines, "hill climbing for a solution")

    # print(astar(chip_temp))
