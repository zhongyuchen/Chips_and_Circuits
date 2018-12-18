from algorithms.astar_spfa import AstarSpfa
from algorithms.genetic_algorithm import GeneticAlgorithm
from algorithms.hillclimber import HillClimber
import sys
sys.path.append('../')
import argparse
from classes.environment import Environment


def argparser():
    parser = argparse.ArgumentParser(description='Chips and Circuits')


    parser.add_argument('--netlist', default=1, type=int,
                        choices=[1, 2, 3, 4, 5, 6],
                        help='choose the netlist.')

    parser.add_argument('--algorithm',
                        choices=["astar", "genetic", "hillclimbing",
                                 "randomwalk", "hillclimbing_solution"],
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

    parser.add_argument('--steps', default=50, type=int,
                        help='The steps for hill climber')
    parser.add_argument('--amount', default=3, type=int,
                        help='The amount of wires changed in a transformation for hill climber')
    parser.add_argument('--retry', default=3, type=int,
                        help='The allowed max retry in a step in hill climber')
    parser.add_argument('--savechip', default=False, type=bool,
                        choices=[0, 1],
                        help='Save the best chip in json file after hill climbing')
    parser.add_argument('--showchip', default=False, type=bool,
                        choices=[0, 1],
                        help='Show the best chip after hill climbing')
    parser.add_argument('--result', default=True, type=bool,
                        choices=[0, 1],
                        help='Show the hill climbing process')
    parser.add_argument('--savechip_name', default="hillclimbing_bestchip.json", type=str,
                        help='The name of the chip json file')
    parser.add_argument('--showchip_name', default="hillclimbing_bestchip", type=str,
                        help='The name of the chip plot')
    parser.add_argument('--result_name', default="hillclimbing_result", type=str,
                        help='The name of the plot of hill climbing process')

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
    steps = args.steps
    amount = args.amount
    retry = args.retry
    savechip = args.savechip
    showchip = args.showchip
    result = args.result
    savechip_name = args.savechip_name
    showchip_name = args.showchip_name
    result_name = args.result_name

    algos = {
        "astar": AstarSpfa(env).run,
        "genetic": GeneticAlgorithm(env).run,
        "hillclimbing":
            HillClimber(env, steps=steps, amount=amount, retry=retry,
                        save_chip=savechip, show_chip=showchip,
                        show_lineplot=result,
                        chip_filename=savechip_name,
                        chip_plotname=showchip_name,
                        lineplot_filename=result_name).hillclimbing,
        "randomwalk":
            HillClimber(env, steps=steps, amount=amount, retry=retry,
                        save_chip=savechip, show_chip=showchip,
                        show_lineplot=result,
                        chip_filename=savechip_name,
                        chip_plotname=showchip_name,
                        lineplot_filename=result_name).randomwalk,
        "hillclimbing_solution":
            HillClimber(env, steps=steps, amount=amount, retry=retry,
                        save_chip=savechip, show_chip=showchip,
                        show_lineplot=result,
                        chip_filename=savechip_name,
                        chip_plotname=showchip_name,
                        lineplot_filename=result_name).hillclimbing_solution,
    }

    if args.algorithm == "astar":
        algos[args.algorithm](args.astar_complete)
    elif args.algorithm == "genetic":
        algos[args.algorithm](args.genetic_poolSize, args.genetic_parentSize, args.genetic_generationSize)
    elif args.algorithm == "hillclimbing" or \
            args.algorithm == "randomwalk" or \
            args.algorithm == "hillclimbing_solution":
        algos[args.algorithm]()
    else:
        parser.print_help()