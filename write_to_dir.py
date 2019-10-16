import os.path
import shutil
import os
import json

"""
    Module to create and write to a file within a directory and close and delete the file when called to do so.
    Works with the contents to write being a list (of dictionaries)

"""

# Write to a file within a directory
def write_file(dir_name,file_name, contents):
    # We will create a file within a folder within the current working directory
    cwd = os.getcwd()
    dir_path = os.path.join(cwd, dir_name)
    full_file_name = os.path.join(dir_path, file_name)

    # Check if the directory already exists, if not, create one
    try:
        os.stat(dir_path)
    except:
        os.mkdir(dir_path)

    # Write to the directory
    with open(full_file_name, 'w') as f:
        json.dump(contents, f)

# Read the contents of a file within a directory
def read_file(dir_name,file_name):
    cwd = os.getcwd()
    dir_path = os.path.join(cwd, dir_name)
    full_file_name = os.path.join(dir_path, file_name)
    contents = json.load(open(full_file_name, 'r'))
    return contents

# Close a directory and remove files within
def close_file(dir_name):
    # Only delete a directory if it contains the string 'temp' since we do not want to accidently delete important folders
    if 'temp' in dir_name:
        shutil.rmtree(dir_name)
    else:
        print("Will only delete folders containing the string 'temp' for saftey")

# Unecessary but I like to know how to print directories
def print_dirs():
    my_dirs = [d for d in os.listdir('.') if os.path.isdir(os.path.join('.', d))]
    print(my_dirs)