from readjson import loadchip
from astar import astar
import copy


def shuffle_random_wires(chip, amount=2, ):



def hc_solution(chip, steps=1000, amount=2, retry=1, filename="hc-"):
    # hill climbing for finding a solution
    print("Starting climbing for a solution...")
    print(f"Start with a cost of {chip.cost()}...")
    costs = [chip.cost()]
    fail_num = copy.deepcopy(steps)
    chip_best = copy.deepcopy(chip)

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

            # success check list
            check_list = [fail != -1]
            if function == "reduce":
                check_list.append(chip_temp_temp.cost() < chip.cost())

            # success
            if sum(check_list) == len(check_list):
                chip = chip_temp_temp
                fail_num -= 1
                print(f"success", end=" ")
                break

        if chip.cost() < chip_best.cost():
            chip_best = chip

        print(f"cost {chip.cost()}")
        costs.append(chip.cost())

    # save the best!
    filename += "%04d.json" % chip_best.cost()
    chip_best.save(filename)

    print(f"All done! {steps} steps and {fail_num} fails")
    return costs


if __name__ == "__main__":
