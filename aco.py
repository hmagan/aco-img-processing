import constants as c
import random as r
import operator
from PIL import Image, ImageEnhance
from ant import Ant

def is_valid(i, j, n, m):
    return (i >= 0 and i < m and j >= 0 and j < n)

# returns the variation of intensity values around the pixel i, j
# V(I(i, j)) = |I(i-1, j-1) - I(i+1, j+1)| + |I(i-1, j) - I(i+1, j)| + |I(i-1, j+1) - I(i+1, j-1)| + |I(i, j-1) - I(i, j+1)|
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
            total += abs(img.getpixel((j1, i1))[0] - img.getpixel((j2, i2))[0])
    return total

# ant system; corresponds to methods developed by Dorigo et al., with a few tweaks made specifically for edge detection
def AS(image_path): 
    I = Image.open(image_path).convert('LA')
    M1 = I.width
    M2 = I.height

    contrast = ImageEnhance.Contrast(I)
    I = contrast.enhance(c.C)

    name = image_path.split('/')[1].split('.')[0]
    # I.save('saved_images/' + name + '1.png')

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
          
    for i in range(M2):
        for j in range(M1):
            N[i][j] /= Z # complete the heuristic matrix; N(i, j) = Vc(I(i, j)) / Z
            
    K = M1 * M2 # K is the number of ants; place one at each vertex; other method is randomly distributed & K = (M1 * M2)^1/2
    ants = []
    for i in range(M2):
        for j in range(M1):
            ants.append(Ant(i, j))

    dx = [-1, -1, -1, 0, 0, 1, 1, 1]
    dy = [-1, 0, 1, -1, 1, -1, 0, 1]

    for i in range(c.N):
        for j in range(c.L): 
            # for each ant, calculate P for each pixel in the 8-connected neighborhood and choose a random one according to P
            for ant in ants: 
                P_list = []
                edges = []
                denom = 0.0 # normalizer
                for k in range(8): # 8 because 8-connected neighborhood
                    x, y = ant.x + dx[k], ant.y + dy[k]
                    if is_valid(y, x, M1, M2):
                        num = (T[y][x] ** c.A) * (N[y][x] ** c.B)
                        P_list.append(num)
                        edges.append((x, y))
                        denom += num
                for k in range(len(P_list)): # 8 because 8-connected neighborhood
                    P_list[k] /= denom
                if(len(edges) > 0):  
                    edge = r.choices(edges, weights=P_list, k=1)[0]
                    x, y = edge[0], edge[1]
                    T[y][x] = (1 - c.p) * T[y][x] + c.p * N[y][x]
        # global pheromone update 
        for j in range(M2): 
            for k in range(M1): 
                T[j][k] = (1 - c.PSI) * T[j][k] + c.PSI * c.T_init

    new_image = Image.new('RGB', (M1, M2))
   
    sorted_T = []
    for i in range(M2): 
        for j in range(M1): 
            sorted_T.append((T[i][j], i, j))

    sorted_T.sort(reverse=True, key=operator.itemgetter(0))
    for i in range(M1 * M2): 
        if i <= (M1 * M2 * c.Tp): 
            new_image.putpixel((sorted_T[i][2], sorted_T[i][1]), (0, 0, 0))
        else: 
            new_image.putpixel((sorted_T[i][2], sorted_T[i][1]), (255, 255, 255))

    new_image.save('saved_images/lena_aco.png')
    new_image.show()