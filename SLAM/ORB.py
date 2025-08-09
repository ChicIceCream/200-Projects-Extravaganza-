import cv2
import matplotlib.pyplot as plt
import os

def feature_matching_demo():
    """
    This function performs feature detection and matching between two images
    and visualizes the results.
    """
    # --- IMPORTANT: SET YOUR IMAGE PATHS HERE ---
    path1 = "C:\\Users\\User\\Downloads\\1.jpg"
    path2 = "C:\\Users\\User\\Downloads\\2.jpg"
    # -------------------------------------------

    # Check if files exist
    if not os.path.exists(path1) or path1 == "path/to/your/first/image.jpg":
        print("\nError: The path for the first image is not set or does not exist.")
        print(f"Please edit the script and change the value of the 'path1' variable.")
        return
        
    if not os.path.exists(path2) or path2 == "path/to/your/second/image.jpg":
        print("\nError: The path for the second image is not set or does not exist.")
        print(f"Please edit the script and change the value of the 'path2' variable.")
        return

    # Read the images
    img1_color = cv2.imread(path1)
    img2_color = cv2.imread(path2)
    
    # Convert images to grayscale for feature detection
    img1_gray = cv2.cvtColor(img1_color, cv2.COLOR_BGR2GRAY)
    img2_gray = cv2.cvtColor(img2_color, cv2.COLOR_BGR2GRAY)

    # --- Step 1 & 2: Detect and Describe Landmarks (Keypoints) ---
    orb = cv2.ORB_create(nfeatures=1000)
    kp1, des1 = orb.detectAndCompute(img1_gray, None)
    kp2, des2 = orb.detectAndCompute(img2_gray, None)
    
    print(f"\nFound {len(kp1)} landmarks in the first image.")
    print(f"Found {len(kp2)} landmarks in the second image.")

    img1_keypoints = cv2.drawKeypoints(img1_color, kp1, None, color=(0, 255, 0), flags=0)
    img2_keypoints = cv2.drawKeypoints(img2_color, kp2, None, color=(0, 255, 0), flags=0)

    plt.figure(figsize=(20, 10))
    plt.subplot(1, 2, 1); plt.imshow(cv2.cvtColor(img1_keypoints, cv2.COLOR_BGR2RGB)); plt.title('Landmarks Detected in Image 1'); plt.axis('off')
    plt.subplot(1, 2, 2); plt.imshow(cv2.cvtColor(img2_keypoints, cv2.COLOR_BGR2RGB)); plt.title('Landmarks Detected in Image 2'); plt.axis('off')
    plt.suptitle("Step 1 & 2: Landmark Detection", fontsize=16)
    plt.show()

    # --- Step 3 & 4: Match and Sort Landmarks ---
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=True)
    matches = bf.match(des1, des2)
    matches = sorted(matches, key=lambda x: x.distance)
    
    print(f"\nFound {len(matches)} initial matches between the two images.")

    # --- Step 5: Visualize the Best Matches ---
    num_matches_to_draw = 50
    print(f"Drawing the top {num_matches_to_draw} matches...")
    
    final_img = cv2.drawMatches(
        img1_color, kp1, 
        img2_color, kp2, 
        matches[:num_matches_to_draw], 
        None, 
        flags=cv2.DrawMatchesFlags_NOT_DRAW_SINGLE_POINTS
    )

    plt.figure(figsize=(25, 15))
    plt.imshow(cv2.cvtColor(final_img, cv2.COLOR_BGR2RGB))
    plt.title(f'Step 3-5: Top {num_matches_to_draw} Landmark Matches')
    plt.axis('off')
    plt.show()

if __name__ == '__main__':
    feature_matching_demo()
