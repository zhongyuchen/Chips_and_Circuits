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


def hillclimbing_longest(chip, steps):
    print("Starting to climb a hill...")
    print(f"Start with a cost of {chip_test.cost()}...")
    costs = [chip_test.cost()]

    for i in range(steps):
        wire_num = longest_wire(chip)
        print(f"Step {i}, trying to re-add wire {wire_num}, ", end="")
        fail = chip.del_and_add(wire_num, wire_num)
        if fail:
            print(f"failed {fail}")
            break
        else:
            print(f"cost {chip_test.cost()}")
            costs.append(chip_test.cost())

    return costs


def hillclimbing_random(chip, steps):
    print("Starting to climb a hill...")
    print(f"Start with a cost of {chip_test.cost()}...")
    costs = [chip_test.cost()]

    for i in range(steps):
        wire_num = random_wire(chip)
        print(f"Step {i}, trying to re-add wire {wire_num}, ", end="")
        fail = chip.del_and_add(wire_num, wire_num)
        if fail:
            print(f"failed {fail}")
            break
        else:
            print(f"cost {chip_test.cost()}")
            costs.append(chip_test.cost())

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
    return random.randint(0, len(chip.net) - 1)


def lineplot(costs_list, filename=""):
    # draw line plot
    data = []
    for i, costs in enumerate(costs_list):
        trace = go.Scatter(
            x=[0 for i in range(len(costs))],
            y=costs,
            mode='lines',
            name=f'Method {i}'
        )
        data.append(trace)

    layout = dict(
        title="hillclimbing costs"
    )

    if filename == "":
        filename = "hillclimbing costs"
    fig = go.Figure(data=data, layout=layout)
    py.plot(fig, filename=filename, validate=False)


if __name__ == "__main__":
    size1 = readjson("gridsizes.json", 1)
    gate1 = readjson("gatelists.json", 1)
    netlist1 = readjson("netlists.json", 1)
    steps = 1000

    print("Finding a solution with astar...")
    ans = 0
    i = 0
    while ans != len(netlist1):
        chip_test = chip(size1, gate1, netlist1)
        ans = astar(chip_test)
        print(f"{i}: {ans} connected, with a cost of {chip_test.cost()}")
        i += 1
    print("Solution found!")

    # chip_test.plot(f"astar-1-1-{chip_test.cost()}-before")
    # hillclimbing(chip_test, steps)
    # chip_test.plot(f"astar-1-1-{chip_test.cost()}-after")

    costs0 = hillclimbing_longest(chip_test, steps)
    costs1 = hillclimbing_random(chip_test, steps)
    lineplot([costs0, costs1])