# -*- coding:utf8 -*-
# @author: Tiancheng Guo
# @contact: skyerguo97@gmail.com
# @file: genetic_algorithm.py
# @time: 12/4/18
# @description:

import random
from readjson import readjson, loadchip
import sys
sys.path.append('../')
from classes.chip import chip
import astar_spfa
import os
import shutil

POOL_SIZE = 5000
PARENT_SIZE = 50 # this must be even number
GENERATION_SIZE = 10
GA_PATH = "../../results/GApool"


def create_pool(chipsize, chipgate, chipnetlist):
    total_wires = len(chipnetlist)
    index = [[] for i in range(POOL_SIZE)]

    ans = 0
    for i in range(POOL_SIZE):
        current_chip = chip(chipsize, chipgate, chipnetlist)
        ans = astar_spfa.astar_spfa(current_chip)
        current_chip.save("GApool/generation0/astar-%04d-%02d.json" % (i, ans))

        with open("pool_record.txt", "a") as f:
            print(i, ans, file=f)


def load_pool(gene):

    # scan filename.
    index = []
    files = os.listdir(GA_PATH + '/generation' + str(gene))
    for GAfilename in files:
        i = int(GAfilename[6:10])
        ans = int(GAfilename[11:13])
        index.append([i, ans])
    index.sort(key=lambda index_pair: index_pair[1], reverse=True)  # sort the index by ans

    index_parent = []
    for i in range(PARENT_SIZE):
        index_parent.append(index[i])

    return index_parent


def cycle_crossover(parent_generation, father, mother):
    dict = "/GApool/generation" + str(parent_generation) + '/'
    chip_father = loadchip(dict + "astar-%04d-%02d.json" % (father[0], father[1]))
    chip_mother = loadchip(dict + "astar-%04d-%02d.json" % (mother[0], mother[1]))

    father_list = chip_father.net
    mother_list = chip_mother.net

    # print(father_list)
    # print(mother_list)
    # print('-----')


def work_each_generation(parent_generation, index_parent):

    # copy the parent files for next generation

    dict_parent = GA_PATH + '/generation' + str(parent_generation) + '/'
    dcit_child = GA_PATH + '/generation' + str(parent_generation + 1) + '/'

    cnt = 0
    for i in range(PARENT_SIZE):
        src_file = dict_parent + "astar-%04d-%02d.json" % (index_parent[i][0], index_parent[i][1])
        dst_file = dcit_child + "astar-%04d-%02d.json" % (cnt, index_parent[i][1])
        shutil.copy(src_file, dst_file)
        cnt = cnt + 1

    # work for children generation
    for i in range(PARENT_SIZE):
        if (i&1) == 0:
            cycle_crossover(parent_generation, index_parent[i], index_parent[i + 1])


def genetic_algorithm_main():
    index_parent = []

    for generation in range(1, GENERATION_SIZE + 1):

        parent_generation = generation - 1

        # save each generation data in different dict
        dirt = GA_PATH + '/generation' + str(generation)
        if not os.path.exists(dirt):
            os.mkdir(dirt)

        # load parent for each parent generation
        index_parent = load_pool(parent_generation)

        work_each_generation(parent_generation, index_parent)

        break


if __name__ == '__main__':
    chipsize = readjson("gridsizes.json", 1)
    chipgate = readjson("gatelists.json", 1)
    chipnetlist = readjson("netlists.json", 3)

    # create_pool(chipsize, chipgate, chipnetlist)
    genetic_algorithm_main()
