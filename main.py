import aco

folder = 'images_to_process/'
image_paths = [
    folder + 'man.jpg', # 0
    folder + 'lena.png', # 1
    folder + 'test.png', # 2
    folder + 'borgir.jpg', # 3
    folder + 'r2d2.jpg', # 4
    folder + 'camera.jpg', # 5
    folder + 'camera_n.jpg' # 6
]

def main(): 
    aco.AS(image_paths[5])

if __name__ == '__main__':
    main()