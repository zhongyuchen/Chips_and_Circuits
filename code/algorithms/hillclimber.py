import sys
sys.path.append('../')
import random
import copy
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from astar_spfa import AstarSpfa
from classes.environment import Environment
from classes.chip import Chip


plotly.tools.set_credentials_file(username='chipsandcircuits', api_key='9A2KpJpwzbsL04AhXSTY')


class HillClimber:
    """
        Hill Climber:
            hillclimbing: start with a valid solution, try to get lower cost;
            randomwalk: start with a valid solution, take a random walk to get other valid solutions;
            hillclimbing_solution: start with an invalid solution, try to get more connected solution.
    """

    def __init__(self, environment, steps=20, amount=3, retry=3,
                 save_chip=False, show_chip=False, show_lineplot=True,
                 chip_filename="hillclimbing_bestchip.json",
                 chip_plotname="hillclimbing_bestchip",
                 lineplot_filename="hillclimbing_result"):
        self.astarspfa = AstarSpfa(environment)
        self.chip = Chip(environment)
        self.steps = steps
        self.save_chip, self.chip_filename = save_chip, chip_filename
        self.show_chip, self.chip_plotname = show_chip, chip_plotname
        self.show_lineplot, self.lineplot_filename = show_lineplot, lineplot_filename
        self.amount = amount
        self.retry = retry

    def hillclimbing(self, random_walk=False):
        """
            hillclimbing: try to get a chip with lower cost

            start chip:
                a valid (fully connected) chip
            chip transfromation (for a certain times):
                delete a certain amount of random wires,
                and add them back in a random order,
                if it fails in adding wire or fails in getting better solution,
                retry a different order for a certain times.
            Accept:
                accept the result that is fully connected with a lower chip cost.
        """

        # use astar spfa to finad a valid solution first
        self.astarspfa.wrapper(self.chip, valid=True)

        print("Starting to climb a hill...")
        print(f"Start with a chip with cost of {self.chip.cost()}...")
        costs = [self.chip.cost()]
        fail_num = copy.deepcopy(self.steps)
        chip_best = copy.deepcopy(self.chip)

        # hillclimbing for a certain steps
        for i in range(self.steps):
            # get wire nums function
            wire_num = self.chip.random_wires(self.amount)

            # climb
            print(f"Step {i}, trying to re-add wire {wire_num}, ", end="")
            chip_temp = copy.deepcopy(self.chip)

            # delete the randomly selected wires
            for w in wire_num:
                chip_temp.delline(w)

            # re-add the deleted wires
            for j in range(self.retry):
                # try another random order to put them back
                random.shuffle(wire_num)
                chip_temp_temp = copy.deepcopy(chip_temp)

                fail = 0
                for w in wire_num:
                    fail = chip_temp_temp.addline(w)
                    if fail == -1:
                        # fail in adding wires back
                        break

                if fail != -1 and (random_walk or chip_temp_temp.cost() < self.chip.cost()):
                    # succeed in adding all the wires back
                    # and get a chip with lower cost
                    self.chip = chip_temp_temp
                    if not random_walk:
                        fail_num -= 1
                        print(f"gets better", end=", ")
                    break

            # record the best chip (for random walk)
            if self.chip.cost() < chip_best.cost():
                chip_best = self.chip

            # cost list, for drawing a line plot to show the results
            print(f"cost {self.chip.cost()}")
            costs.append(self.chip.cost())

        print(f"All done! {self.steps} steps", end="")
        if not random_walk:
            print(f", among which {self.steps - fail_num} steps get better!")
        else:
            print("!")

        # save the best chip in json file
        if self.save_chip:
            chip_best.save(self.chip_filename)

        # show the best chip in plotle
        if self.show_chip:
            chip_best.plot(self.chip_plotname)

        # draw a line plot to show the hillclimbing result
        if self.show_lineplot:
            self.lineplot(costs)

    def randomwalk(self):
        """
            randomwalk: talk a random walk to get more solutions

            This has the same structure as hillclimbing,
            except that after the transformation,
            as long as the result is fully connected,
            it will be accepted whether or not it has a lower cost
        """
        return self.hillclimbing(random_walk=True)

    def hillclimbing_solution(self):
        """
            hillclimbing_solution: try to get more (fully) connected chip

            start chip:
                a partly connected chip,
                in this sequence of adding wires, it can not be fully connected
            transformation:
                randomly take a chunk (certain length) of that sequence,
                shuffle this chunk, and put this chunk back to the same position,
                try to find a solution in this new sequence of add wires.
            accept:
                accept the result with more connected wires
        """

        # hill climbing for finding a solution
        print("Starting climbing for a solution...")
        success_num = 0

        # find a (invalid) chip first
        connected = self.astarspfa.wrapper(self.chip, valid=False)

        connected_list = [copy.deepcopy(connected)]
        print(f"Starting with a {connected}/{len(self.chip.net)}-connected chip...")

        # hillclimbing to get more connected wires
        for i in range(self.steps):
            # got fully connected chip, finished
            if connected == len(self.chip.net):
                break
            # retry for certain times
            for j in range(self.retry):
                # new a chip copy
                print(f"Step {i}-{j},", end=" ")
                chip_test = copy.deepcopy(self.chip)
                chip_test.clean()
                # transformation
                chip_test.shuffle_random_wires(self.amount)

                # accept the more connected chip
                connected_test = self.astarspfa.wrapper(chip_test)
                if connected_test > connected:
                    connected = copy.deepcopy(connected_test)
                    self.chip = copy.deepcopy(chip_test)
                    success_num += 1
                    break

            print(f"Step {i} result: {connected}/{len(self.chip.net)}")
            connected_list.append(copy.deepcopy(connected))

        print(f"All done! {len(connected_list) - 1} steps, "
              f"among which {success_num} steps get better, "
              f"{connected}/{len(self.chip.net)} connected")

        # save the best chip
        if self.save_chip:
            self.chip.save(self.chip_filename)

        # show the best chip
        if self.show_chip:
            self.chip.plot(self.chip_plotname)

        # draw a line plot of the hillclimbing result
        if self.show_lineplot:
            self.lineplot(connected_list)

    def lineplot(self, cost):
        """
            lineplot: draw a line plot to show the hillclimbing process
        """

        data = []
        trace = go.Scatter(
            x=list(range(len(cost))),
            y=cost,
            mode='lines',
        )
        data.append(trace)

        layout = dict(
            title=self.lineplot_filename,
            xaxis=dict(title='Step'),
            yaxis=dict(title='Value')
        )

        fig = go.Figure(data=data, layout=layout)
        py.plot(fig, filename=self.lineplot_filename)


if __name__ == "__main__":
    env = Environment(2)
    hillclimber = HillClimber(env,
                              save_chip=True, show_chip=True, show_lineplot=True,
                              chip_filename="hc_bestchip.json",
                              chip_plotname="hc_bestchip",
                              lineplot_filename="hc_result")
    hillclimber.hillclimbing()
    hillclimber.randomwalk()
    hillclimber.hillclimbing_solution()