# from algorithms.astar_spfa import AstarSpfa

import sys
sys.path.append('../')
import argparse
from classes.environment import Environment

def argparser():
    parser = argparse.ArgumentParser(description='Chips and Circuits')
    parser.print_help()

    parser.add_argument('--netlist', default=1, type=int,
                        choices=[1, 2, 3, 4, 5, 6],
                        help='choose the netlist.')

    parser.add_argument('--algorithms',
                        choices=["astar", "genetic", "hillclimbing"],
                        help='the algorithm that is used.')

    args = parser.parse_args()

    env = Environment(args.netlist)

    print(env.chipsize)

    # test = AstarSpfa(env)
    # test.run()  # hc.random_seminar_swap_hill_climber(1000)

    # algos = {"hillclimber": algorithms.Hillclimber(env).run,
    #         "annealing": algorithms.Annealing(main_timetable).run,
    #         "greedy": algorithms.Hillclimber(main_timetable).worst_to_best,
    #         "genetic": algorithms.Genetic(generations, size).run}