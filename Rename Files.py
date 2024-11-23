import os

def rename_files_in_folder(folder_path):
    try:
        # Get all files in the folder
        files = os.listdir(folder_path)
        # Sort files to ensure consistent renaming
        files.sort()
        
        # Rename each file with a numeric sequence
        for index, file_name in enumerate(files, start=1):
            # Get the file extension
            file_extension = os.path.splitext(file_name)[1]
            # Define the new file name
            new_name = f"{index}{file_extension}"
            # Get full paths
            old_file_path = os.path.join(folder_path, file_name)
            new_file_path = os.path.join(folder_path, new_name)
            # Rename the file
            os.rename(old_file_path, new_file_path)
        print(f"Renamed {len(files)} files successfully.")
    except Exception as e:
        print(f"An error occurred: {e}")

folder_path = "C:\\Users\\User\\Desktop\\SIH DATASET\\Sat"  # Replace with your choice ot folder path
rename_files_in_folder(folder_path)
