from readjson import readjson, loadchip
import sys
sys.path.append('../')
from classes.chip import chip
import random
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
import copy


plotly.tools.set_credentials_file(username='zhongyuchen', api_key='MVlLKp3ujiU1bFQImbKP')


def longest_wire(chip):
    # get the number of the (first) longest wire
    wire_num = 0
    max_length = 0
    for i, wire in enumerate(chip.map_line):
        if len(wire) > max_length:
            wire_num = i
            max_length = len(wire)
    return wire_num


def hc_longest_wire(chip, step):
    # the cost drops once for ~ 2, or doesn't drop at all

    print("Starting to climb a hill...")
    print(f"Start with a cost of {chip.cost()}...")
    costs = [chip.cost()]

    for i in range(steps):
        # get wire num function
        wire_num = longest_wire(chip)

        # climb
        print(f"Step {i}, trying to re-add wire {wire_num}, ", end="")

        # re-add the selected wires
        chip.delline(wire_num)
        chip.addline(wire_num)

        print(f"cost {chip.cost()}")
        costs.append(chip.cost())

    return costs


def random_wire(chip):
    # get stable around 50 steps
    # improvement ~ 10
    return random.randint(0, len(chip.net) - 1)


def hc_random_wire(chip, steps):
    # keep dropping for 80 steps, cost reduces ~ 10
    print("Starting to climb a hill...")
    print(f"Start with a cost of {chip.cost()}...")
    costs = [chip.cost()]

    for i in range(steps):
        # get wire num function
        wire_num = random_wire(chip)

        # climb
        print(f"Step {i}, trying to re-add wire {wire_num}, ", end="")

        # re-add the selected wires
        chip.delline(wire_num)
        chip.addline(wire_num)

        print(f"cost {chip.cost()}")
        costs.append(chip.cost())

    return costs


def random_wires(chip, amount):
    # randomly select a certain amount of wires
    length = len(chip.net)
    wires = []
    for i in range(amount):
        wires.append(random.randint(0, length - 1))
    return wires


def hc_random_wires(chip, steps, amount):
    # sometimes gets good optimization
    # but highly unstable, comparing to hc_random_wires_reduce
    # good for getting states that aren't reachable for hc_random_wires_reduce
    print("Starting to climb a hill...")
    print(f"Start with a cost of {chip.cost()}...")
    costs = [chip.cost()]

    for i in range(steps):
        # get wire num function
        wire_num = random_wires(chip, amount)

        # climb
        print(f"Step {i}, trying to re-add wire {wire_num}, ", end="")
        chip_temp = copy.deepcopy(chip)

        # delete the selected wires
        for w in wire_num:
            chip_temp.delline(w)

        # re-add
        random.shuffle(wire_num)
        fail = 0
        for w in wire_num:
            fail = chip_temp.addline(w)
            if fail == -1:
                # fail
                print(f"failed", end=" ")
                break

        # success
        if fail != -1:
            chip = chip_temp

        print(f"cost {chip.cost()}")
        costs.append(chip.cost())

    return costs


def hc_random_wires_reduce(chip, steps, amount):
    # quite promising
    # after 1500 steps, cost still drops
    print("Starting to climb a hill...")
    print(f"Start with a cost of {chip.cost()}...")
    costs = [chip.cost()]

    for i in range(steps):
        # get wire num function
        wire_num = random_wires(chip, amount)

        # climb
        print(f"Step {i}, trying to re-add wire {wire_num}, ", end="")
        chip_temp = copy.deepcopy(chip)

        # delete the selected wires
        for w in wire_num:
            chip_temp.delline(w)

        # re-add
        random.shuffle(wire_num)
        fail = 0
        for w in wire_num:
            fail = chip_temp.addline(w)
            if fail == -1:
                # fail
                print("failed", end=" ")
                break

        # success
        if chip_temp.cost() < chip.cost() and fail != -1:
            chip = chip_temp

        print(f"cost {chip.cost()}")
        costs.append(chip.cost())

    return costs


def lineplot(costs_names, filename=""):
    costs_list = []
    name_list = []
    for cost_name in costs_names:
        costs_list.append(cost_name[0])
        name_list.append(cost_name[1])

    # draw line plot
    data = []
    for i, costs in enumerate(costs_list):
        trace = go.Scatter(
            x=list(range(len(costs))),
            y=costs,
            mode='lines',
            name=name_list[i]
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
    netlist2 = readjson("netlists.json", 2)

    steps = 2000

    chip0 = loadchip("astar-1-2-000-0523.json")
    # chip1 = copy.deepcopy(chip0)
    chip2 = copy.deepcopy(chip0)
    chip3 = copy.deepcopy(chip0)

    cn = []
    # cn.append([hc_longest_wire(chip0, steps), "hc_longest_wire"])
    # cn.append([hc_random_wire(chip1, steps), "hc_random_wire"])
    cn.append([hc_random_wires(chip2, steps, 3), "hc_random_wires"])
    cn.append([hc_random_wires_reduce(chip3, steps, 3), "hc_random_wires_reduce"])
    lineplot(cn)

    # randomly take one wire, try to connect the shortest option and pierce through all (some?) the other wires
    # put back in different orders
    # ppa
    # hillclimbing for a solution
