from readjson import readjson, loadchip
import sys
sys.path.append('../')
from classes.chip import chip
import random
import plotly
import plotly.plotly as py
import plotly.graph_objs as go


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


def hc_longest_wires(chip, steps):
    print("Starting to climb a hill...")
    print(f"Start with a cost of {chip.cost()}...")
    costs = [chip.cost()]

    for i in range(steps):
        # get wire num function
        wire_num = longest_wires(chip)

        # climb
        print(f"Step {i}, trying to re-add wire {wire_num}, ", end="")
        chip.rollback_wires = []

        # delete the selected wires
        for w in wire_num:
            chip.delline(w, 1)

        # re-add
        random.shuffle(wire_num)
        for w in wire_num:
            fail = chip.addline(w, 1)
            if fail == -1:
                # fail
                print(f"failed", end=" ")
                # rollback
                chip.rollback()
                break

        print(f"cost {chip.cost()}")
        costs.append(chip.cost())

    return costs


def random_wire(chip):
    # get stable around 50 steps
    # improvement ~ 10
    return random.randint(0, len(chip.net) - 1)


def hc_random_wire(chip, steps):
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
    print("Starting to climb a hill...")
    print(f"Start with a cost of {chip.cost()}...")
    costs = [chip.cost()]

    for i in range(steps):
        # get wire num function
        wire_num = random_wires(chip, amount)

        # climb
        print(f"Step {i}, trying to re-add wire {wire_num}, ", end="")
        chip.rollback_wires = []

        # delete the selected wires
        for w in wire_num:
            chip.delline(w, 1)

        # re-add
        random.shuffle(wire_num)
        for w in wire_num:
            fail = chip.addline(w, 1)
            if fail == -1:
                # fail
                print(f"failed", end=" ")
                # rollback
                chip.rollback()
                break

        print(f"cost {chip.cost()}")
        costs.append(chip.cost())

    return costs


def hc_random_wires_better(chip, steps, amount):
    print("Starting to climb a hill...")
    print(f"Start with a cost of {chip.cost()}...")
    costs = [chip.cost()]

    for i in range(steps):
        # get wire num function
        wire_num = random_wires(chip, amount)

        # climb
        print(f"Step {i}, trying to re-add wire {wire_num}, ", end="")
        old_cost = chip.cost()
        chip.rollback_wires = []

        # delete the selected wires
        for w in wire_num:
            chip.delline(w, 1)

        # re-add
        random.shuffle(wire_num)
        fail = 0
        for w in wire_num:
            fail = chip.addline(w, 1)
            if fail == -1:
                # fail
                print("failed", end=" ")
                break

        if old_cost <= chip.cost() or fail == -1:
            chip.rollback()
            print("rollback", end=" ")

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

    steps = 500

    filename = "astar-1-2-000-0523.json"
    chip0 = loadchip(filename)
    chip1 = loadchip(filename)
    chip2 = loadchip(filename)
    chip3 = chip0.copy()

    cn = []
    cn.append([hc_random_wire(chip0, steps), "random_wire"])
    # cn.append([hc_random_wires(chip1, steps, 3), "random_wires"])
    # cn.append([hc_random_wires_better(chip2, steps, 3), "random_wires_better"])
    cn.append([hc_random_wires_better(chip3, steps, 3), "random_wires_better"])
    lineplot(cn)

    # problem: just make a deep copy
    # randomly take one wire, try to connect the shortest option and pierce through all (some?) the other wires
    # put back in different orders
    # ppa
    # hillclimbing for a solution
