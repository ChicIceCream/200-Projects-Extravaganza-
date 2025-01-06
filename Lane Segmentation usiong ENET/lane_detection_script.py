import cv2
import numpy as np
import torch
from scipy.signal import savgol_filter
from lane_detector import ENet  # Assuming you have a custom ENet class
import time
# Parameters for smoothing
window_length = 5  # Window size for moving average, adjust as needed
polyorder = 2      # Polynomial order for Savitzky-Golay filter

# Function to apply smoothing and outlier detection
def smooth_and_filter_detections(left_lane_positions, right_lane_positions):
    if len(left_lane_positions) >= window_length:
        left_lane_smoothed = savgol_filter(left_lane_positions, window_length, polyorder)
        right_lane_smoothed = savgol_filter(right_lane_positions, window_length, polyorder)
    else:
        left_lane_smoothed = np.array(left_lane_positions)
        right_lane_smoothed = np.array(right_lane_positions)

    return left_lane_smoothed[-1], right_lane_smoothed[-1]

# Updated process_and_save_video function
def process_and_save_video(input_video_path, output_video_path):
    cap = cv2.VideoCapture(input_video_path)
    frame_width = int(cap.get(3))
    frame_height = int(cap.get(4))
    out = cv2.VideoWriter(output_video_path, cv2.VideoWriter_fourcc(*'XVID'), 10, (frame_width, frame_height))
    
##################### ROI FULL #####################################
    # roi_vertices = np.array([[(0, frame_height),  # bottom left
    #                         (frame_width, frame_height),  # bottom right
    #                         (frame_width, 0),  # top right
    #                         (0, 0)]],  # top left
    #                         dtype=np.int32)
    
##################### ROI NORMAL ####################################
    roi_vertices = np.array([[(50, frame_height), # bottom left
                            (frame_width + 50, frame_height), # bottom right
                            (frame_width // 2 + 200, frame_height // 2), # upper right
                            (frame_width // 2 - 200, frame_height // 2)]], # upper left
                            dtype=np.int32)
    vehicle_center_x = frame_width // 2 + 10

    target_y = 400  # Y-coordinate corresponding to 2 meters away (approximately)
    frame_now = 1 # for logging frame number

    left_lane_positions = []
    right_lane_positions = []

    start = time.time()
    print("applying ROI")
    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        # Apply ROI mask to the frame
        
        print(f"Frame : {frame_now}")
        frame_now += 1
        mask = np.zeros_like(frame[:, :, 0])
        cv2.fillPoly(mask, roi_vertices, 255)
        masked_frame = cv2.bitwise_and(frame, frame, mask=mask)

        input_image = cv2.cvtColor(masked_frame, cv2.COLOR_BGR2GRAY)
        input_image = cv2.resize(input_image, (512, 256))
        input_image = input_image[..., None]
        input_tensor = torch.from_numpy(input_image).float().permute(2, 0, 1)

        with torch.no_grad():
            binary_logits, _ = enet_model(input_tensor.unsqueeze(0))

        binary_seg = torch.argmax(binary_logits, dim=1).squeeze().numpy()
        binary_seg = cv2.resize(binary_seg.astype(np.uint8), (frame_width, frame_height))

        # Apply the same ROI mask to the binary segmentation result
        binary_seg = cv2.bitwise_and(binary_seg, binary_seg, mask=mask)

        # Extract lane points at target_y within ROI
        left_lane_points = np.where((binary_seg[target_y, :vehicle_center_x] == 1))[0]
        right_lane_points = np.where((binary_seg[target_y, vehicle_center_x:] == 1))[0]

        if left_lane_points.size > 0:
            left_lane_center = np.mean(left_lane_points)
            left_lane_positions.append(left_lane_center)
        if right_lane_points.size > 0:
            right_lane_center = np.mean(right_lane_points) + vehicle_center_x
            right_lane_positions.append(right_lane_center)

        if len(left_lane_positions) >= window_length and len(right_lane_positions) >= window_length:
            left_lane_center, right_lane_center = smooth_and_filter_detections(left_lane_positions, right_lane_positions)
            lanes_center = (left_lane_center + right_lane_center) / 2
            lateral_offset = (lanes_center - vehicle_center_x) * 0.007

            output_image = frame.copy()
            cv2.polylines(output_image, [roi_vertices], isClosed=True, color=(0, 255, 0), thickness=2)

            lane_overlay = np.zeros_like(frame)
            lane_overlay[binary_seg == 1] = [0, 255, 255]
            output_image = cv2.addWeighted(output_image, 0.7, lane_overlay, 0.3, 0)

            # Draw lane centers and vehicle center
            lane_center_y = target_y
            car_center_y = target_y + 100  # 100 pixels below lane center

            # Draw centers
            cv2.circle(output_image, (int(left_lane_center), target_y), 5, (255, 0, 0), -1)
            cv2.circle(output_image, (int(right_lane_center), target_y), 5, (0, 0, 255), -1)
            cv2.circle(output_image, (int(lanes_center), lane_center_y), 8, (0, 255, 0), -1)
            cv2.circle(output_image, (int(vehicle_center_x), car_center_y), 8, (255, 0, 0), -1)

            # Draw connecting line between lane center and vehicle center
            cv2.line(output_image, 
                    (int(lanes_center), lane_center_y), 
                    (int(vehicle_center_x), car_center_y), 
                    (255, 0, 0), 2)

            # Add labels
            cv2.putText(output_image, "Lane Center", (int(lanes_center)-60, lane_center_y-10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
            cv2.putText(output_image, "Vehicle Center", (int(vehicle_center_x)-60, car_center_y+20), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 0, 0), 2)
            cv2.putText(output_image, f"Lateral Offset: {lateral_offset:.2f} meters", 
                        (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 255), 2)

            out.write(output_image)
            cv2.imshow('Lane Detection with Lateral Offset', output_image)

        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()

# Load the pre-trained model
model_path = 'ENET.pth'
enet_model = ENet(2, 4)  # (2,8) for enet_now_model

# Load the trained model's weights
enet_model.load_state_dict(torch.load(model_path, map_location=torch.device('cpu'),weights_only=False))
enet_model.eval()

input_video_path = "lane_vid"
output_video_path = 'lane_vid_output.avi'
process_and_save_video(input_video_path, output_video_path)