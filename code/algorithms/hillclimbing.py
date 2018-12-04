from readjson import readjson
from astar import astar
import sys
sys.path.append('../')
from classes.chip import chip
import random
import plotly
import plotly.plotly as py
import plotly.graph_objs as go


plotly.tools.set_credentials_file(username='zhongyuchen', api_key='MVlLKp3ujiU1bFQImbKP')


def hillclimbing(chip, steps, get_wire_num):
    print("Starting to climb a hill...")
    print(f"Start with a cost of {chip.cost()}...")
    costs = [chip.cost()]

    for i in range(steps):
        # get wire num function
        if get_wire_num == "random_wire":
            wire_num = random_wire(chip)
        elif get_wire_num == "longest_wire":
            wire_num = longest_wire(chip)
        else:
            print("Wrong get_wire_num function!")
            break

        # climb
        print(f"Step {i}, trying to re-add wire {wire_num}, ", end="")

        chip.delline(wire_num)
        fail = chip.addline(wire_num)
        if fail == -1:
            print(f"failed {fail}")
            break
        else:
            print(f"cost {chip.cost()}")
            costs.append(chip.cost())

    return costs


def longest_wire(chip):
    # get the number of the (first) longest wire
    wire_num = 0
    max_length = 0
    for i, wire in enumerate(chip.map_line):
        if len(wire) > max_length:
            wire_num = i
            max_length = len(wire)
    return wire_num


def longest_wires(chip):
    # get the number of the longest wire(s)
    # the cost only drops once or doesn't drop at all
    # improment ~ 2
    wires_num = []
    max_length = 0
    for i, wire in enumerate(chip.map_line):
        if len(wire) > max_length:
            wires_num = [i]
            max_length = len(wire)
        elif len(wire) == max_length:
            wires_num.append(i)

    return wires_num


def random_wire(chip):
    # get stable around 50 steps
    # improvement ~ 10
    return random.randint(0, len(chip.net) - 1)


def lineplot(costs_list, filename=""):
    # draw line plot
    data = []
    for i, costs in enumerate(costs_list):
        trace = go.Scatter(
            x=list(range(len(costs))),
            y=costs,
            mode='lines',
            name=f'Method {i}'
        )
        data.append(trace)

    layout = dict(
        title="hillclimbing costs",
        xaxis=dict(title='step'),
        yaxis=dict(title='cost')
    )

    if filename == "":
        filename = "hillclimbing costs"
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename=filename)


if __name__ == "__main__":
    size1 = readjson("gridsizes.json", 1)
    gate1 = readjson("gatelists.json", 1)
    netlist1 = readjson("netlists.json", 1)
    steps = 1000

    print("Finding a solution with astar...")
    chip0 = chip(size1, gate1, netlist1)
    ans = 0
    i = 0
    while ans != len(netlist1):
        chip0 = chip(size1, gate1, netlist1)
        ans = astar(chip0)
        print(f"{i}: {ans} connected, with a cost of {chip0.cost()}")
        i += 1
    print("Solution found!")

    chip1 = chip0
    costs0 = hillclimbing(chip0, steps, "longest_wire")
    costs1 = hillclimbing(chip1, steps, "random_wire")
    lineplot([costs0, costs1])