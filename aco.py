import numpy as np
import constants as c
import random as r
import operator
import copy
from PIL import Image, ImageEnhance
from ant import Ant

def is_valid(i, j, n, m):
    return (i >= 0 and i < m and j >= 0 and j < n)

# returns the variation of intensity values around the pixel i, j
# V(I(i, j)) = |I(i-1, j-1) - I(i+1, j+1)| + |I(i-1, j) - I(i+1, j)| + |I(i-1, j+1) - I(i+1, j-1)| + |I(i, j-1) - I(i, j+1)|
# maybe tweak with f(.)
def V(img, coords):
    i = coords[0]
    j = coords[1]
    dx = [[-1, 1], [-1, 1], [-1, 1], [0, 0]]
    dy = [[-1, 1], [0, 0], [1, -1], [-1, 1]]
    total = 0
    for k in range(4):
        i1 = i + dx[k][0]
        i2 = i + dx[k][1]
        j1 = j + dy[k][0]
        j2 = j + dy[k][1]
        if is_valid(i1, j1, img.width, img.height) and is_valid(i2, j2, img.width, img.height):
            # print(i1, ', ', j1, '  ', i2, ', ', j2)
            total += abs(img.getpixel((j1, i1))[0] - img.getpixel((j2, i2))[0])
    return total

# ant system; corresponds to methods developed by Dorigo et al., with a few tweaks made specifically for edge detection
def AS(image_path): 
    I = Image.open(image_path).convert('LA') # I is the image to process converted to grayscale
    M1 = I.width
    M2 = I.height

    # find contrast factor
    I_copy = copy.deepcopy(I)
    contrast = ImageEnhance.Contrast(I)
    c_factor = 1.0
    last_intensities = [-1.0] * M1
    variation = True
    mid = int(M2 / 2)
    while(variation):
        c_factor += 1.0
        I_copy = contrast.enhance(c_factor)
        variation = False
        for i in range(M1): 
            if I_copy.getpixel((i, mid)) != last_intensities[i]: 
                variation = True
            last_intensities[i] = I_copy.getpixel((i, mid))
    # print('contrast factor: ', c_factor - 2.0)
    # I = contrast.enhance(c_factor - 2.0)
    # I.show()
    name = image_path.split('/')[1].split('.')[0]
    I.save('saved_images/' + name + '1.png')

    T = [[c.T_init for i in range(M1)] for j in range(M2)] # pheromone matrix
    N = [[0 for i in range(M1)] for j in range(M2)] # heuristic matrix

    # set up the heuristic matrix
    Z = 0.0 # normalization factor
    for i in range(M2):
        for j in range(M1):
            N[i][j] = V(I, (i, j))
            if N[i][j] == 0:
                N[i][j] += 0.00001
            Z += N[i][j]
          
    N_sorted = [] # construct sorted 1D array of N for ant placement
    for i in range(M2):
        for j in range(M1):
            N[i][j] /= Z # complete the heuristic matrix; N(i, j) = Vc(I(i, j)) / Z
            N_sorted.append((N[i][j], j, i))

    N_sorted.sort(reverse=True, key=operator.itemgetter(0))
    print(N_sorted[0], 'vs', N_sorted[-1])
    ants = []
            
    K = int(np.sqrt(M1 * M2))
    idx = 0
    while idx < K: 
        ants.append(Ant(N_sorted[idx][1], N_sorted[idx][2]))
        idx += 1

    # K = M1 * M2
    # for i in range(M2):
    #     for j in range(M1):
    #         ants.append(Ant(i, j))

    dx = [-1, -1, -1, 0, 0, 1, 1, 1]
    dy = [-1, 0, 1, -1, 1, -1, 0, 1]

    for i in range(c.N):
        # for each ant, calculate P for each pixel in the 8-connected neighborhood and choose a random one according to P
        for ant in ants: 
            P_list = []
            edges = []
            denom = 0.0 # normalizer
            for j in range(8): # 8 because 8-connected neighborhood
                x, y = ant.x + dx[j], ant.y + dy[j]
                if not (x, y) in ant.recently_visited and is_valid(y, x, M1, M2):
                    num = (T[y][x] ** c.A) * (N[y][x] ** c.B)
                    # print((T[ant.y][ant.x] ** c.A), ' x ', (N[ant.y][ant.x] ** c.B))
                    P_list.append(num)
                    edges.append((x, y))
                    denom += num
            for j in range(len(P_list)): # 8 because 8-connected neighborhood
                P_list[j] /= denom
            if(len(edges) > 0):  
                edge = r.choices(edges, weights=P_list, k=1)[0]
                x, y = edge[0], edge[1]
                T[y][x] = (1 - c.p) * T[y][x] + c.p * N[y][x]
                ant.add_vertex((x, y))
        # global pheromone update 
        for j in range(M2): 
            for k in range(M1): 
                T[j][k] = (1 - c.PHI) * T[j][k] + c.PHI * c.T_init

    threshold = sum(T[mid]) / len(T[mid]) # guesstimate of the threshold of which the Otsu technique is based
    print(threshold)
    last_t = 1
    G1 = []
    G2 = []
    for i in range(M2): 
        for j in range(M1): 
            if T[i][j] >= threshold: 
                G1.append((T[i][j], i, j))
            else: 
                G2.append((T[i][j], i, j))
    s1 = sum(num[0] for num in G1)
    l1 = len(G1)
    s2 = sum(num[0] for num in G2)
    l2 = len(G2)
    mu1 = s1 / l1
    mu2 = s2 / l2
    last_t = threshold
    threshold = (mu1 + mu2) / 2
    G1.sort(key=operator.itemgetter(0))
    G2.sort(key=operator.itemgetter(0))
    # iteratively calculate the threshold using the equation T = (mu1 + mu2) / 2
    while abs(last_t - threshold) > c.epsilon: 
        while G2[-1] > threshold: 
            s1 += G2[-1][0]
            l1 += 1
            s2 -= G2[-1][0]
            l2 -= 1
            G1.insert(G2.pop(), 0)
        mu1 = s1 / l1
        mu2 = s2 / l2
        last_t = threshold
        threshold = (mu1 + mu2) / 2
    print('t:', threshold)

    new_image = Image.new('RGB', (M1, M2))
    # display the pixels of the image which have a pheromone level above the calculated threshold
    for px in G1: 
        new_image.putpixel((px[2], px[1]), (0, 0, 0))
    print(len(G1), 'good ones')
    for px in G2: 
        new_image.putpixel((px[2], px[1]), (255, 255, 255))

    new_image.save('saved_images/' + name + '_e2.png')
    new_image.show()