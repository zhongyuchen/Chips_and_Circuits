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

POOL_SIZE = 5000
PARENT_SIZE = 50


def create_pool(pool_size, chipsize, chipgate, chipnetlist):
    total_wires = len(chipnetlist)
    index = [[] for i in range(pool_size)]

    ans = 0
    for i in range(pool_size):
        current_chip = chip(chipsize, chipgate, chipnetlist)
        ans = astar_spfa.astar_spfa(current_chip)
        current_chip.save("GApool/astar-%04d-%02d.json" % (i, ans))
        print(i)


# def load_pool(pool_size, parent_size):


if __name__ == '__main__':
    chipsize = readjson("gridsizes.json", 1)
    chipgate = readjson("gatelists.json", 1)
    chipnetlist = readjson("netlists.json", 3)

    create_pool(POOL_SIZE, chipsize, chipgate, chipnetlist)
    # load_pool(POOL_SIZE, PARENT_SIZE)