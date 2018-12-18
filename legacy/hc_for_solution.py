from readjson import readjson, loadchip
import copy
import sys
sys.path.append('../')
from classes.chip import chip
import random
from hillclimbing import lineplot


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
