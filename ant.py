from collections import deque
import constants as c

class Ant:
    x = 0
    y = 0
    # total = 0 # sum of heuristics on current tour
    # num = 0 # total number of pixels visited
    # recently_visited = deque((-1, -1) * c.mem, c.mem) # each ant remembers recently visited vertices as not to get stuck in a loop

    def __init__(self, i, j):
        self.x = i
        self.y = j

    # def get_average(self):
    #     return self.total / self.num