import cv2
import glob
import os
import numpy as np
import shutil
import random

# Function to apply gamma correction
def adjust_gamma(image, gamma=1.0):
    invGamma = 1.0 / gamma
    table = np.array([((i / 255.0) ** invGamma) * 255 for i in np.arange(0, 256)]).astype("uint8")
    return cv2.LUT(image, table)

# Function to apply color jittering (brightness, contrast, saturation)
def color_jitter(image, brightness=0, saturation=0):
    hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    h, s, v = cv2.split(hsv)
    v = cv2.add(v, brightness)
    s = cv2.add(s, saturation)
    hsv = cv2.merge((h, s, v))
    return cv2.cvtColor(hsv, cv2.COLOR_HSV2BGR)

# Function to rotate the image
def rotate_image(image, angle):
    (h, w) = image.shape[:2]
    center = (w // 2, h // 2)
    matrix = cv2.getRotationMatrix2D(center, angle, 1.0)
    return cv2.warpAffine(image, matrix, (w, h))

# Function to horizontally flip the image
def flip_image(image):
    return cv2.flip(image, 1)

# Function to scale (resize) the image
def scale_image(image, scale=1.0):
    return cv2.resize(image, (0, 0), fx=scale, fy=scale)

# Define paths
input_dir = "/Users/jarvis/Desktop/Data analysis project/all_frames"  # Input directory
output_dir = "/Users/jarvis/Desktop/Data analysis project/augmented/"  # Output directory
os.makedirs(output_dir, exist_ok=True)

# Get list of all images
images = glob.glob(os.path.join(input_dir, "*.jpg"))
print(f"Input directory: {input_dir}")
print(f"Images found: {images}")

# Check if there are any images
if not images:
    print("No images found in the specified directory. Please check the path and image format.")
    exit(1)

# Input: Specify the total number of images to process
total_images = int(input("Enter the total number of images to process for all augmentations: "))

# Save original images to the output directory
for image_path in images[:total_images]:
    shutil.copy(image_path, os.path.join(output_dir, os.path.basename(image_path)))

# Adjust images list to ensure it has only the needed number of images
images = images[:total_images]  # Limit images to the requested count

# Calculate number of images per augmentation
num_images_per_augmentation = total_images // 5  # Divide by the number of augmentations
extra_images = total_images % 5  # Any remaining images to add randomly

# Shuffle images to randomize augmentations
random.shuffle(images)

# Step 1: Gamma Correction
for image_path in images[:num_images_per_augmentation]:
    img = cv2.imread(image_path)
    gamma_img = adjust_gamma(img, gamma=1.5)
    filename = os.path.basename(image_path).replace(".jpg", "_gamma.jpg")
    cv2.imwrite(os.path.join(output_dir, filename), gamma_img)

# Step 2: Color Jittering
for image_path in images[num_images_per_augmentation:num_images_per_augmentation * 2]:
    img = cv2.imread(image_path)
    jittered_img = color_jitter(img, brightness=30, saturation=30)
    filename = os.path.basename(image_path).replace(".jpg", "_jitter.jpg")
    cv2.imwrite(os.path.join(output_dir, filename), jittered_img)

# Step 3: Rotation
for image_path in images[num_images_per_augmentation * 2:num_images_per_augmentation * 3]:
    img = cv2.imread(image_path)
    rotated_img = rotate_image(img, angle=15)  # Rotate by 15 degrees
    filename = os.path.basename(image_path).replace(".jpg", "_rotated.jpg")
    cv2.imwrite(os.path.join(output_dir, filename), rotated_img)

# Step 4: Flipping
for image_path in images[num_images_per_augmentation * 3:num_images_per_augmentation * 4]:
    img = cv2.imread(image_path)
    flipped_img = flip_image(img)
    filename = os.path.basename(image_path).replace(".jpg", "_flipped.jpg")
    cv2.imwrite(os.path.join(output_dir, filename), flipped_img)

# Step 5: Scaling
for image_path in images[num_images_per_augmentation * 4:num_images_per_augmentation * 5 + extra_images]:
    img = cv2.imread(image_path)
    scaled_img = scale_image(img, scale=1.2)  # Scale up by 20%
    filename = os.path.basename(image_path).replace(".jpg", "_scaled.jpg")
    cv2.imwrite(os.path.join(output_dir, filename), scaled_img)

print("Image augmentation completed!")



