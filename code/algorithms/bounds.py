from readjson import readjson


def theoretical_lower_bound(gates, nets):
    bound = 0
    for net in nets:
        bound += abs(gates[net[0]][0] - gates[net[1]][0]) + \
                 abs(gates[net[0]][1] - gates[net[1]][1])
    return bound


def theoretical_upper_bound(size):
    return (size[0] - 1) * size[1] * size[2] + \
           size[0] * (size[1] - 1) * size[2] + \
           size[0] * size[1] * (size[2] - 1)


def upper_bound_0(gates, nets, size):
    return len(nets) * 2 + size[0] * size[1] * size[2] - len(gates)


if __name__ == "__main__":
    gates_1 = readjson("gatelists.json", 1)
    gates_2 = readjson("gatelists.json", 2)
    netlist_1 = readjson("netlists.json", 1)
    netlist_2 = readjson("netlists.json", 2)
    netlist_3 = readjson("netlists.json", 3)
    netlist_4 = readjson("netlists.json", 4)
    netlist_5 = readjson("netlists.json", 5)
    netlist_6 = readjson("netlists.json", 6)
    size_1 = readjson("gridsizes.json", 1)
    size_2 = readjson("gridsizes.json", 2)


    print(theoretical_lower_bound(gates_1, netlist_1), end = ',')
    print(theoretical_lower_bound(gates_1, netlist_2), end = ',')
    print(theoretical_lower_bound(gates_1, netlist_3), end = ',')
    print(theoretical_lower_bound(gates_2, netlist_4), end = ',')
    print(theoretical_lower_bound(gates_2, netlist_5), end = ',')
    print(theoretical_lower_bound(gates_2, netlist_6))

    print(theoretical_upper_bound(size_1), end = ',')
    print(theoretical_upper_bound(size_2))

    print(upper_bound_0(gates_1, netlist_1, size_1), end = ',')
    print(upper_bound_0(gates_1, netlist_2, size_1), end = ',')
    print(upper_bound_0(gates_1, netlist_3, size_1), end = ',')
    print(upper_bound_0(gates_2, netlist_4, size_2), end = ',')
    print(upper_bound_0(gates_2, netlist_5, size_2), end = ',')
    print(upper_bound_0(gates_2, netlist_6, size_2))
