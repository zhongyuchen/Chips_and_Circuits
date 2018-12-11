from readjson import readjson, loadchip
import sys
sys.path.append('../')
import random
import copy
from lineplot import lineplot


def longest_wire(chip):
    # get the number of the (first) longest wire
    wire_num = 0
    max_length = 0
    for i, wire in enumerate(chip.map_line):
        if len(wire) > max_length:
            wire_num = i
            max_length = len(wire)
    return wire_num


def hc_longest_wire(chip, step):
    # the cost drops once for ~ 2, or doesn't drop at all

    print("Starting to climb a hill...")
    print(f"Start with a cost of {chip.cost()}...")
    costs = [chip.cost()]

    for i in range(steps):
        # get wire num function
        wire_num = longest_wire(chip)

        # climb
        print(f"Step {i}, trying to re-add wire {wire_num}, ", end="")

        # re-add the selected wires
        chip.delline(wire_num)
        chip.addline(wire_num)

        print(f"cost {chip.cost()}")
        costs.append(chip.cost())

    return costs


def random_wire(chip):
    # get stable around 50 steps
    # improvement ~ 10
    return random.randint(0, len(chip.net) - 1)


def hc_random_wire(chip, steps):
    # keep dropping for 80 steps, cost reduces ~ 10
    print("Starting to climb a hill...")
    print(f"Start with a cost of {chip.cost()}...")
    costs = [chip.cost()]

    for i in range(steps):
        # get wire num function
        wire_num = random_wire(chip)

        # climb
        print(f"Step {i}, trying to re-add wire {wire_num}, ", end="")

        # re-add the selected wires
        chip.delline(wire_num)
        chip.addline(wire_num)

        print(f"cost {chip.cost()}")
        costs.append(chip.cost())

    return costs


def random_wires(chip, amount):
    # randomly select a certain amount of wires
    length = len(chip.net)
    wires = []
    for i in range(amount):
        wires.append(random.randint(0, length - 1))
    return wires


def hc_random_wires(chip, steps=1000, amount=1, retry=1, function="", filename="hc-"):
    # flag == "":
    #     sometimes gets good optimization
    #     but highly unstable, comparing to hc_random_wires_reduce
    #     good for getting states that aren't reachable for hc_random_wires_reduce
    #     fail ratio ~10% (1000 steps, 3 amount, 1 times)
    #     fail ratio ~8% (1000 steps, 3 amount, 5 times) 523 -> 501, net2
    #     fail ratio ~30% (1000 steps, 6 amount, 30 times) 523 -> 465, net2

    # flag == "reduce":
    #     promising
    #     after 1500 steps, cost still drops
    #     fail ratio ~98% (1000 steps, 3 amount, 1 times)
    #     fail ratio ~97.5% (1000 steps, 3 amount, 5 times) 523 -> 461, net2
    #     fail ratio ~97.5% (1000 steps, 6 amount, 30 times) 523 -> 449, net2

    print("Starting to climb a hill...")
    print(f"Start with a cost of {chip.cost()}...")
    costs = [chip.cost()]
    fail_num = copy.deepcopy(steps)
    chip_best = copy.deepcopy(chip)

    for i in range(steps):
        # get wire num function
        wire_num = random_wires(chip, amount)

        # climb
        print(f"Step {i}, trying to re-add wire {wire_num}, ", end="")
        chip_temp = copy.deepcopy(chip)

        # delete the selected wires
        for w in wire_num:
            chip_temp.delline(w)

        # re-add
        for j in range(retry):
            # try another random order
            random.shuffle(wire_num)
            chip_temp_temp = copy.deepcopy(chip_temp)

            fail = 0
            for w in wire_num:
                fail = chip_temp_temp.addline(w)
                if fail == -1:
                    # fail
                    break

            # success check list
            check_list = [fail != -1]
            if function == "reduce":
                check_list.append(chip_temp_temp.cost() < chip.cost())

            # success
            if sum(check_list) == len(check_list):
                chip = chip_temp_temp
                fail_num -= 1
                print(f"success", end=" ")
                break

        if chip.cost() < chip_best.cost():
            chip_best = chip

        print(f"cost {chip.cost()}")
        costs.append(chip.cost())

    # save the best!
    filename += "%04d.json" % chip_best.cost()
    chip_best.save(filename)

    print(f"All done! {steps} steps and {fail_num} fails")
    return costs


if __name__ == "__main__":
    size1 = readjson("gridsizes.json", 1)
    gate1 = readjson("gatelists.json", 1)
    netlist2 = readjson("netlists.json", 2)

    steps = 1000

    chip0 = loadchip("hillclimbing/hc-2-000-0523.json")
    chip1 = copy.deepcopy(chip0)
    chip2 = copy.deepcopy(chip0)
    chip3 = copy.deepcopy(chip0)

    cn = []
    cn.append([hc_longest_wire(chip0, steps), "hc_longest_wire"])
    cn.append([hc_random_wire(chip1, steps), "hc_random_wire"])
    cn.append([hc_random_wires(chip2, steps=steps, amount=6, retry=30), "hc_random_wires"])
    cn.append([hc_random_wires(chip3, steps=steps, amount=6, retry=30, function="reduce", filename="hillclimbing/hc-2-002-"), "hc_random_wires_reduce"])
    lineplot(cn, "hill climbing for better solution")
