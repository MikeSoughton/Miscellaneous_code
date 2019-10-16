"""
    Module to create new file extensions of the form 00x.

    Params:

        output_directory: str - the directory of the desired output
        output_file_name: str - the name of the file (without file type extension) to output. Required
        file_type: str - the file type to output, e.g. .txt - works with or without a dot. Not required

    Returns:

        new_output_file_name: str - the name of with file, with a new extension of the form 00x

"""

import os

# ====================================== CREATE NEW FILE EXTENSIONS ====================================================

def file(output_directory, output_file_name, file_type = None):

    # File to save (without extension)
    #output_file_name = 'val_cow_28_keypoints_default'
    output_file_name_list = [output_file_name]

    # Check the number of files with file name already existing
    num_existing_files = 0
    for fname in os.listdir(output_directory):           # change directory as needed
        if os.path.isfile(os.path.join(output_directory, fname)):           # make sure it's a file, not a directory entry
            if output_file_name in fname:    # if there exists a file matching our file name, add one to the number of existing files
                num_existing_files += 1

    # Create a list of file names for the number of exisiting files
    for i in range(num_existing_files):
        output_file_name_list.append(output_file_name)

    # Create a new list appending to the previous ones an extension of the form '00x'
    new_output_file_name_list = []
    for idx, item in enumerate(output_file_name_list, start = 1):
        new_output_file_name_list.append(item + '_{}'.format(str(idx).zfill(3)))

    # Get the new file name
    if file_type is None:
        new_output_file_name = new_output_file_name_list[len(new_output_file_name_list) - 1]
    elif file_type is not None:
        # Format file_type to remove the dot if it exists (we will add it in again later)
        if file_type.find('.') != -1:
            file_type = file_type.replace('.', '')
        new_output_file_name = new_output_file_name_list[len(new_output_file_name_list) - 1] + '.' + file_type

    return new_output_file_name