import aco

folder = 'images_to_process/'
image_paths = [
    folder + 'man.jpg', # 0
    folder + 'lena.png', # 1
    folder + 'test.png' # 2
]

def main():
    aco.AS(image_paths[0])

if __name__ == '__main__':
    main()