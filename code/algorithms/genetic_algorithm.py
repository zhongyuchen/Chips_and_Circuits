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
from astar_spfa import astar_spfa
import os
import shutil
import operator

POOL_SIZE = 5000
PARENT_SIZE = 50  # this must be even number
GENERATION_SIZE = 30
GA_PATH = "../../results/GApool"

chipsize = readjson("gridsizes.json", 1)
chipgate = readjson("gatelists.json", 1)
chipnetlist = readjson("netlists.json", 3)


def create_pool():
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


def produce_child(dict_child, father_list, mother_list, round_number, cnt):
    list_len = len(father_list)
    visit = [0 for i in range(list_len)]

    child_list = [[] for i in range(list_len)]

    # round 1
    for t in range(round_number):
        for i in range(list_len):
            if visit[i] == 1:
                continue

            temp = father_list[i]
            pos = i
            visit[i] = 1
            child_list[i] = father_list[i]
            # find one crossover
            while not operator.eq(mother_list[pos], temp):
                for j in range(list_len):
                    if operator.eq(father_list[j], mother_list[pos]):
                        pos = j
                        visit[pos] = 1
                        child_list[pos] = father_list[pos]
                        break
            break

    for j in range(list_len):
        if len(child_list[j]):
            pass
        else:
            child_list[j] = mother_list[j]

    if operator.eq(child_list, mother_list) or operator.eq(child_list, father_list):
        pass
    else:
        # save child_list in child_chip.net
        child_chip = chip(chipsize, chipgate, chipnetlist)
        child_chip.net = child_list
        ans = astar_spfa(child_chip)
        child_chip.save(dict_child + "astar-%04d-%02d.json" % (cnt, ans))
        cnt = cnt + 1

    return cnt


def cycle_crossover(parent_generation, father, mother, cnt, round_number):
    dict_parent = 'GApool/generation' + str(parent_generation) + '/'
    dict_child = 'GApool/generation' + str(parent_generation + 1) + '/'
    chip_father = loadchip(dict_parent + "astar-%04d-%02d.json" % (father[0], father[1]))
    chip_mother = loadchip(dict_parent + "astar-%04d-%02d.json" % (mother[0], mother[1]))

    cnt = produce_child(dict_child, chip_father.net, chip_mother.net, round_number, cnt)

    # swap father_list and mother_list
    cnt = produce_child(dict_child, chip_mother.net, chip_father.net, round_number, cnt)

    return cnt


def work_each_generation(parent_generation, index_parent):
    # copy the parent files for next generation

    dict_parent = GA_PATH + '/generation' + str(parent_generation) + '/'
    dict_child = GA_PATH + '/generation' + str(parent_generation + 1) + '/'

    cnt = 0
    for i in range(PARENT_SIZE):
        src_file = dict_parent + "astar-%04d-%02d.json" % (index_parent[i][0], index_parent[i][1])
        dst_file = dict_child + "astar-%04d-%02d.json" % (cnt, index_parent[i][1])
        shutil.copy(src_file, dst_file)
        cnt = cnt + 1

    # work for children generation
    random.shuffle(index_parent)  # select proportionate randomly
    for i in range(PARENT_SIZE):
        print(i, cnt)
        if (i & 1) == 0:
            cnt = cycle_crossover(parent_generation, index_parent[i], index_parent[i + 1], cnt, random.randint(2, 5))


def genetic_algorithm_main():
    for generation in range(1, GENERATION_SIZE + 1):

        parent_generation = generation - 1

        # save each generation data in different dict
        dirt = GA_PATH + '/generation' + str(generation)
        if not os.path.exists(dirt):
            os.mkdir(dirt)

        # load parent for each parent generation
        index_parent = load_pool(parent_generation)

        work_each_generation(parent_generation, index_parent)

        print("---", generation)


if __name__ == '__main__':
    # create_pool()

    genetic_algorithm_main()  # fitness proportionate selection
