# Data Preparation


Function of these files will be breifly described below.

1. extract_frames_from_video.py
2. face_select.py
3. build_dataset.py
4. data_to_JSON.py
   create_labels.py
5. generate_tfrecord.py




In order to prepare a dataset to run in the object detection framework, we need
a correct format for the data. Here, the provided data is a video. We will collect frames from the video to create a dataset. 

The file, extract_frames_from_video.py, will extract frames from the videos.
	Set input_folder and output_dir to the approprate directories.
	To run script: 
		python extract_frames_from_video.py

The file, face_select.py, annotates the pictures, outputs the true values of the object detection in a csv format.
	To run script:
		pythonw face_select.py <IMAGEPATH>*.png
        Set <IMAGEPATH> to the approprate directory, *.png will grab all .png files.
	Use mouse/touch pad to create box around the object.
	Press s to save coordinates.
	Press w to close picture and go to the next one. 

The file, build_dataset.py, will separate and randomly assign dataset into 80% train, 10% test, and 10% validation datasets.
	Set image_path to the appropriate image directory.
	In the image directory, create directories called train, test, and val. 
	To run script:
		python build_dataset.py 
	
The file, data_to_JSON.py, will create a JSON format annotation file (used in MASK tutorial).
	Set image_path to the approriate image directory. 
	To run script:
		python data_to_JSON.py

The file, create_labels.py, will create a csv format annotation file (used in model/research/object_detection tutorial).
	Set image_path to the appropriate image directory.
	To run script:
		python create_labels.py

After running the create_lables.py, the generate_tfrecord.py will create .record files for tensorflow to read.
	To run script:
		# From tensorflow/models/research/
  		# Create train data:
  		python generate_tfrecord.py --csv_input=data/train_labels.csv  --output_path=data/train.record

  		# Create test data:
  		python generate_tfrecord.py --csv_input=data/test_labels.csv  --output_path=data/test.record	

