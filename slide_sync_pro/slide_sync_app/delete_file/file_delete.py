import os

def empty_directory(directory):
    # Check if the directory exists
    if not os.path.exists(directory):
        print(f"The directory '{directory}' does not exist.")
        return

    # Iterate over all the files and subdirectories in the directory
    for root, dirs, files in os.walk(directory):
        for file in files:
            file_path = os.path.join(root, file)
            # Remove the file
            os.remove(file_path)

        for dir in dirs:
            dir_path = os.path.join(root, dir)
            # Remove the subdirectory and its contents
            os.rmdir(dir_path)

    print(f"The directory '{directory}' has been emptied.")

# Example usage:
