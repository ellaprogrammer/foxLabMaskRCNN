#Change Monkey annotation format to JSON


from glob import glob
import matplotlib.image as mpimg
import matplotlib.patches as patches
from os import listdir
from os.path import isfile, join
import os
import sys
import json

def toJSON(image_path):
    
    dic = [] 
    diction = {}

    roi_files = glob(image_path + '/*.csv')

    for roi_file in roi_files:
        with open(roi_file) as fp:
            roi_list = [x.strip().split(',') for x in fp.readlines()] #getting coordinates, xmin,ymin,xmax,ymax
        image_file = roi_file[:-4]+'.png'

        file_name = os.path.basename(roi_file)[:-4]+'.png' #file_name
        img_bytes = os.stat(image_file) #image_size in bytes
        image_id = str(file_name) + str(img_bytes.st_size) #file_name + image_bytes
        REGION = {}
        for i in range(len(roi_list)):
            dic = {str(i):
                   {"shape_attributes":
                    {"name":"polygon","all_points_x":[int(float(roi_list[i][0])),int(float(roi_list[i][0])),int(float(roi_list[i][2])),int(float(roi_list[i][2]))],"all_points_y":[int(float(roi_list[i][1])),int(float(roi_list[i][3])),int(float(roi_list[i][3])),int(float(roi_list[i][1]))]},#,"height": height,"width": width},
                    "region_attributes":{"name":"monkey"}
                   }
                  }
            extra = dict(dic)
            REGION.update(extra)
        KEY = image_id
        VALUES2 = dict(fileref="", size=img_bytes.st_size, filename=file_name, base64_img_data="", file_attributes={}, regions=REGION)
        diction[KEY] = VALUES2

    #outfile = image_path + 'via_region_data.json'
    with open(os.path.join(image_path + 'via_region_data.json'), 'w') as outfile:
        json.dump(diction, outfile)


def main():
    # annnotations will go in train and val directory but can change val -> train if val is used to validate
    for image_dir in ['train', 'val']:
        image_path = os.path.join(os.getcwd(), 'dataset/{}/'.format(image_dir))
        toJSON(image_path)
        
main()
