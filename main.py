import math
import os
import random
import shutil
import subprocess
from glob import glob


def create_output_dirs(dst):
    if not os.path.exists(dst):
        os.mkdir(dst)
        print(f"Created output dir: {dst}\n=======================")

    if not os.path.exists(dst + f"/train"):
        os.mkdir(dst + f"/train")
    if not os.path.exists(dst + f"/test"):
        os.mkdir(dst + f"/test")
    if not os.path.exists(dst + f"/val"):
        os.mkdir(dst + f"/val")

def dir_parser(src, ext="txt"):
    '''
        Directory Parser
    :param src: Source directory path
    :param ext: File extension
    :return: None
    '''

    def walk_dirs(src):
        print(f"Parsing {src}\n-------------")

        dir_obj = next(os.walk(src))
        root = dir_obj[0]
        dirs = dir_obj[1]
        files = dir_obj[2]

        if files != []:
            for file in files:
                print(root+"_"+file)
                shutil.copy(root + f"/{file}", root+"_"+file)

        if dirs != []:
            for dir in dirs:
                print(dir)
                walk_dirs(root+"/"+dir)

    walk_dirs(src)


    # for dir_obj in os.walk(src):
        # filename = os.path.basename(filepath)
        # print(filename)
        # root = dir_obj[0]
        # dirs = dir_obj[1]
        # files = dir_obj[2]
        # files = [file for file in dir_obj[2] if not file.endswith(ext)]

        # print(root)
        # print(dirs)
        # print(files)






def shuffler(src, dst):
    '''
    Shuffle files from source directory to a new output directory
    :param src: Source directory path
    :param dst: Output directory path
    :return: None
    '''

    # Get files count
    _, _, files = next(os.walk(src))
    file_count = len(files)
    print(file_count)

    # Generate file indices
    random_indices = [i for i in range(file_count)]
    random.shuffle(random_indices)

    print(random_indices)


def splitter(src, dst, ext="txt"):
    _, _, files = next(os.walk(src))
    files = [fi for fi in files if not fi.endswith(f".{ext}")]
    file_count = len(files)

    print(file_count)
    ratio = math.floor(file_count*0.7)
    count = 0
    for filename in files:
        if count < ratio:
            shutil.copy(src+f"/{filename}", dst+f"/train/{filename}")
        else:
            shutil.copy(src+f"/{filename}", dst+f"/val/{filename}")

        count += 1

def splitter_2(src, dst, split):
    _, _, src_files = next(os.walk(src))

    exts = {'labels': '.txt', 'images': ('.jpg', '.png')}

    for key, value in exts.items():
        files = [fi for fi in src_files if fi.endswith(value)]
        file_count = len(files)

        if file_count != 0:
            ratio = math.floor(file_count * (split / 10))
            count = 0
            tr = 0
            valc = 0
            for filename in files:
                if count < ratio:
                    # print(dst + f"/{key}/train/{filename} - Dest")
                    tr += 1
                    # shutil.copy(src + f"/{filename}", dst + f"/{key}/train/{filename}")
                else:
                    # print(dst + f"/{key}/val/{filename} - Dest")
                    valc += 1
                    # shutil.copy(src + f"/{filename}", dst + f"/{key}/val/{filename}")

                count += 1
            print(f"Total {value} files = {count}\n-----------------------\nSplit {split*10}:{100-split*10}\nTrain = {tr} Val = {valc}\n")
        else:
            print(f'No file exists for extensions {value}')


def move_files(name='person', dir_type='train', labels='labels',count=8):
    dst = r"output"

    for i in range(count):
        src = fr"C:\Users\ashwi\PycharmProjects\daxplore\P3\{name}_{i+1}\{labels}\{dir_type}/"

        dir_obj = next(os.walk(src))
        root = dir_obj[0]
        files = dir_obj[2]

        for file in files:
            shutil.copy(root + f"/{file}", dst + f"/{labels}/{dir_type}/{name}_{i+1}_" + file)

    print(f"Done {labels}/{dir_type}/{name}")


if __name__ == "__main__":
    # src = r'C:\Users\ashwi\PycharmProjects\Datasets\Checkbox model\Checkbox Dataset\docs_with_checkboxes'
    src = r'C:\Users\ashwi\PycharmProjects\daxplore\data\PeekNot_V2\person'
    dst = r'C:\Users\ashwi\Desktop\checkbox'
    # create_output_dirs(dst)

    # splitter(src, dst, ext='txt')
    # splitter_2(src, dst, 5)

    # dir_parser(src)
    # move_files(name='camera', dir_type='train', labels='images', count=6)
    # move_files(name='camera', dir_type='train', labels='labels', count=6)
    # move_files(name='camera', dir_type='val', labels='images', count=6)
    # move_files(name='camera', dir_type='val', labels='labels', count=6)
    #
    # move_files(name='mobile', dir_type='train', labels='images', count=6)
    # move_files(name='mobile', dir_type='train', labels='labels', count=6)
    # move_files(name='mobile', dir_type='val', labels='images', count=6)
    # move_files(name='mobile', dir_type='val', labels='labels', count=6)
    #
    # move_files(name='person', dir_type='train', labels='images', count=8)
    # move_files(name='person', dir_type='train', labels='labels', count=8)
    # move_files(name='person', dir_type='val', labels='images', count=8)
    # move_files(name='person', dir_type='val', labels='labels', count=8)

    """
    Check missing files in images and labels dir
    """
    # src = fr"C:\Users\ashwi\PycharmProjects\daxplore\output\images\train"
    # dst = fr"C:\Users\ashwi\PycharmProjects\daxplore\output\labels\train"
    #
    # dir_obj = next(os.walk(src))
    # root = dir_obj[0]
    # files = dir_obj[2]
    # li1 = []
    # for i in files:
    #     li1.append(i[:-4])
    #
    # dir_obj2 = next(os.walk(dst))
    # root2 = dir_obj2[0]
    # files2 = dir_obj2[2]
    #
    # li2 = []
    # for i in files2:
    #     li2.append(i[:-4])
    #
    # s = set(li1)
    # temp3 = [x for x in li2 if x not in s]
    # print(temp3)
    #
    # print("Completed Dataset creation")

    """
    Auvi -> Yolo class labels
    """
    # src = r"C:\Users\ashwi\Desktop\PeekNot_v3\labels\train"
    # dst = r"C:\Users\ashwi\Desktop\PeekNot_v3_yolo\labels\train"
    #
    # classes = {'mobile': 0,
    #            'camera': 1,
    #            'person': 2,
    #            'unknown': 4
    #         }
    #
    # dir_obj = next(os.walk(src))
    # root = dir_obj[0]
    # files = dir_obj[2]
    #
    # for i in files:
    #     label = open(src+"/"+i, 'r')
    #     outfile = open(dst+"/"+i, 'w')
    #
    #     for line in label.readlines():
    #         class_name, nx, ny, nw, nh = map(str, line.split(' '))
    #         nx, ny, nw, nh = map(float, [nx, ny, nw, nh])
    #         if class_name == 'unknown':
    #             print(src+"/"+i)
    #         else:
    #             outfile.write(f"{classes[class_name]} {nx} {ny} {nw} {nh}\n")
    #
    #     outfile.close()
    #     label.close()
