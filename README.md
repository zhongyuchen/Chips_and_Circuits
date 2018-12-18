# Chips_and_Circuits

## Author 
- Tiancheng Guo (12455814)
- Zhongyu Chen (12455822)

## Structure
- Put code, data and results in different locations.

## Usage
```angular2html
usage: main.py [-h] [--netlist {1,2,3,4,5,6}]
               [--algorithm {astar,genetic,hillclimbing,randomwalk,hillclimbing_solution}]
               [--astar-complete {0,1}] [--genetic-poolSize GENETIC_POOLSIZE]
               [--genetic-parentSize GENETIC_PARENTSIZE]
               [--genetic-generationSize GENETIC_GENERATIONSIZE]
               [--steps STEPS] [--amount AMOUNT] [--retry RETRY]
               [--savechip {0,1}] [--showchip {0,1}] [--result {0,1}]
               [--savechip_name SAVECHIP_NAME] [--showchip_name SHOWCHIP_NAME]
               [--result_name RESULT_NAME]

Chips and Circuits

optional arguments:
  -h, --help            show this help message and exit
  --netlist {1,2,3,4,5,6}
                        choose the netlist.
  --algorithm {astar,genetic,hillclimbing,randomwalk,hillclimbing_solution}
                        the algorithm that is used.
  --astar-complete {0,1}
                        Whether to find a complete solution
  --genetic-poolSize GENETIC_POOLSIZE
                        The pool size for genetic algorithm
  --genetic-parentSize GENETIC_PARENTSIZE
                        The parent size(pair) for genetic algorithm
  --genetic-generationSize GENETIC_GENERATIONSIZE
                        The generation size for genetic algorithm
  --steps STEPS         The steps for hill climber
  --amount AMOUNT       The amount of wires changed in a transformation for
                        hill climber
  --retry RETRY         The allowed max retry in a step in hill climber
  --savechip {0,1}      Save the best chip in json file after hill climbing
  --showchip {0,1}      Show the best chip after hill climbing
  --result {0,1}        Show the hill climbing process
  --savechip_name SAVECHIP_NAME
                        The name of the chip json file
  --showchip_name SHOWCHIP_NAME
                        The name of the chip plot
  --result_name RESULT_NAME
                        The name of the plot of hill climbing process
```

## Example
```angular2html
python main.py --netlist 2 --algorithm hillclimbing
               --steps 300 --amount 6 --retry 20
               --savechip 1 --showchip 1 --result 1
               --savechip_name chip.json
               --showchip_name chip
               --result_name hillclimbing_result
```

## Requirements
```angular2html
plotly==3.4.0
python==3.6.6
```