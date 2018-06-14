import numpy as np
import os
import six.moves.urllib as urllib
import sys
import tarfile
import tensorflow as tf
import zipfile
import pandas as pd 
from collections import defaultdict
from io import StringIO
from matplotlib import pyplot as plt
from PIL import Image
import csv
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util
import moviepy
from moviepy.editor import VideoFileClip
from moviepy.editor import concatenate_videoclips
import moviepy.editor as mpy
from skimage.draw import polygon_perimeter, polygon
#import imageio
#imageio.plugins.ffmpeg.download()

def boxOutput(modelName, training_dir):
    # What model to download.
    MODEL_NAME = str(modelName)

    # Path to frozen detection graph. This is the actual model that is used for the object detection.
    PATH_TO_CKPT = MODEL_NAME + '/frozen_inference_graph.pb'
    # List of the strings that is used to add correct label for each box.
    PATH_TO_LABELS = os.path.join(str(training_dir), 'monkey_label_map.pbtxt')
    NUM_CLASSES = 1
    detection_graph = tf.Graph()

    with detection_graph.as_default():
        od_graph_def = tf.GraphDef()
        with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
            serialized_graph = fid.read()
            od_graph_def.ParseFromString(serialized_graph)
            tf.import_graph_def(od_graph_def, name='')
    label_map = label_map_util.load_labelmap(PATH_TO_LABELS)
    categories = label_map_util.convert_label_map_to_categories(label_map, max_num_classes=NUM_CLASSES, use_display_name=True)
    category_index = label_map_util.create_category_index(categories)
    return([detection_graph,category_index])

def detection(movie_file, num_images, output_inf_graph_pth, training_dir):
    # Size, in inches, of the output images.
    IMAGE_SIZE = (12, 8)
    boxOutput_outs = boxOutput(output_inf_graph_pth, training_dir)
    detection_graph = boxOutput_outs[0]
    category_index = boxOutput_outs[1]
    coordinate_list = []
    with detection_graph.as_default():
        with tf.Session(graph=detection_graph) as sess:
            # Definite input and output Tensors for detection_graph
            image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
            # Each box represents a part of the image where a particular object was detected.
            detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
            # Each score represent how level of confidence for each of the objects.
            # Score is shown on the result image, together with the class label.
            detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
            detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
            num_detections = detection_graph.get_tensor_by_name('num_detections:0')
            #mov = VideoFileClip(movie_file,audio=False) #need to input movie file
            mov = movie_file
            selected_frame_times = np.arange(0,mov.duration, mov.duration/num_images) #need to input num_images
            for frame_time in selected_frame_times:
                #print(frame_time)
                this_frame = mov.get_frame(frame_time)
                # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
                image_np_expanded = np.expand_dims(this_frame, axis=0)
                # Actual detection.
                (boxes, scores, classes, num) = sess.run(
                    [detection_boxes, detection_scores, detection_classes, num_detections],
                    feed_dict={image_tensor: image_np_expanded})
                #mov = mpy.VideoFileClip(movie_file, audio=False)
                mov = movie_file
                width, height = mov.size
                coordinate_list_for_frame = []
                for i, box in enumerate(np.squeeze(boxes)):
                    if(np.squeeze(scores)[i] > 0.5):
                        ymin = box[0]*height
                        xmin = box[1]*width
                        ymax = box[2]*height
                        xmax = box[3]*width
                        coords = [ymin,xmin,ymax,xmax]
                        coordinate_list_for_frame.append(coords)
                coordinate_list.append(coordinate_list_for_frame)
    return(coordinate_list)

## requires:
## movie_file:  path to a movie file
## selected_frames: a list of times for which there are coordiantes.
## coordinate_list: a list of coordinates: [[x,y, x2,y2], [[xx,yy, xx2,yx2], [...], etc. ]

