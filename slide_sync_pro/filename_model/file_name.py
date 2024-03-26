import os


def get_file_names(folder_path):
    # Check if the provided path is a directory
    if not os.path.isdir(folder_path):
        print("Error: Not a valid directory path.")
        return

    # Get list of files in the directory
    files = os.listdir(folder_path)

    # Print the names of the files
    print("Files in the folder:")
    for file_name in files:
        return file_name





