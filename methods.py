def is_valid(i, j, n, m):
    return (i >= 0 and i < m and j >= 0 and j < n)

# returns the variation of intensity values around the pixel i, j
# Vc(I(i, j)) = |I(i-1, j-1) - I(i+1, j+1)| + |I(i-1, j) - I(i+1, j)| + |I(i-1, j+1) - I(i+1, j-1)| + |I(i, j-1) - I(i, j+1)|
def Vc(img, coords):
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