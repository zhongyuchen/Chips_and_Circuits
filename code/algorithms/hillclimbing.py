from readjson import readjson, loadchip
import sys
sys.path.append('../')
import random
import copy
from lineplot import lineplot
from classes.chip import Chip


class Hillclimber():

    def __init__(self, size, gatelist, netlist, steps=500):
        self.chip = Chip(size, gatelist, netlist)
        self.steps = steps

    def hillclimbing(self, steps=1000, amount=1, retry=1, get_wires_function=random_wires, filename="hc-"):
        print("Starting to climb a hill...")
        print(f"Start with a cost of {self.chip.cost()}...")
        costs = [self.chip.cost()]
        fail_num = copy.deepcopy(steps)
        chip_best = copy.deepcopy(self.chip)

        for i in range(steps):
            # get wire num function
            wire_num = get_wires_function(self.chip, amount)

            # climb
            print(f"Step {i}, trying to re-add wire {wire_num}, ", end="")
            chip_temp = copy.deepcopy(self.chip)

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

                # success
                if fail != -1 and chip_temp_temp.cost() < self.chip.cost():
                    self.chip = chip_temp_temp
                    fail_num -= 1
                    print(f"success", end=" ")
                    break

            if self.chip.cost() < chip_best.cost():
                chip_best = self.chip

            print(f"cost {self.chip.cost()}")
            costs.append(self.chip.cost())

        # save the best!
        filename += "%04d.json" % chip_best.cost()
        chip_best.save(filename)

        print(f"All done! {steps} steps and {fail_num} fails")
        return costs




def hc_longest_wire(chip, steps, fun=longest_wire):
    # the cost drops once for ~ 2, or doesn't drop at all

    print("Starting to climb a hill...")
    print(f"Start with a cost of {chip.cost()}...")
    costs = [chip.cost()]

    for i in range(steps):
        # get wire num function
        wire_num = fun(chip)

        # climb
        print(f"Step {i}, trying to re-add wire {wire_num}, ", end="")

        # re-add the selected wires
        chip.delline(wire_num)
        chip.addline(wire_num)

        print(f"cost {chip.cost()}")
        costs.append(chip.cost())

    return costs





def hc_random_wires(chip, steps=1000, amount=1, retry=1, get_wires_function=random_wires, filename="hc-"):
    print("Starting to climb a hill...")
    print(f"Start with a cost of {chip.cost()}...")
    costs = [chip.cost()]
    fail_num = copy.deepcopy(steps)
    chip_best = copy.deepcopy(chip)

    for i in range(steps):
        # get wire num function
        wire_num = get_wires_function(chip, amount)

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

            # success
            if fail != -1 and chip_temp_temp.cost() < chip.cost():
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

    steps = 100

    chip0 = loadchip("hillclimbing/hc-2-000-0523.json")
    chip1 = copy.deepcopy(chip0)
    chip2 = copy.deepcopy(chip0)
    chip3 = copy.deepcopy(chip0)

    cn = []
    cn.append([hc_longest_wire(chip0, steps=steps), "hc_longest_wire"])
    # cn.append([hc_random_wire(chip1, steps), "hc_random_wire"])
    cn.append([hc_random_wires(chip2, steps=steps, amount=6, retry=30), "hc_random_wires"])
    # cn.append([hc_random_wires(chip3, steps=steps, amount=6, retry=30, function="reduce", filename="hillclimbing/hc-2-002-"), "hc_random_wires_reduce"])
    lineplot(cn, "hill climbing comparison test")
