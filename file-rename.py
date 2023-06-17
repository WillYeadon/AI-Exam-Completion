import os

# Directory containing the files to rename
dir_path = "exam papers/Durham/pdf/Physics exams 2022"

# Loop over all files in the directory
for filename in os.listdir(dir_path):
    # Check if the file name has at least 8 characters
    if len(filename) >= 8:
        # Construct the new file name by replacing the first 8 characters with "2018-"
        new_filename = "2022-" + filename[8:]
        # Rename the file
        os.rename(os.path.join(dir_path, filename), os.path.join(dir_path, new_filename))
