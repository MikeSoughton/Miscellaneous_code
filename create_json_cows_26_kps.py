#!/usr/bin/env python3

"""
    Script to search through a coco json datafile for images within a certain category (here cows) and output a json
    file with only images, annotations and categories within the specified categor(ies).

    __author__ = "Michael Soughton"

"""

import os
import json
import numpy as np
from pycocotools.coco import COCO

# Import the dataset
instance_annotation_file = 'D:/MikeDisk/projects/coco-annotator/annotation_tools/data/annotations/instances_val2017.json'
dataset = json.load(open(instance_annotation_file, 'r'))
assert type(dataset) == dict, 'annotation file format {} not supported'.format(type(dataset))

# ====================================== CREATE NEW FILE EXTENSIONS ====================================================

# File to save (without extension)
output_file_name = 'val_cow_28_keypoints_default'
output_file_name_list = [output_file_name]

# Check the number of files with file name already existing
num_existing_files = 0
for fname in os.listdir('.'):           # change directory as needed
    if os.path.isfile(fname):           # make sure it's a file, not a directory entry
        if output_file_name in fname:   # if there exists a file matching our file name, add one to the number of existing files
            num_existing_files += 1

# Create a list of file names for the number of exisiting files
for i in range(num_existing_files):
    output_file_name_list.append(output_file_name)

# Create a new list appending to the previous ones an extension of the form '00x'
new_output_file_name_list = []
for idx, item in enumerate(output_file_name_list, start = 1):
    new_output_file_name_list.append(item + '_{}'.format(str(idx).zfill(3)))

# Get the new file name
new_output_file_name = new_output_file_name_list[len(new_output_file_name_list) - 1] + '.json'


# ===================================== CREATE A NEW DICTIONARY FROM THE DATASET =======================================

# Define the number of keypoints
num_kps = 28

# Create dictionaries and lists for annotations, categories and images
anns_list, cats_list, imgs_list = [], [], []

# We must first get the image and annotation (and category) Ids for cows
coco = COCO(instance_annotation_file)
catIds = coco.getCatIds(catNms=['cow'])
imgIds = coco.getImgIds(catIds=catIds)
annIds = coco.getAnnIds(imgIds=imgIds, catIds=catIds, iscrowd=None)

if 'images' in dataset:
    for img in dataset['images']:
        if img['id'] in imgIds:
            imgs_list.append(img)

# Create lists (and dictionaries) for the dataset components for annotations, images and categories which meet the above criterion
if 'annotations' in dataset:
    for ann in dataset['annotations']:
        if ann['id'] in annIds:
            anns_list.append(ann)
            # Add the number of keypoints
            ann['num_keypoints'] = num_kps

            # We want to create some default keypoints within the bounding box of an annotation
            # We could normalise the default cow skeleton to the size of the bounding box and center the skeleton in the box
            # Instead I will create a horizontal line just above or below the box

            # Need to get image Id to check where the bounding box is in relations to the image edges
            img_ids = [dict['id'] for dict in imgs_list]
            img_heights = [dict['height'] for dict in imgs_list]
            img_widths = [dict['width'] for dict in imgs_list]

            img_id = ann['image_id']
            image_height = [dict['height'] for dict in imgs_list if dict['id'] == img_id][0]
            image_width = [dict['width'] for dict in imgs_list if dict['id'] == img_id][0]

            # Find the bounding box infomation
            top_left_x = ann['bbox'][0]
            top_left_y = ann['bbox'][1]
            box_width = ann['bbox'][2]
            box_height = ann['bbox'][3]

            # If not too close to the top of the image, make keypoints above the bounding box
            # In the image x coordinates start from 0 at the left and y coordinates start from 0 at the top

            # Define a spacing to displace the keypoints by
            spacing = 7.

            # If the bounding box is left of center, place keypoints slightly to the right
            if (top_left_x + box_width/2.) < (image_width/2.):
                xlinlist = np.linspace(top_left_x + spacing, top_left_x + box_width + spacing, num_kps).tolist()

            # If the bounding box is right of center, place keypoints slightly to the left
            elif (top_left_x + box_width/2.) > (image_width/2.):
                xlinlist = np.linspace(top_left_x - spacing, top_left_x + box_width - spacing, num_kps).tolist()

            # If the bounding box is above center, place keypoints slightly to the bottom
            if (top_left_y + box_height/2.) < (image_height/2.):
                ylinlist = np.full((num_kps,), top_left_y + box_height + spacing)

            # If the bounding box below center, place keypoints slightly to the top
            elif (top_left_y + box_height/2.) > (image_height/2.):
                ylinlist = np.full((num_kps,), top_left_y - spacing)

            # Add the visibility values (0 = N/A, 1 = occluded, 2 = visible), set to 2 by default
            vislist = np.full((num_kps,), 2)

            # For some strange reason the integers in vislist are 'numpy.int32' which cannot be stored in JSON format, so convert them to standard ints
            int_vislist = []
            for i in vislist:
                int_vislist.append(int(i))

            # Put the keypoint coordinates into a list and add them to the dictionary
            zipped_list = [(i, j, k) for i, j, k in zip(xlinlist, ylinlist, int_vislist)]
            keypoint_list = [item for t in zipped_list for item in t]
            ann['keypoints'] = keypoint_list

            # Set a value so that we can track if an annotation has been modified
            ann['modified'] = 'default'

if 'categories' in dataset:
    for cat in dataset['categories']:
        if cat['id'] in catIds:
            cat['keypoints'] = ["nose", "left_eye", "right_eye", "left_ear", "right_ear", "left_lower_shoulder",
                               "right_lower_shoulder", "front_left_knee", "front_right_knee", "front_left_hoof",
                                "front_right_hoof", "left_lower_hip", "right_lower_hip", "rear_left_knee", "rear_right_knee",
                                "rear_left_hoof", "rear_right_hoof", "left_upper_hip", "right_upper_hip", "underbelly",
                                "left_upper_shoulder", "right_upper_shoulder", "top_head", "chin", "dewlap", "top_tail",
                                "middle_tail", "bottom_tail"]
            cat['skeleton'] = [[16, 14], [14, 12], [17, 15], [15, 13], [12, 18], [13, 19], [18, 19], [18, 20], [19, 20], [6, 20],
                               [7, 20], [21, 18], [22, 19], [6, 8], [7, 9], [8, 10], [9, 11], [21, 6], [22, 7], [2, 3], [1, 2],
                               [1, 3], [2, 23], [3, 23], [4, 23], [5, 23], [1, 24], [24, 25], [25, 6], [25, 7], [18, 26], [19, 26],
                               [26, 27], [27, 28]]
            cats_list.append(cat)

# Add the licences
licenses_list = dataset['licenses']

# Create a dictionary (of lists of dictionaries)) for the json file
dataset_export = {
    'categories' : cats_list,
    'annotations' : anns_list,
    'images' : imgs_list,
    'licenses' : licenses_list
  }

# Write the new dataset to a json file
with open(new_output_file_name, 'w') as output_json:
    json.dump(dataset_export, output_json)
print("Saved output file as '{}'".format(new_output_file_name))