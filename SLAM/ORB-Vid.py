import cv2
import numpy as np
import os
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

def save_point_cloud_to_ply(points_3d, colors_3d, filename="room_map1.ply"):
    """
    Saves a 3D point cloud with colors to a .ply file.
    """
    if not points_3d:
        print("Point cloud is empty, nothing to save.")
        return

    points_3d = np.array(points_3d)
    colors_3d = np.array(colors_3d)

    ply_header = f"""ply
format ascii 1.0
element vertex {len(points_3d)}
property float x
property float y
property float z
property uchar red
property uchar green
property uchar blue
end_header
"""
    combined = np.hstack([points_3d, colors_3d])
    
    with open(filename, 'w') as f:
        f.write(ply_header)
        np.savetxt(f, combined, fmt="%f %f %f %d %d %d")
        
    print(f"\nSUCCESS: 3D map saved to '{filename}'")
    print("You can now open this file with a 3D viewer like MeshLab or CloudCompare.")


def run_visual_odometry_with_live_plot():
    # --- IMPORTANT: SET YOUR VIDEO PATH HERE ---
    video_path = "euroc_video.mp4"
    # -------------------------------------------

    if not os.path.exists(video_path) or "path/to" in video_path:
        print("\nError: Video path is not set or does not exist.")
        print("Please edit the script and change the 'video_path' variable.")
        return

    # --- Camera Intrinsics ---
    cap_check = cv2.VideoCapture(video_path)
    W = int(cap_check.get(cv2.CAP_PROP_FRAME_WIDTH))
    H = int(cap_check.get(cv2.CAP_PROP_FRAME_HEIGHT))
    cap_check.release()
    FOCAL_LENGTH = W / 2 
    K = np.array([[FOCAL_LENGTH, 0, W/2], [0, FOCAL_LENGTH, H/2], [0, 0, 1]])

    print(f"Video resolution detected: W={W}, H={H}")
    print(f"Using assumed focal length: F={FOCAL_LENGTH}\n")
    
    # --- Setup ---
    cap = cv2.VideoCapture(video_path)
    orb = cv2.ORB_create(nfeatures=3000)
    bf = cv2.BFMatcher(cv2.NORM_HAMMING, crossCheck=False)
    
    last_frame_data = None
    current_R, current_t = np.identity(3), np.zeros((3, 1))
    
    map_points = []
    map_colors = []
    path_history = [current_t.flatten()]

    # --- Matplotlib 3D Live Plot Setup ---
    plt.ion()
    fig = plt.figure(figsize=(15, 10))
    ax = fig.add_subplot(111, projection='3d')

    frame_count = 0
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret: break

        frame_count += 1
        if frame_count % 5 != 0: continue

        print(f"Processing frame {frame_count}...")
        gray_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        kp, des = orb.detectAndCompute(gray_frame, None)

        if des is None: continue
        if last_frame_data is None:
            last_frame_data = {'kp': kp, 'des': des, 'frame': frame}
            continue

        last_kp, last_des = last_frame_data['kp'], last_frame_data['des']
        matches = bf.knnMatch(last_des, des, k=2)

        good_matches = []
        for item in matches:
            if len(item) == 2:
                m, n = item
                if m.distance < 0.75 * n.distance: good_matches.append(m)

        if len(good_matches) < 20: continue
            
        last_pts = np.float32([last_kp[m.queryIdx].pt for m in good_matches])
        current_pts = np.float32([kp[m.trainIdx].pt for m in good_matches])

        E, mask = cv2.findEssentialMat(current_pts, last_pts, K, method=cv2.RANSAC, prob=0.999, threshold=1.0)
        if E is None: continue

        _, rel_R, rel_t, mask = cv2.recoverPose(E, current_pts, last_pts, K, mask=mask)

        # *** THE FIX IS HERE: Check if there are any inlier points ***
        if mask is None or mask.sum() == 0:
            print(f"Frame {frame_count}: RANSAC rejected all points. Skipping triangulation.")
            last_frame_data = {'kp': kp, 'des': des, 'frame': frame}
            continue

        scale = 1.0 
        current_t = current_t + scale * (current_R @ rel_t)
        current_R = rel_R @ current_R
        path_history.append(current_t.flatten())

        last_pts_inliers = last_pts[mask.ravel() == 1]
        current_pts_inliers = current_pts[mask.ravel() == 1]

        points_4d_hom = cv2.triangulatePoints(K @ np.hstack((np.identity(3), np.zeros((3,1)))), 
                                            K @ np.hstack((rel_R, rel_t)), 
                                            last_pts_inliers.T, current_pts_inliers.T)
        points_3d = (points_4d_hom / points_4d_hom[3])[:3,:].T
        
        colors_for_points = []
        for pt in last_pts_inliers:
            x, y = int(pt[0]), int(pt[1])
            b, g, r = last_frame_data['frame'][y, x]
            colors_for_points.append([r, g, b])
        
        global_points_3d = (current_R @ points_3d.T + current_t).T
        
        map_points.extend(global_points_3d)
        map_colors.extend(colors_for_points)
        
        # --- Live Visualization ---
        ax.cla()
        path = np.array(path_history)
        ax.plot(path[:, 0], path[:, 2], -path[:, 1], 'b-', label='Camera Path')
        
        if map_points:
            map_pts_arr = np.array(map_points)
            map_clr_arr = np.array(map_colors) / 255.0 # Normalize colors to 0-1 for scatter plot
            # Downsample for performance
            sample_indices = np.random.choice(map_pts_arr.shape[0], size=min(2000, map_pts_arr.shape[0]), replace=False)
            ax.scatter(map_pts_arr[sample_indices, 0], map_pts_arr[sample_indices, 2], -map_pts_arr[sample_indices, 1], 
                       c=map_clr_arr[sample_indices], marker='.', s=2, label='3D Map Points')

        ax.set_title("Live Visual Odometry")
        ax.set_xlabel('X'); ax.set_ylabel('Z'); ax.set_zlabel('Y')
        ax.legend()
        plt.pause(0.01)

        last_frame_data = {'kp': kp, 'des': des, 'frame': frame}
    
    cap.release()
    plt.ioff() # Turn off interactive mode for the final plot
    print("\nVideo processing finished. Displaying final map.")
    
    # Show the final plot and wait for user to close it
    fig.canvas.manager.set_window_title("Final Result - Close this window to save .ply file")
    plt.show()

    save_point_cloud_to_ply(map_points, map_colors)

if __name__ == '__main__':
    run_visual_odometry_with_live_plot()