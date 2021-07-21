import aco

folder = 'images_to_process/'
image_paths = [
    folder + 'man.jpg', # 0
    folder + 'lena.png', # 1
    folder + 'camera.jpg', # 2
]

def main(): 
    aco.AS(image_paths[1])

if __name__ == '__main__':
    main()