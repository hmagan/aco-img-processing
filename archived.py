# This file is purely to store old code while I decide my methodology
# i.e. AS vs ACS

# V_low = 9999 # arbitrarily high number
# V_high = 0

# # set up the heuristic matrix
# for i in range(M2):
#   for j in range(M1):
#       N[i][j] = m.Vc(I, (i, j))
#       if N[i][j] < V_low: 
#           V_low = N[i][j]
#       if N[i][j] > V_high: 
#           V_high = N[i][j]
# V_max = V_high - V_low # max intensity variation

# for i in range(M2):
#   for j in range(M1):
#       N[i][j] /= V_max # complete the heuristic matrix; N(i, j) = Vc(I(i, j)) / V_max

#      for i in range(c.N):
#         visited = [[set() for i in range(M1)] for j in range(M2)] # keep track of what ants visited each vertex
#         vertices_to_update = set() # keep track of what pixels got updated so we don't have to iterate through all M1 x M2 vertices
#         for j in range(c.L):
#             for ant in ants: 
#                 x, y = 0, 0 # i, j
#                 OMEGA = 0 # sum of neighborhood pixels
#                 # check to see what method to use (randomly)
#                 q = r.random()
#                 if q <= c.q0:
#                     # maximize T[x][y] * N[x][y] ** c.B
#                     P = 0
#                     for k in range(8): 
#                         px = ant.x + dx[k]
#                         py = ant.y + dy[k]
#                         if is_valid(px, py) and not (px, py) in ant.recently_visited:
#                             p = T[py][px] * (N[py][px] ** c.B)
#                             if p > P:
#                                 P = p
#                                 x, y = px, py
#                 else:
#                     # loop first to find omega, and then to check all neighborhood pixels
#                     for k in range(8): 
#                         px = ant.x + dx[k]
#                         py = ant.y + dy[k]
#                         if is_valid(px, py):
#                             OMEGA += I.getpixel((px, py))[0]
#                     poss_vertices = []
#                     weights = []
#                     cum_weight = []
#                     for k in range(8): 
#                         px = ant.x + dx[k]
#                         py = ant.y + dy[k]
#                         if is_valid(px, py) and not (px, py) in ant.recently_visited:
#                             pheromone_value = T[py][px] ** c.A
#                             heuristic_value = N[py][px] ** c.B
#                             p = 0
#                             if pheromone_value != 0 and heuristic_value != 0 and OMEGA != 0:
#                                 p = (pheromone_value * heuristic_value) / (OMEGA * pheromone_value * heuristic_value) # equation for probability
#                             poss_vertices.append((px, py))
#                             weights.append(p)
#                             if(len(weights) == 1):
#                                 cum_weight.append(p)
#                             else: 
#                                 cum_weight.append(cum_weight[-1]+p)
#                             # print(px, ', ', py, ' poss with a weight of ', p)
#                     result = (ant.x, ant.y)
#                     if len(cum_weight) > 0:
#                         result = r.choices(poss_vertices, cum_weights=cum_weight, k=1)[0]
#                     # print('chosen: ', result)
#                     x, y = result[0], result[1]
#                 ant.x = x
#                 ant.y = y
#                 ant.recently_visited.pop()
#                 ant.recently_visited.appendleft((x, y))
#                 T[y][x] = ((1 - c.PHI) * T[y][x]) + (c.PHI * c.T_init) # local pheromone update
#                 ant.total += N[y][x]
#                 ant.num += 1
#                 visited[y][x].add(ant)
#                 vertices_to_update.add((y, x))
#         # global pheromone update
#         for coords in vertices_to_update: 
#             x = coords[0]
#             y = coords[1]
#             dT = 0 # find sum of pheromones deposited by the each ant at pixel x, y
#             for ant in visited[x][y]:
#                 dT += ant.get_average() # returns average of heuristic information on the specific ant's tour
#             T[x][y] = ((1 - c.p) * T[x][y]) + (c.p * dT)