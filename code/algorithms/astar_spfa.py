import random
# from readjson import readjson
import sys
sys.path.append('../')
from classes.chip import Chip
from classes.environment import Environment

# chipsize = readjson("gridsizes.json", 1)
# chipgate = readjson("gatelists.json", 1)
# chipnetlist = readjson("netlists.json", 1)


class AstarSpfa:
    """
        This is the method to find path in the chip.
        Use the algorithm called SPFA.
        Once the user wants a simpler algorithm Breadth-First-Search to implement,
            just sets the variable 'use_spfa' as 0.
    """

    def __init__(self, environment):
        self.env = environment
        self.chip = Chip(self.env)

    def astar_spfa(self):
        cnt = 0
        for pair_gate in self.chip.net:
            cost = self.chip.addline(cnt)
            flag_conflict = 0
            # If there is a conflict occurs, the 'flag_conflict' will be 1.

            if cost == -1:

                flag_conflict = 1

                # for pair_gate[0]
                # four points in level 0

                if flag_conflict == 1:
                    for i in range(4):
                        if flag_conflict == 0:
                            break
                        tx = self.chip.gate[pair_gate[0]][0] + self.env.four_direction[i][0]
                        ty = self.chip.gate[pair_gate[0]][1] + self.env.four_direction[i][1]

                        if tx < 0 or tx >= self.chip.size[1] or ty < 0 or ty >= self.chip.size[2]:
                            continue

                        net_num = self.chip.used_wired[0][tx][ty]

                        flag_conflict = self.chip.del_and_add(net_num, cnt)

                if flag_conflict == 1:
                    # the point in level 1
                    net_num = self.chip.used_wired[1][self.chip.gate[pair_gate[0]][0]][self.chip.gate[pair_gate[0]][1]]
                    flag_conflict = self.chip.del_and_add(net_num, cnt)

                # for pair_gate[1]
                if flag_conflict == 1:
                    for i in range(4):
                        if flag_conflict == 0:
                            break
                        tx = self.chip.gate[pair_gate[1]][0] + self.env.four_direction[i][0]
                        ty = self.chip.gate[pair_gate[1]][1] + self.env.four_direction[i][1]

                        if tx < 0 or tx >= self.chip.size[1] or ty < 0 or ty >= self.chip.size[2]:
                            continue

                        net_num = self.chip.used_wired[0][tx][ty]

                        flag_conflict = self.chip.del_and_add(net_num, cnt)

                if flag_conflict == 1:
                    # The point in level 1
                    net_num = self.chip.used_wired[1][self.chip.gate[pair_gate[1]][0]][self.chip.gate[pair_gate[1]][1]]
                    flag_conflict = self.chip.del_and_add(net_num, cnt)

            if flag_conflict == 0:
                cnt = cnt + 1
            else:
                return cnt

        return cnt

    def run(self, use_spfa=1):
        random.shuffle(self.chip.net)

        if not use_spfa:
            # Change the situation to the more simple algorithm - Breadth-First-Search.
            self.chip.grid_value = self.chip.memset_list(1)

        answer = self.astar_spfa()

        if not use_spfa:
            # Recover the grid_value to initial values.
            self.chip.manhattan_distance_weight()

        return answer


if __name__ == "__main__":

    env = Environment(5)
    temp = AstarSpfa(env)
    ans = temp.run()
    print(ans)
    temp.chip.plot("test for env")


