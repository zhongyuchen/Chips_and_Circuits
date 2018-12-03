# -*- coding:utf8 -*-
# @author: Tiancheng Guo
# @contact: skyerguo97@gmail.com
# @file: genetic_algorithm.py
# @time: 12/4/18
# @description:

import random
from readjson import readjson
import sys
sys.path.append('../')
from classes.chip import chip
import astar_spfa


def load_pool(pool_size, parent_size, chipsize, chipgate, chipnetlist):
    total_wires = len(chipnetlist)
    print(total_wires)

    ans = 0
    for i in range(pool_size):
        current_chip = chip(chipsize, chipgate, chipnetlist)
        ans = astar_spfa.astar_spfa(current_chip)


if __name__ == '__main__':
    chipsize = readjson("gridsizes.json", 1)
    chipgate = readjson("gatelists.json", 1)
    chipnetlist = readjson("netlists.json", 3)

    load_pool(5000, 50, chipsize, chipgate, chipnetlist)