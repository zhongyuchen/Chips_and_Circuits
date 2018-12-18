import random
import json
import sys

sys.path.append('../')
from classes.chip import Chip
from algorithms.astar_spfa import AstarSpfa
import os
import shutil
import operator

class GeneticAlgorithm:
    """
        This is the class of Genetic Algorithm.
        It helps to find better sequence of netlist of Chip.
        It uses the crossover method to generate the children.
    """

    def __init__(self, environment):
        self.POOL_SIZE = 5000
        self.PARENT_SIZE = 50  # This must be even number.
        self.GENERATION_SIZE = 30
        self.env = environment
        self.GA_PATH = "../results/GApool"

    def create_pool(self):
        """
            If the default pool of generation does not exist, produce the pool.
            For per 1000 elements, it will take 20 minutes to generate.
        """

        for i in range(self.POOL_SIZE):
            astarspfa = AstarSpfa(self.env)
            random.shuffle(astarspfa.chip.net)
            number_connected = astarspfa.astar_spfa()
            astarspfa.chip.save("GApool/generation0/astar-%04d-%02d.json" % (i, number_connected))

            print("pool_number / pool_size = ", i, '/', self.POOL_SIZE)

    def load_pool(self, gene):
        """
            Load the pool of certain generation.
            Sort the index by the number_connected and return such list.
        """

        # Scan filename.
        index = []
        files = os.listdir(self.GA_PATH + '/generation' + str(gene))
        for GA_filename in files:
            i = int(GA_filename[6:10])
            number_connected = int(GA_filename[11:13])
            index.append([i, number_connected])

        # Sort the index by number_connected.
        index.sort(key=lambda index_pair: index_pair[1], reverse=True)

        index_parent = []
        for i in range(self.PARENT_SIZE):
            index_parent.append(index[i])

        return index_parent

    def produce_child(self, dict_child, father_list, mother_list, round_number, cnt):
        """
            It uses the father_list and mother_list to generate child_list.
            For the method of crossover, it fetches some(determined by round_number) cycles from father_list,
                while the rest positions are just copy from mother_list.
            Once it generates a new child, it responses the increasing of variable 'cnt'.
        """

        list_len = len(father_list)
        visit = [0 for _ in range(list_len)]  # Mark whether the position has been detected by a cycle.

        child_list = [[] for _ in range(list_len)]  # The sequence of children generation.

        for _ in range(round_number):
            for i in range(list_len):
                if visit[i] == 1:
                    continue

                temp = father_list[i]
                pos = i
                visit[i] = 1
                child_list[i] = father_list[i]

                # Find one crossover
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

            astarspfa = AstarSpfa(self.env)
            astarspfa.chip.net = child_list
            ans = astarspfa.astar_spfa()
            astarspfa.chip.save(dict_child + "astar-%04d-%02d.json" % (cnt, ans))

            cnt = cnt + 1

        return cnt

    def fetch_net(self, filename):
        with open(filename, "r") as f:
            dic = json.load(f)
            return dic["net"]

    def cycle_crossover(self, parent_generation, father, mother, cnt, round_number):
        """
            Fetch the sequence of netlist from father and mother chips.
            Then try produce two children for each pair of parents.
            The increasing of return value 'cnt' marks how much children it have produced in reality.
        """

        dict_parent = 'GApool/generation' + str(parent_generation) + '/'
        dict_child = 'GApool/generation' + str(parent_generation + 1) + '/'

        father_list = self.fetch_net('../results/' + dict_parent + "astar-%04d-%02d.json" % (father[0], father[1]))
        mother_list = self.fetch_net('../results/' + dict_parent + "astar-%04d-%02d.json" % (mother[0], mother[1]))

        cnt = self.produce_child(dict_child, father_list, mother_list, round_number, cnt)
        cnt = self.produce_child(dict_child, mother_list, father_list, round_number, cnt)

        return cnt

    def work_each_generation(self, parent_generation, index_parent):
        """
            For each generation, it first copies the parent chips to the children pool.
            Then, for each pair of parent, call crossover function to produce children.
        """

        # Copy the parent files for next generation.
        dict_parent = self.GA_PATH + '/generation' + str(parent_generation) + '/'
        dict_child = self.GA_PATH + '/generation' + str(parent_generation + 1) + '/'

        # Variable Cnt represents the child be produced.
        cnt = 0
        for i in range(self.PARENT_SIZE):
            src_file = dict_parent + "astar-%04d-%02d.json" % (index_parent[i][0], index_parent[i][1])
            dst_file = dict_child + "astar-%04d-%02d.json" % (cnt, index_parent[i][1])
            shutil.copy(src_file, dst_file)
            cnt = cnt + 1

        # Work for children generation.
        random.shuffle(index_parent)  # Select proportionate randomly.
        for i in range(self.PARENT_SIZE):
            if not (i & 1):  # For each pair, work once.
                cnt = self.cycle_crossover(parent_generation, index_parent[i], index_parent[i + 1], cnt,
                                           random.randint(2, 5))

    def genetic_algorithm_main(self):
        """
            Work iteratively through the generations.
            Each generation is separated by "---" .
        """

        for generation in range(1, self.GENERATION_SIZE + 1):

            parent_generation = generation - 1

            # Save each generation data in different dict.
            dirt = self.GA_PATH + '/generation' + str(generation)
            if not os.path.exists(dirt):
                os.mkdir(dirt)

            # Load parent for each parent generation.
            index_parent = self.load_pool(parent_generation)

            self.work_each_generation(parent_generation, index_parent)

            print("---", generation)

    def pool_exist(self):
        # Check whether there is a such folder.

        folder_exist = 1

        dirt = "../results"
        if not os.path.exists(dirt):
            os.mkdir(dirt)
            folder_exist = 0

        dirt = self.GA_PATH
        if not os.path.exists(dirt):
            os.mkdir(dirt)
            folder_exist = 0

        dirt = self.GA_PATH + '/generation0'
        if not os.path.exists(dirt):
            os.mkdir(dirt)
            folder_exist = 0

        if not folder_exist:
            return 0

        # Check whether the pool contains enough elements.
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
