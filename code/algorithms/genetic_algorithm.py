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

chipsize = readjson("gridsizes.json", 1)
chipgate = readjson("gatelists.json", 1)
chipnetlist = readjson("netlists.json", 3)


class Genetic_algorithm():
    def __init__(self):
        self.POOL_SIZE = 5000
        self.PARENT_SIZE = 50  # this must be even number
        self.GENERATION_SIZE = 30
        self.GA_PATH = "../../results/GApool"

    def create_pool(self, ):
        """
            If the default pool of generation does not exist, produce the pool.
            For per 1000 elements, it will take 20 minutes to generate.
        """

        for i in range(self.POOL_SIZE):
            current_chip = chip(chipsize, chipgate, chipnetlist)
            number_connected = astar_spfa.astar_spfa(current_chip)
            current_chip.save("GApool/generation0/astar-%04d-%02d.json" % (i, number_connected))

            with open("pool_record.txt", "a") as f:
                print(i, number_connected, file=f)

    def load_pool(self, gene):
        """
            Load the pool of certain generation.
            Sort the index by the number_connected and return such list.
        """

        # scan filename.
        index = []
        files = os.listdir(self.GA_PATH + '/generation' + str(gene))
        for GA_filename in files:
            i = int(GA_filename[6:10])
            number_connected = int(GA_filename[11:13])
            index.append([i, number_connected])

        # sort the index by number_connected
        index.sort(key=lambda index_pair: index_pair[1], reverse=True)

        index_parent = []
        for i in range(self.PARENT_SIZE):
            index_parent.append(index[i])

        return index_parent

    def produce_child(self, dict_child, father_list, mother_list, round_number, cnt):
        list_len = len(father_list)
        visit = [0 for _ in range(list_len)]

        child_list = [[] for _ in range(list_len)]

        # round 1
        for _ in range(round_number):
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
            if not len(child_list[j]):
                child_list[j] = mother_list[j]

        if not (operator.eq(child_list, mother_list) or operator.eq(child_list, father_list)):
            # save child_list in child_chip.net
            child_chip = chip(chipsize, chipgate, chipnetlist)
            child_chip.net = child_list
            ans = astar_spfa(child_chip)
            child_chip.save(dict_child + "astar-%04d-%02d.json" % (cnt, ans))
            cnt = cnt + 1

        return cnt

    def cycle_crossover(self, parent_generation, father, mother, cnt, round_number):
        dict_parent = 'GApool/generation' + str(parent_generation) + '/'
        dict_child = 'GApool/generation' + str(parent_generation + 1) + '/'
        chip_father = loadchip(dict_parent + "astar-%04d-%02d.json" % (father[0], father[1]))
        chip_mother = loadchip(dict_parent + "astar-%04d-%02d.json" % (mother[0], mother[1]))

        cnt = self.produce_child(dict_child, chip_father.net, chip_mother.net, round_number, cnt)

        # swap father_list and mother_list
        cnt = self.produce_child(dict_child, chip_mother.net, chip_father.net, round_number, cnt)

        return cnt

    def work_each_generation(self, parent_generation, index_parent):
        """
            For each generation, it first copies the parent chips to the children pool.
            Then, for each pair of parent, call crossover function to produce children.
        """

        # copy the parent files for next generation

        dict_parent = self.GA_PATH + '/generation' + str(parent_generation) + '/'
        dict_child = self.GA_PATH + '/generation' + str(parent_generation + 1) + '/'

        # cnt represents the child be produced.
        cnt = 0
        for i in range(self.PARENT_SIZE):
            src_file = dict_parent + "astar-%04d-%02d.json" % (index_parent[i][0], index_parent[i][1])
            dst_file = dict_child + "astar-%04d-%02d.json" % (cnt, index_parent[i][1])
            shutil.copy(src_file, dst_file)
            cnt = cnt + 1

        # work for children generation

        random.shuffle(index_parent) # select proportionate randomly
        for i in range(self.PARENT_SIZE):
            if not (i & 1):  # for each pair, work once
                cnt = self.cycle_crossover(parent_generation, index_parent[i], index_parent[i + 1], cnt,
                                           random.randint(2, 5))

    def genetic_algorithm_main(self):
        for generation in range(1, self.GENERATION_SIZE + 1):

            parent_generation = generation - 1

            # save each generation data in different dict
            dirt = self.GA_PATH + '/generation' + str(generation)
            if not os.path.exists(dirt):
                os.mkdir(dirt)

            # load parent for each parent generation
            index_parent = self.load_pool(parent_generation)

            self.work_each_generation(parent_generation, index_parent)

            print("---", generation)

    def pool_exist(self):

        # Check whether there is a such folder
        dirt = self.GA_PATH + '/generation0'
        if not os.path.exists(dirt):
            return 0

        # Check whether the pool contains enough elements
        index = self.load_pool(0)
        if len(index) < self.PARENT_SIZE:
            return 0

        return 1

    def run(self):
        """
            It is the main function of genetic algorithm to be used by others.
            It first check if there is a existing pool, which ensures the process work.
            Then, it call the function of genetic_algorithm_main.
        """

        if not self.pool_exist():
            self.create_pool()

        self.genetic_algorithm_main()


if __name__ == '__main__':

    GA = Genetic_algorithm()
    GA.run()
