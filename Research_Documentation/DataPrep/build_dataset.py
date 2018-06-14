# Split dataset into train, test, validation sets randomly.
# 80% train, 10% test, 10% val

import glob as glob
import numpy as np
import os
import random

def get_csv(image_path):                                                 
    img_files = glob.glob(image_path + '/*csv')
    filenames = [os.path.basename(img_file) for img_file in img_files]
    filenames.sort()
    random.seed(230)
    random.shuffle(filenames) # randomly shuffles the ordering of filenames

    split1 = int(0.8 * len(filenames))
    split2 = int(0.9 * len(filenames))
    train_filenames = filenames[:split1]
    test_filenames = filenames[split1:split2]
    val_filenames = filenames[split2:]

    return(train_filenames, test_filenames, val_filenames)

def get_png(image_path):
    img_files = glob.glob(image_path + '/*png') # full image paths
    filenames = [os.path.basename(img_file) for img_file in img_files] # image file names filename.png
    
    split_data = get_csv(image_path)
    train = split_data[0]
    test = split_data[1]
    val = split_data[2]
    
    for filename in filenames:
        #print(filename)
        for file in train:
            #print(file)
            base_name = file[:-4]
            #print(base_name)
            if base_name == filename[:-4]:
                #break
                os.rename(os.path.join(image_path + filename), os.path.join(image_path, "train/", filename))
        for file in test:
            base_name = file[:-4]
            if base_name == filename[:-4]:
                os.rename(os.path.join(image_path + filename), os.path.join(image_path, "test/", filename))
        for file in val:
            base_name = file[:-4]
            if base_name == filename[:-4]:
                os.rename(os.path.join(image_path + filename), os.path.join(image_path, "val/", filename))


def main():
    image_path = '/Users/rurikoimai/Desktop/Mask/Mask_RCNN/samples/monkey/dataset/'
    split_data = get_csv(image_path)
    get_png(image_path)    
    train_csv = split_data[0]
    test_csv = split_data[1]
    val_csv = split_data[2]
    
    [os.rename(image_path + file, os.path.join(image_path, "train/", file)) for file in train_csv]
    [os.rename(image_path + file, os.path.join(image_path, "test/", file)) for file in test_csv]
    [os.rename(image_path + file, os.path.join(image_path, "val/", file)) for file in val_csv]

main()    
