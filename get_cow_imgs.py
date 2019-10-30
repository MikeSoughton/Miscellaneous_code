import os
import json
from shutil import copyfile


# ========================================= GET IMAGE IDS FOR MODIFIED COWS ============================================

# Specify what json file to use
instance_annotation_file = '../data/cow_data2017/annotations/train_cow_26_keypoints_91_imgs.json'
dataset = json.load(open(instance_annotation_file, 'r'))
assert type(dataset) == dict, 'annotation file format {} not supported'.format(type(dataset))

# Get the image ids of modified cows from the json file
modified_image_ids = []
if 'annotations' in dataset:
    for ann in dataset['annotations']:
        if ann['modified'] == 'modified':
            modified_image_ids.append(ann['image_id'])

# ===================================== GET COW IMAGES WITH IDS THAT ARE MODIFIED ======================================

image_directory = '../data/cow_data2017/images/train'
destination_directory = './cow_images'

# First get the names of all images within the specified folder, then copy selected ones to a new destination
if os.path.isdir(image_directory):
    for img_name in os.listdir(image_directory):
        if '.jpg' in img_name:

            # if an image file has Id (the image names contain their Id) also within the modified id list,
            # copy it to a new directory
            if int(img_name.strip('0').strip('.jpg')) in modified_image_ids:
                source = os.path.join(image_directory, img_name)
                destination = os.path.join(destination_directory, 'cow' + img_name.strip('0'))
                copyfile(source, destination)

else:
    print("The image directory is invalid.")
