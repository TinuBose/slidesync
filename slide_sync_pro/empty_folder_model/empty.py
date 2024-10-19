import os

def empty_folder(folder_path):
    # Ensure the folder path is valid
    if not os.path.exists(folder_path):
        print(f"The folder {folder_path} does not exist.")
        return

    # Iterate over the contents of the folder
    for root, dirs, files in os.walk(folder_path, topdown=False):
        for name in files:
            # Construct full file path
            file_path = os.path.join(root, name)
            # Remove the file
            os.remove(file_path)
        for name in dirs:
            # Construct full directory path
            dir_path = os.path.join(root, name)
            # Remove the directory
            os.rmdir(dir_path)

    print(f"The folder {folder_path} has been emptied.")

# Example usage
