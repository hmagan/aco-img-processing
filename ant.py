from collections import deque
import constants as c

class Ant:
    x = 0
    y = 0
    recently_visited = deque((-1, -1) for i in range(c.mem)) # each ant remembers recently visited vertices as not to get stuck in a loop

    def __init__(self, i, j):
        self.x = i
        self.y = j

    def add_vertex(self, coords): 
        self.recently_visited.appendleft(coords)
        self.recently_visited.pop()