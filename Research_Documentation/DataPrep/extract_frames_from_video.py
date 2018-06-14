import moviepy.editor as moviepy
import numpy as np
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt
from glob import glob

input_folder = '/Users/rurikoimai/Desktop/genomecenter_Upload/frames/movies/'
output_dir = '/Users/rurikoimai/Desktop/genomecenter_Upload/frames/frames/'
#movie_extension = '.mov'
num_images = 10

movie_files = glob(input_folder+'/*.mov')#+movie_extension)
#print(movie_files)

for movie_file in movie_files:
    movie_root = movie_file.split('/')[-1][:-4]
#    print(movie_root)
    mov = moviepy.VideoFileClip(movie_file, audio=False)
    w,h = mov.size
#    print(w,h) 
    selected_frames = np.random.uniform(0, mov.duration, num_images)
#    print("selected_frames")
    selected_frames = np.around(selected_frames,2)
#    print("selected_frames2") #prints till here
    f, ax = plt.subplots(1,1,figsize=(10,10.0/w*h))
    for i,each_frame in enumerate(selected_frames):
        m = mov.get_frame(each_frame)
        ax.imshow(m)
        ax.axes.get_xaxis().set_visible(False)
        ax.axes.get_yaxis().set_visible(False)
        plt.tight_layout()
        f.savefig(output_dir+movie_root+'_'+str(each_frame).replace('.','_')+'.png', bbox_inches='tight', pad_inches=0)

