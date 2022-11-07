import math
import os
import random
import shutil
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

    for dir_obj in os.walk(src):
        # filename = os.path.basename(filepath)
        # print(filename)
        root = dir_obj[0]
        dirs = dir_obj[1]
        files = [file for file in dir_obj[2] if not file.endswith(('.txt', '.tar'))]
        print(root)
        print(dirs)
        print(files)


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


if __name__ == "__main__":
    src = r'C:\Users\ashwi\PycharmProjects\Datasets\Checkbox model\Checkbox Dataset\docs_with_checkboxes'
    dst = r'C:\Users\ashwi\Desktop\checkbox'
    # create_output_dirs(dst)

    # splitter(src, dst, ext='txt')

    dir_parser(src)

