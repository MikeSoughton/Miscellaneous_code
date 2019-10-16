#!/usr/bin/env python3

"""
    Script to adapt a json keypoint file and output a json file with keypoints added or removed

    __author__ = "Michael Soughton"

"""

import os
import json
import numpy as np
from pycocotools.coco import COCO

# Import the dataset to adapt
instance_annotation_file = './train_cow_28_keypoints.json'
dataset = json.load(open(instance_annotation_file, 'r'))
assert type(dataset) == dict, 'annotation file format {} not supported'.format(type(dataset))

output_file_name = 'train_cow_26_keypoints.json'

# =============================================== SCRIPT STARTS HERE  ==================================================

# Define the number of keypoints
num_kps = 26

# Define the keypoints to drop and their positions in the keypoint list:
dropped_kps = ["left_upper_hip", "right_upper_hip", "left_upper_shoulder", "right_upper_shoulder"]
dropped_kps_pos = [17, 18, 20 ,21]
# Account for kp x, y, vis

# Define the keypoints to add and their positions in the keypoint list:
added_kps = ["bottom_spine", "top_spine"]
added_kps_pos = [17, 18]

num_new_kps = abs(len(dropped_kps_pos) - len(added_kps_pos))

# Account for kp x, y, vis
dropped_kps_pos = [[x*3, x*3 + 1, x*3 +2] for x in dropped_kps_pos]
added_kps_pos = [[x*3, x*3 + 1, x*3 +2] for x in added_kps_pos]

# Return list of tuples to list
dropped_kps_pos = [item for tuple in dropped_kps_pos for item in tuple]
added_kps_pos = [item for tuple in added_kps_pos for item in tuple]

# Create dictionaries and lists for annotations, categories and images
anns_list, cats_list, imgs_list = [], [], []

if 'images' in dataset:
    for img in dataset['images']:
        imgs_list.append(img)

# Create lists (and dictionaries) for the dataset components for annotations, images and categories which meet the above criterion
if 'annotations' in dataset:

    # Count the number of annotations changed
    num_modified_annos_changed = 0
    for ann in dataset['annotations']:
        # Add the number of keypoints
        if 'num_keypoints' in ann:
            if ann['num_keypoints'] != num_kps:
                ann['num_keypoints'] = num_kps

        elif 'num_keypoints' not in ann:
            ann['num_keypoints'] = num_kps

        # Drop selected keypoints
        dropped_ann = []
        for i, j in enumerate(ann['keypoints']):
            if i not in dropped_kps_pos:
                dropped_ann.append(j)
        ann['keypoints'] = dropped_ann

        # If the image has previously been modified, then we do not want to change the existing keypoints, but just add
        # the new ones in at default positions
        if ann['modified'] == 'modified':
            #anns_list.append(ann)

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

            # If the bounding box is left of center, place new keypoints slightly to the right
            if (top_left_x + box_width/2.) < (image_width/2.):
                xlinlist = np.linspace(top_left_x + box_width/8. + spacing, top_left_x + 7*box_width/8. + spacing, num_new_kps).tolist()

            # If the bounding box is right of center, place new keypoints slightly to the left
            elif (top_left_x + box_width/2.) > (image_width/2.):
                xlinlist = np.linspace(top_left_x + box_width/8. - spacing, top_left_x + 7*box_width/8. - spacing, num_new_kps).tolist()

            # If the bounding box is above center, place new keypoints slightly to the bottom
            if (top_left_y + box_height/2.) < (image_height/2.):
                ylinlist = np.full((num_new_kps,), top_left_y + box_height + spacing)

            # If the bounding box below center, place new keypoints slightly to the top
            elif (top_left_y + box_height/2.) > (image_height/2.):
                ylinlist = np.full((num_new_kps,), top_left_y - spacing)

            # Add the visibility values (0 = N/A, 1 = occluded, 2 = visible), set to 2 by default
            vislist = np.full((num_new_kps,), 2)

            # For some strange reason the integers in vislist are 'numpy.int32' which cannot be stored in JSON format, so convert them to standard ints
            int_vislist = []
            for i in vislist:
                int_vislist.append(int(i))

            # Put the keypoint coordinates into a list and add them to the dictionary
            zipped_list = [(i, j, k) for i, j, k in zip(xlinlist, ylinlist, int_vislist)]
            new_keypoint_list = [item for t in zipped_list for item in t]
            #ann['keypoints'] = keypoint_list
            #print(new_keypoint_list)
            #print(len(ann['keypoints']))
            # Insert the default values for new keypoints at the appropriate indices of 'keypoints'
            for new_kp_value_idx, new_kp_idx in enumerate(added_kps_pos):
                #print(new_kp_idx, new_kp_value_idx)
                ann['keypoints'].insert(new_kp_idx,new_keypoint_list[new_kp_value_idx])

            num_modified_annos_changed += 1
            my_ann = ann['keypoints']

            anns_list.append(ann)

        # If the image has not previously been modified, then we do want to change all the existing keypoints
        # by defining a new set of default points
        elif ann['modified'] == 'default':
            #anns_list.append(ann)

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

            # If the bounding box is left of center, place new keypoints slightly to the right
            if (top_left_x + box_width / 2.) < (image_width / 2.):
                xlinlist = np.linspace(top_left_x + spacing, top_left_x + box_width + spacing, num_kps).tolist()

            # If the bounding box is right of center, place new keypoints slightly to the left
            elif (top_left_x + box_width / 2.) > (image_width / 2.):
                xlinlist = np.linspace(top_left_x - spacing, top_left_x + box_width - spacing, num_kps).tolist()

            # If the bounding box is above center, place new keypoints slightly to the bottom
            if (top_left_y + box_height / 2.) < (image_height / 2.):
                ylinlist = np.full((num_kps,), top_left_y + box_height + spacing)

            # If the bounding box below center, place new keypoints slightly to the top
            elif (top_left_y + box_height / 2.) > (image_height / 2.):
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

            anns_list.append(ann)

if 'categories' in dataset:
    for cat in dataset['categories']:
        cat['keypoints'] = ["nose", "left_eye", "right_eye", "left_ear", "right_ear", "left_lower_shoulder",
                           "right_lower_shoulder", "front_left_knee", "front_right_knee", "front_left_hoof",
                            "front_right_hoof", "left_lower_hip", "right_lower_hip", "rear_left_knee", "rear_right_knee",
                            "rear_left_hoof", "rear_right_hoof", "bottom_spine", "top_spine", "underbelly", "top_head",
                            "chin", "dewlap", "top_tail", "middle_tail", "bottom_tail"]

        cat['skeleton'] = [[16, 14], [14, 12], [17, 15], [15, 13], [12, 18], [13, 18], [18, 20], [19, 20], [6, 20], [7, 20],
                           [19, 28], [6, 8], [7, 9], [8, 10], [9, 11], [18, 6], [18, 7], [2, 3], [1, 2], [1,3], [2, 4], [3, 5],
                           [2, 21], [3, 21], [4, 21], [5, 21], [1, 22], [22, 23], [23, 6], [23, 7], [18, 24], [24, 25], [25, 26]]
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
with open(output_file_name, 'w') as output_json:
    json.dump(dataset_export, output_json)
print("Saved output file as '{}'".format(output_file_name))