"""
    Simple script to open and edit a text file, specifically to take only the contents of a line before a colon and
    then add a comma to the end of the new string.
"""

input_filename = './text_to_edit.txt'
output_filename = './edited_text.txt'

with open(input_filename,'r') as input_file:
    with open(output_filename, 'w') as output_file:
        for line in input_file:
            line = line.strip()     # Remove any leading and trailing whitespaces
            line = line.split(':')[0]  # Split on the colon and take only the part of the string prior to the colon
            line = line + ','   # Add a comma to the end of the line
            #print(line)

            # Write to a new file
            output_file.write(line)
            #output_file.write(line+'\n')    # Need to specify that we want a new line