def write_out_movie( movie_file, selected_frame_times, coordinate_list, out_filename): #='human_intruder.mp4' ): 
    # load movie_file
    #mov = mpy.VideoFileClip(movie_file, audio=False)
    mov = movie_file
    # get width and height
    w,h = mov.size

    def get_coords(t, selected_frame_times, coordinate_list ):
        """A function that returns the coordinates for the nearest frame..."""
        # find nearest selected_frame_time
        frame_time =min(selected_frame_times, key=lambda x:abs(x-t))
        # grab the coordinate that corresponds to that time

        ##### THIS LINE IS AN ERROR AND MUST RETURN A LIST OF COORDINATES!!!
        this_frame = [i for i, x in enumerate(selected_frame_times) if x == frame_time][0]
        coords = []
        coords = coordinate_list[this_frame]
        return coords

    def make_boxes_mask(t):
        """Returns a mask image of the frame for time t, with .75 everywhere except the box."""
        # get coordinates
        coords_list_for_frame = get_coords(t, selected_frame_times, coordinate_list )
        # initialize mask
        alpha = np.ones((h,w))*.75

        print( len( coords_list_for_frame ))
        i = 0 
        for coords in coords_list_for_frame:
            print( i, coords )
            i = i+1
            # fill in a polygon defined by coordinates. 
            rr, cc = polygon(r=(coords[0], coords[2], coords[2], coords[0]), 
                     c=(coords[1], coords[1], coords[3], coords[3]), shape=alpha.shape)
            alpha[rr, cc] = 1.00
        return alpha

    def make_boxes_outline_mask(t):
        """Returns a mask image of the frame for time t, for the perimeter of the box."""
        # get coordinates
        coords_list_for_frame = get_coords(t, selected_frame_times, coordinate_list )
        # initialize mask
        alpha = np.zeros((h,w))
        for coords in coords_list_for_frame:
            # fill in a polygon-perimeter defined by coordinates. 
            rr, cc = polygon_perimeter(r=(coords[0], coords[2], coords[2], coords[0]), 
                c=(coords[1], coords[1], coords[3], coords[3]), shape=alpha.shape)
            alpha[rr, cc] = 1.0
        return alpha
        
    # create a red image
    red_image = np.dstack( (np.ones((h,w))*255,np.ones((h,w)),np.ones((h,w))) )
    # turn red-image into a movie clip. 
    red = mpy.ImageClip(red_image).set_duration(mov.duration).add_mask()
    # mask the red movie with the function outlined above. 
    red.mask.get_frame = lambda t: make_boxes_outline_mask(t)
   
    # add a mask to the movie we read in
    mov = mov.add_mask()
    # apply a semi-transparent mask to the movie, so that the face pops out. 
    mov.mask.get_frame = lambda t: make_boxes_mask(t)

    # create a composite video of the movie and the red box, both with masks applied. 
    video = mpy.CompositeVideoClip([mov, red])
    
    # write out the file. #FIX THIS!!!!!!
    video.write_videofile(out_filename, fps=25, codec='libx264' )
    clips = VideoFileClip(out_filename)
    return(clips)

def main():
    output_inf_graph_pth = '../output_inference_graphs/monkey_inference_graph'
    training_dir = '../data' #path to labelmap
    movie_file = '../movies/human_intruder.mov'
    num_images = 240
    # load movie_file
    mov = mpy.VideoFileClip(movie_file, audio=False)
    prev_t = 0
    frames = []
    new_clips = []
    coordinate_list_frames = []
    coordinate_list = []
    selected_frame_times_frames = []
    selected_frame_times = []
    out_filenames = []
    clip_array = []
    for indx,t in enumerate(range(60,int(mov.duration),60)):
        print(indx,prev_t,t)
        frames = mov.subclip(prev_t,t)
        new_clips.append(frames)
        coordinate_list_frames = detection(new_clips[indx], num_images, output_inf_graph_pth, training_dir) #returns a list of coordinates
        coordinate_list.append(coordinate_list_frames)
        selected_frame_times_frames = np.arange(0,new_clips[indx].duration, new_clips[indx].duration/num_images)
        selected_frame_times.append(selected_frame_times_frames)
        out_filenames.append('human_intruders{}.mp4'.format(indx))
        out_clips = write_out_movie( new_clips[indx], selected_frame_times[indx], coordinate_list[indx], out_filenames[indx] )
        clip_array.append(out_clips)
        prev_t = t
    
    #print(clip_array)
    final_clip = concatenate_videoclips(clip_array)
    final_clip.write_videofile("my_concatenation.mp4")


main()
