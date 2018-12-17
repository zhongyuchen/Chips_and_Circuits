from readjson import loadchip
import sys
sys.path.append('../')
import random
import copy
import plotly
import plotly.plotly as py
import plotly.graph_objs as go


plotly.tools.set_credentials_file(username='chipsandcircuits', api_key='9A2KpJpwzbsL04AhXSTY')


class HillClimber:
    def __init__(self, startchip_filename="astar-2-000-0523.json", steps=500,
                 save_chip=False, show_chip=False, show_lineplot=True,
                 chip_filename="hillclimbing_bestchip.json",
                 chip_plotname="hillclimbing_bestchip",
                 lineplot_filename="hillclimbing_result"):
        self.chip = loadchip(startchip_filename)
        self.steps = steps
        self.save_chip, self.chip_filename = save_chip, chip_filename
        self.show_chip, self.chip_plotname = show_chip, chip_plotname
        self.show_lineplot, self.lineplot_filename = show_lineplot, lineplot_filename

    def hillclimbing(self, random_walk=False, amount=6, retry=30):
        print("Starting to climb a hill...")
        print(f"Start with a chip with cost of {self.chip.cost()}...")
        costs = [self.chip.cost()]
        fail_num = copy.deepcopy(self.steps)
        chip_best = copy.deepcopy(self.chip)

        for i in range(self.steps):
            # get wire num function
            wire_num = self.chip.random_wires(amount)

            # climb
            print(f"Step {i}, trying to re-add wire {wire_num}, ", end="")
            chip_temp = copy.deepcopy(self.chip)

            # delete the selected wires
            for w in wire_num:
                chip_temp.delline(w)

            # re-add
            for j in range(retry):
                # try another random order
                random.shuffle(wire_num)
                chip_temp_temp = copy.deepcopy(chip_temp)

                fail = 0
                for w in wire_num:
                    fail = chip_temp_temp.addline(w)
                    if fail == -1:
                        # fail
                        break

                # success
                if fail != -1 and (random_walk or chip_temp_temp.cost() < self.chip.cost()):
                    self.chip = chip_temp_temp
                    if not random_walk:
                        fail_num -= 1
                        print(f"gets better", end=", ")
                    break

            if self.chip.cost() < chip_best.cost():
                chip_best = self.chip

            print(f"cost {self.chip.cost()}")
            costs.append(self.chip.cost())

        print(f"All done! {self.steps} steps", end="")
        if not random_walk:
            print(f", among which {self.steps - fail_num} steps get better!")
        else:
            print("!")

        # save the best!
        if self.save_chip:
            chip_best.save(self.chip_filename)

        if self.show_chip:
            chip_best.plot(self.chip_plotname)

        if self.show_lineplot:
            self.lineplot(costs)

    def randomwalk(self, amount=6, retry=30):
        return self.hillclimbing(random_walk=True, amount=amount, retry=retry)

    def lineplot(self, cost):
        # draw line plot
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
    hillclimber = HillClimber(startchip_filename="astar-2-000-0523.json", steps=30,
                              save_chip=True, show_chip=True, show_lineplot=True,
                              chip_filename="hc_bestchip.json",
                              chip_plotname="hc_bestchip",
                              lineplot_filename="hc_result")
    # hillclimber.hillclimbing()
    # hillclimber.randomwalk()