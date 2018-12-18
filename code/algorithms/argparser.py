from algorithms.astar_spfa import AstarSpfa
from algorithms.genetic_algorithm import GeneticAlgorithm

import sys
sys.path.append('../')
import argparse
from classes.environment import Environment


def argparser():
    parser = argparse.ArgumentParser(description='Chips and Circuits')


    parser.add_argument('--netlist', default=1, type=int,
                        choices=[1, 2, 3, 4, 5, 6],
                        help='choose the netlist.')

    parser.add_argument('--algorithm', default="astar",
                        choices=["astar", "genetic", "hillclimbing"],
                        help='the algorithm that is used.')

    parser.add_argument('--astar-complete', default=1, type=int,
                        choices=[0, 1],
                        help='Whether to find a complete solution')

    parser.add_argument('--genetic-poolSize', default=500, type=int,
                        help='The pool size for genetic algorithm')

    parser.add_argument('--genetic-parentSize', default=25, type=int,
                        help='The parent size(pair) for genetic algorithm')

    parser.add_argument('--genetic-generationSize', default=30, type=int,
                        help='The generation size for genetic algorithm')

    args = parser.parse_args()


    if args.algorithm != 'astar' and args.astar_complete != True:
        parser.error('--astar-complete can only be set when --algorithm=astar.')

    if args.algorithm != "genetic" and args.genetic_poolSize != 500:
        parser.error('--genetic-poolSize can only be set when --algorithm=genetic.')

    if args.algorithm != 'genetic' and args.genetic_parentSize != 25:
        parser.error('--genetic-parentSize can only be set when --algorithm=genetic.')

    if args.algorithm != 'genetic' and args.genetic_generationSize != 30:
        parser.error('--genetic-generationSize can only be set when --algorithm=genetic.')

    env = Environment(args.netlist)

    algos = {"astar": AstarSpfa(env).run,
             "genetic": GeneticAlgorithm(env).run}

    if args.algorithm == "astar":
        algos[args.algorithm](args.astar_complete)
    if args.algorithm == "genetic":
        algos[args.algorithm](args.genetic_poolSize, args.genetic_parentSize, args.genetic_generationSize)

    parser.print_help()