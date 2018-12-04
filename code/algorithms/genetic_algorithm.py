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
import os

POOL_SIZE = 5000
PARENT_SIZE = 50
GA_PATH = "../../results/GApool"


def create_pool(pool_size, chipsize, chipgate, chipnetlist):
    total_wires = len(chipnetlist)
    index = [[] for i in range(pool_size)]

    ans = 0
    for i in range(pool_size):
        current_chip = chip(chipsize, chipgate, chipnetlist)
        ans = astar_spfa.astar_spfa(current_chip)
        current_chip.save("GApool/astar-%04d-%02d.json" % (i, ans))

        with open("pool_record.txt", "a") as f:
            print(i, ans, file=f)


def load_pool(pool_size, parent_size):

    # scan filename.
    index = []
    files = os.listdir(GA_PATH)
    for GAfilename in files:
        i = int(GAfilename[6:10])
        ans = int(GAfilename[11:13])
        index.append([i, ans])
    index.sort(key=lambda index_pair: index_pair[1], reverse=True)  # sort the index by ans

    index_parent = []
    for i in range(parent_size):
        index_parent.append(index[i])

    return index_parent


if __name__ == '__main__':
    chipsize = readjson("gridsizes.json", 1)
    chipgate = readjson("gatelists.json", 1)
    chipnetlist = readjson("netlists.json", 3)

    # create_pool(POOL_SIZE, chipsize, chipgate, chipnetlist)
    index_parent = load_pool(POOL_SIZE, PARENT_SIZE)
    print(index_parent)