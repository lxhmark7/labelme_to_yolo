#-*- coding: utf-8 -*-

'''
将使用labelme标注的数据集转换为yolo格式；

labelme的文件如下：
    JPEGImages: 存放原始的图片
    Annotations: 存放labelme标注的json文件

生成新的目录 images(图片) 和 labels(标签)
    images: 
        train
        val
    labels：
        train
        val
'''
import os
import json
import random
import shutil
import numpy as np
from pathlib import Path


def convert(size, box):
    ''' 
        size: picture size --> [width, height]
        box: rectangle location --> 
        convert box [x1, y1, x2, y2] --> [x_center, y_center, w, h] --Range:[0,1]
    '''
    # labelme 标注的box,有时是左上角-右下角，有时是右下角-左上角
    dw = 1. / size[0]
    dh = 1. / size[1]
    x_center = (box[0] + box[2]) / 2.0 * dw
    y_center = (box[1] + box[3]) / 2.0 * dh
    w = np.abs(box[2] - box[0]) * dw
    h = np.abs(box[3] - box[1]) * dh
    return x_center, y_center, w, h


def json_to_txt(img_stem, label_json, label_flag, class_to_id):
    '''
        img_stem: img stem
        label_json: labelme label json file 
        label_flag: 'train' or 'val'
        class_to_id: {'A': 0, 'B': 1}
        Convert json file to txt file
    '''
    file = open(label_json, 'r')
    save_txt = open(f'labels/{label_flag}/{img_stem}.txt', 'w')
    json_file = json.load(file)
    img_width = json_file['imageWidth']
    img_height = json_file['imageHeight']
    
    # iter every object
    for obj in json_file['shapes']:
        class_id = class_to_id[obj['label']]
        (x1, y1), (x2, y2) = obj['points']
        # Convert labelme rectangle format to yolo format(x_center, y_center, w, h), yolo range-[0, 1]
        x_center, y_center, w, h = convert([img_width, img_height], (x1, y1, x2, y2))
        save_txt.write(' '.join(map(str, [class_id, x_center, y_center, w, h])))
        save_txt.write('\n')
    save_txt.close()
    file.close()


def main(JPEGImages, Annotations, classes, train_percentage):
    # {'A': 0, 'B': 1, 'C': 2, 'D': 3}
    class_to_id = dict(zip(classes, range(len(classes))))

    img_list = [img.name for img in Path(JPEGImages).iterdir() if img.is_file()]
    random.shuffle(img_list)
    train_num = int(train_percentage * len(img_list))

    # Create train and val directory
    for i in ['images', 'labels']:
        for j in ['train', 'val']:
            dir = Path(f'{i}/{j}')
            if dir.exists():
                shutil.rmtree(dir)
            dir.mkdir(parents=True, exist_ok=True)

    for i, img in enumerate(img_list):
        label_json = f"{Annotations}/{Path(img).stem}.json"
        img_stem = Path(img).stem
        if i < train_num:
            label_flag = 'train'
            # Copy picture
            shutil.copy(f'{JPEGImages}/{img}', f'images/{label_flag}')
            # Convert json to txt
            json_to_txt(img_stem, label_json, label_flag, class_to_id)
        else:
            # validation
            label_flag = 'val'
            # Copy picture
            shutil.copy(f'{JPEGImages}/{img}', f'images/{label_flag}')
            # Convert json to txt
            json_to_txt(img_stem, label_json, label_flag, class_to_id)
    print(f"Train set num: {train_num}, validation set num: {len(img_list) - train_num}")


if __name__ == '__main__':
    # Images directory
    JPEGImages = 'JPEGImages'
    # Labelme generate json file directory
    Annotations = 'Annotations'
    # class name list
    classes = ['A', 'B', 'C', 'D']   
    # Train percentage
    train_percentage = 0.6

    main(JPEGImages, Annotations, classes, train_percentage)


