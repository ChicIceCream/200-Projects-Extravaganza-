import cv2
import os
import csv
import numpy as np

def create_video_from_euroc(dataset_path, output_filename="euroc_video.mp4", fps=20.0):
    """
    Creates a video from a EuRoC MAV dataset image sequence.

    Args:
        dataset_path (str): The path to the 'cam0' or 'cam1' folder 
                            containing 'data.csv' and the 'data' subfolder.
        output_filename (str): The name of the video file to be created.
        fps (float): The frames per second for the output video.
    """
    
    print("--- EuRoC Dataset to Video Converter ---")

    # --- Step 1: Validate Paths ---
    csv_path = os.path.join(dataset_path, 'data.csv')
    image_folder_path = os.path.join(dataset_path, 'data')

    if not os.path.isdir(dataset_path):
        print(f"\nError: Dataset path not found at '{dataset_path}'")
        return
    if not os.path.isfile(csv_path):
        print(f"\nError: 'data.csv' not found inside '{dataset_path}'")
        return
    if not os.path.isdir(image_folder_path):
        print(f"\nError: 'data' folder not found inside '{dataset_path}'")
        return

    print(f"Dataset found at: {dataset_path}")

    # --- Step 2: Read the CSV and Get Image Filenames ---
    image_filenames = []
    with open(csv_path, 'r') as csvfile:
        reader = csv.reader(csvfile)
        # Skip the header row (e.g., #timestamp [ns],filename)
        next(reader, None)  
        for row in reader:
            image_filenames.append(row[1]) # The filename is in the second column
    
    if not image_filenames:
        print("\nError: No image filenames found in data.csv. The file might be empty or malformed.")
        return
        
    print(f"Found {len(image_filenames)} image entries in data.csv.")

    # --- Step 3: Determine Video Dimensions ---
    # Read the first image to get its size (width, height)
    try:
        first_image_path = os.path.join(image_folder_path, image_filenames[0])
        first_image = cv2.imread(first_image_path)
        if first_image is None:
            print(f"\nError: Could not read the first image at '{first_image_path}'")
            return
        height, width, layers = first_image.shape
        size = (width, height)
        print(f"Video dimensions will be: {width}x{height}")
    except Exception as e:
        print(f"\nAn error occurred while reading the first image: {e}")
        return

    # --- Step 4: Initialize the Video Writer ---
    # Define the codec and create VideoWriter object
    fourcc = cv2.VideoWriter_fourcc(*'mp4v') # For .mp4 file
    out = cv2.VideoWriter(output_filename, fourcc, fps, size)
    print(f"Output video will be '{output_filename}' at {fps} FPS.")

    # --- Step 5: Loop Through Images and Write to Video ---
    print("\nStarting video creation process...")
    for i, filename in enumerate(image_filenames):
        image_path = os.path.join(image_folder_path, filename)
        
        if os.path.exists(image_path):
            img = cv2.imread(image_path)
            out.write(img)
            # Print progress every 100 frames
            if (i + 1) % 100 == 0:
                print(f"  Processed {i + 1} / {len(image_filenames)} frames...")
        else:
            print(f"  Warning: Image file not found, skipping: {filename}")

    # --- Step 6: Finalize ---
    # Release everything when the job is done
    out.release()
    print("\n-----------------------------------------")
    print("SUCCESS: Video creation complete!")
    print(f"Your video has been saved as '{output_filename}' in the same directory as the script.")
    print("-----------------------------------------")

if __name__ == '__main__':
    # --- IMPORTANT: SET YOUR DATASET PATH HERE ---
    # This path should point to the folder containing 'data.csv' and the 'data' folder
    # Example for Windows: "C:/Users/User/Downloads/V1_01_easy/mav0/cam0"
    # Example for Linux/Mac: "/home/user/datasets/V1_01_easy/mav0/cam0"
    euroc_dataset_path = "C:\\Users\\User\\Downloads\\V1_01_easy\\mav0\\cam0"
    
    create_video_from_euroc(euroc_dataset_path)