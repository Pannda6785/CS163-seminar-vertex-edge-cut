import cv2
import os

# Folder containing the PNG images
image_folder = r'D:\An\Projects\_tests_\frames\batch1'

# Get all PNG files in the folder and sort them
image_files = sorted([os.path.join(image_folder, img) for img in os.listdir(image_folder) if img.endswith(".png")])

# Define a uniform size for the video frames (width, height)
target_size = (1150, 1150)  # You can change this to whatever size you prefer

# Create a video writer object (use appropriate FPS, e.g., 10 or 30)
video = cv2.VideoWriter('output.mp4', cv2.VideoWriter_fourcc(*'mp4v'), 10, target_size)

# Read and resize each image, then write to the video
for image_file in image_files:
    img = cv2.imread(image_file)
    resized_img = cv2.resize(img, target_size)  # Resize the image
    video.write(resized_img)

# Release the video writer
video.release()
