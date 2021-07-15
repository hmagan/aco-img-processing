import numpy as np
import constants as c
import random as r
from PIL import Image, ImageEnhance
from ant import Ant
import methods as m

def run(image_path): 
    I = Image.open(image_path) # I is the image to process converted to grayscale
    contrast = ImageEnhance.Contrast(I)
    I = contrast.enhance(1.5).convert('LA')
    I.save('saved_images/test.png')

    M1 = I.width
    M2 = I.height

    T = [[c.T_init for i in range(M1)] for j in range(M2)] # pheromone matrix
    N = [[0 for i in range(M1)] for j in range(M2)] # heuristic matrix

    V_low = 9999 # arbitrarily high number
    V_high = 0

    # set up the heuristic matrix
    for i in range(M2):
        for j in range(M1):
            N[i][j] = m.Vc(I, (i, j))
            if N[i][j] < V_low: 
                V_low = N[i][j]
            if N[i][j] > V_high: 
                V_high = N[i][j]
    V_max = V_high - V_low # max intensity variation

    for i in range(M2):
        for j in range(M1):
            N[i][j] /= V_max # complete the heuristic matrix; N(i, j) = Vc(I(i, j)) / V_max
            
    K = int(np.sqrt(M1 * M2)) # K is the number of ants; K = (M1 * M2)^1/2

    ants = [Ant(r.randrange(0, M1), r.randrange(0, M2)) for i in range(K)]

    dx = [-1, -1, -1, 0, 0, 1, 1, 1]
    dy = [-1, 0, 1, -1, 1, -1, 0, 1]

    def is_valid(i, j):
        return (i >= 0 and i < M1 and j >= 0 and j < M2)

    for i in range(c.N):
        visited = [[set() for i in range(M1)] for j in range(M2)] # keep track of what ants visited each vertex
        vertices_to_update = set() # keep track of what pixels got updated so we don't have to iterate through all M1 x M2 vertices
        for j in range(c.L):
            for ant in ants: 
                x, y = 0, 0 # i, j
                OMEGA = 0 # sum of neighborhood pixels
                # check to see what method to use (randomly)
                q = r.random()
                if q <= c.q0:
                    # maximize T[x][y] * N[x][y] ** c.B
                    P = 0
                    for k in range(8): 
                        px = ant.x + dx[k]
                        py = ant.y + dy[k]
                        if is_valid(px, py) and not (px, py) in ant.recently_visited:
                            p = T[py][px] * (N[py][px] ** c.B)
                            if p > P:
                                P = p
                                x, y = px, py
                else:
                    # loop first to find omega, and then to check all neighborhood pixels
                    for k in range(8): 
                        px = ant.x + dx[k]
                        py = ant.y + dy[k]
                        if is_valid(px, py):
                            OMEGA += I.getpixel((px, py))[0]
                    poss_vertices = []
                    weights = []
                    cum_weight = []
                    for k in range(8): 
                        px = ant.x + dx[k]
                        py = ant.y + dy[k]
                        if is_valid(px, py) and not (px, py) in ant.recently_visited:
                            pheromone_value = T[py][px] ** c.A
                            heuristic_value = N[py][px] ** c.B
                            p = 0
                            if pheromone_value != 0 and heuristic_value != 0 and OMEGA != 0:
                                p = (pheromone_value * heuristic_value) / (OMEGA * pheromone_value * heuristic_value) # equation for probability
                            poss_vertices.append((px, py))
                            weights.append(p)
                            if(len(weights) == 1):
                                cum_weight.append(p)
                            else: 
                                cum_weight.append(cum_weight[-1]+p)
                            print(px, ', ', py, ' poss with a weight of ', p)
                    result = (ant.x, ant.y)
                    if len(cum_weight) > 0:
                        result = r.choices(poss_vertices, cum_weights=cum_weight, k=1)[0]
                    print('chosen: ', result)
                    x, y = result[0], result[1]
                ant.x = x
                ant.y = y
                ant.recently_visited.pop()
                ant.recently_visited.appendleft((x, y))
                T[y][x] = ((1 - c.PHI) * T[y][x]) + (c.PHI * c.T_init) # local pheromone update
                ant.total += N[y][x]
                ant.num += 1
                visited[y][x].add(ant)
                vertices_to_update.add((y, x))
        # global pheromone update
        for coords in vertices_to_update: 
            x = coords[0]
            y = coords[1]
            dT = 0 # find sum of pheromones deposited by the each ant at pixel x, y
            for ant in visited[x][y]:
                dT += ant.get_average() # returns average of heuristic information on the specific ant's tour
            T[x][y] = ((1 - c.p) * T[x][y]) + (c.p * dT)


    new_image = Image.new('RGB', (M1, M2))
    # display the pixels of the image which have a pheromone level above the threshold
    for i in range(M2): 
        for j in range(M1): 
            print(i, ', ', j)
            if T[i][j] >= c.threshold:
                new_image.putpixel((j, i), (0, 0, 0))
            else: 
                new_image.putpixel((j, i), (255, 255, 255))

    # new_image.save('saved_images/test.png')
    new_image.show()