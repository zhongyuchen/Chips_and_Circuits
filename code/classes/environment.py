import sys
sys.path.append('../')
from algorithms.readjson import readjson


class Environment:
    def __init__(self, number_netlist=1):
        """
            setting up the environment
        """

        self.four_direction = [[1, 0], [-1, 0], [0, 1], [0, -1]]
        number_table = 1
        if number_netlist > 3:
            number_table = number_table + 1

        self.chipsize = readjson("gridsizes.json", number_table)
        self.chipgate = readjson("gatelists.json", number_table)
        self.chipnetlist = readjson("netlists.json", number_netlist)
