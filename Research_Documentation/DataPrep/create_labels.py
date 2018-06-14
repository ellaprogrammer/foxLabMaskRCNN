import os
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
#%matplotlib inline

from glob import glob
import matplotlib.image as mpimg
import matplotlib.patches as patches
from os import listdir
from os.path import isfile, join

def create_df(roi_file):
    heights = []
    widths = []
    file_names = []
    xmins = [] # List of normalized left x coordinates in bounding box (1 per box)
    xmaxs = [] # List of normalized right x coordinates in bounding box
    # (1 per box)
    ymins = [] # List of normalized top y coordinates in bounding box (1 per box)
    ymaxs = [] # List of normalized bottom y coordinates in bounding box
    # (1 per box)
    
    #for roi_file in roi_files:
    image_file = roi_file[:-4]+'.png'
    img = mpimg.imread(image_file)
    ##heights.append(img.shape[0]) # Image height
    ##widths.append(img.shape[1]) # Image width
    ##file_names.append((os.path.basename(roi_file)).strip('.csv'))
    ##classes = ['monkey_face' for x in file_names]
    
    with open(roi_file) as fp:
        roi_list = [x.strip().split(',') for x in fp.readlines()] #getting coordinates, xmin,ymin,xmax,ymax
    classes = ['monkey_face' for x in roi_list]
    for roi in roi_list:
        heights.append(img.shape[0]) # Image height
        widths.append(img.shape[1]) # Image width
        file_names.append((os.path.basename(roi_file)).strip('.csv'))
        coords = [float(coord) for coord in roi]
        xmins.append(coords[0])
        xmaxs.append(coords[2])
        ymins.append(coords[1])
        ymaxs.append(coords[3])
    
    df = pd.DataFrame(
    {'filename': file_names,
    'width': widths,
    'height': heights,
    'class': classes,
    'xmin': xmins,
    'ymin': ymins,
    'xmax': xmaxs,
    'ymax': ymaxs
    })

    return(df)

def data_frame(FOLDER_LOCATION):
    dataframes = []
    roi_files = glob(FOLDER_LOCATION + '/*.csv')
    for roi_file in roi_files:
        dataframes.append(create_df(roi_file))
    df = pd.concat(dataframes)
    df = df[['filename', 'width', 'height', 'class', 'xmin', 'ymin', 'xmax', 'ymax']]
    return(df)

def main():
    #path = '/Users/rurikoimai/Desktop/monkey_images/testing/'
    for directory in ['training', 'testing']:
        image_path = os.path.join(os.getcwd(), 'images/{}'.format(directory))
        data_labels = data_frame(image_path)
        data_labels.to_csv('data/{}_labels_test.csv'.format(directory), index=None)
        print('Successfully made test/train lables')
main()



