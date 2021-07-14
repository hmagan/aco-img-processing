import numpy as np
import scipy as smp
import constants as c
from PIL import Image
import methods as m

I = Image.open('images_to_process/man.jpg').convert('LA') # I is the image to process converted to grayscale

M1 = I.height 
M2 = I.width

T = [[0 for i in range(M2)] for j in range(M1)] # pheromone matrix
N = [[0 for i in range(M2)] for j in range(M1)] # heuristic matrix

V_low = 9999 # arbitrarily high number
V_high = 0

# set up the heuristic matrix
for i in range(M1):
    for j in range(M2):
        N[i][j] = m.Vc(I, (i, j))
        # print('N[', i, ', ', j, '] = ', N[i][j])
        if N[i][j] < V_low: 
            V_low = N[i][j]
        if N[i][j] > V_high: 
            V_high = N[i][j]
V_max = V_high - V_low # max intensity variation

for i in range(M1):
    for j in range(M2):
        N[i][j] /= V_max # complete the heuristic matrix; N(i, j) = Vc(I(i, j)) / V_max
        
K = int(np.sqrt(M1 * M2)) # K is the number of ants; K = (M1 * M2)^1/2

# I.save('saved_images/test.png')
I.show()