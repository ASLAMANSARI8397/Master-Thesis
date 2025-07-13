#!/usr/bin/env python3

import os
import time

def guide_user():
    print("\n🚀 ROS BAG TO VIDEO PIPELINE - COMPLETE TERMINAL GUIDE 🚀")

    # TERMINAL #1: Hard Disk Check
    print("\n--- TERMINAL #1: Check External Hard Disk ---")
    print("1️⃣ Open Terminal #1.")
    print("2️⃣ List all drives on macOS:")
    print("   ls /Volumes")
    disk_name = input("Enter your hard disk name (e.g., One_Touch): ")
    print(f"3️⃣ Verify folder with .bag file:")
    print(f"   ls /Volumes/{disk_name}")
    folder_name = input("Enter the folder name (e.g., Test2_16_30_R-C): ")
    input("Press Enter after confirming the folder contains your .bag file...")

    # TERMINAL #2: Reuse or Create Docker Container
    print("\n--- TERMINAL #2: Reuse or Create Docker Container ---")
    print("1️⃣ Check existing containers:")
    print("   docker ps -a")
    print("2️⃣ If you see a container (e.g., 'ros_container_final') you created previously:")
    print("   docker start ros_container_final")
    print("   docker attach ros_container_final")
    print("   (This reuses your container with all installed packages.)")
    print()
    print("3️⃣ If no container exists with your packages (or you want a fresh one), do:")
    print("   docker stop ros_container_final  (if exists)")
    print("   docker rm ros_container_final    (if exists)")
    print("   docker run -it --name ros_container_final \\")
    print(f"      -v /Volumes/{disk_name}:/rosbag_data \\")
    print("      my-ros-final bash")
    input("Press Enter after Terminal #2 is running (reused or new) Docker container...")

    print("4️⃣ Inside Docker, source ROS environment and start roscore:")
    print("   source /opt/ros/noetic/setup.bash")
    print("   roscore")
    input("Press Enter after roscore is running...")

    # TERMINAL #3: Play ROS Bag (with --clock)
    print("\n--- TERMINAL #3: Play ROS Bag ---")
    print("1️⃣ Open Terminal #3.")
    print("2️⃣ Attach to your container (e.g., ros_container_final):")
    print("   docker exec -it ros_container_final bash")
    print(f"3️⃣ Navigate to folder and play bag with --clock:")
    print(f"   cd /rosbag_data/{folder_name}")
    print("   rosbag play --clock 1.bag")
    print("   (Wait until the bag is fully played and topics are published.)")
    input("Press Enter when the ROS bag is playing...")

    # TERMINAL #4: Extract Frames
    print("\n--- TERMINAL #4: Extract Images from ROS Bag ---")
    print("1️⃣ Open Terminal #4 and attach to Docker (e.g., ros_container_final):")
    print("   docker exec -it ros_container_final bash")
    print("2️⃣ Create output folder for images:")
    print(f"   mkdir -p /rosbag_data/{folder_name}/output_images")
    print("3️⃣ Check available image topics:")
    print("   rostopic list")
    print("   (Ensure your desired image topic is listed, e.g., /camera/color/image_raw)")
    image_topic = input("Enter the image topic (e.g., /camera/color/image_raw): ")
    print("4️⃣ Run image extraction:")
    print(f"   rosrun image_view extract_images \\")
    print(f"      _filename_format:=/rosbag_data/{folder_name}/output_images/frame%04d.png \\")
    print("      _sec_per_frame:=0 \\  # Set to 0 for every frame without skipping")
    print(f"      image:={image_topic}")
    print("   (Ensure image topic is remapped correctly to avoid syntax errors.)")
    input("Press Enter when images are extracted...")

    # TERMINAL #5: Convert & Save Inside Docker
    print("\n--- TERMINAL #5: Convert Images to Video (Inside Docker) ---")
    print("1️⃣ Attach to Docker container (e.g., ros_container_final):")
    print("   docker exec -it ros_container_final bash")
    print("2️⃣ Convert frames to video using ffmpeg:")
    print(f"   ffmpeg -framerate 10 -i /rosbag_data/{folder_name}/output_images/frame%04d.png \\")
    print(f"      -c:v libx264 -pix_fmt yuv420p /rosbag_data/{folder_name}/output_images/output_video.mp4")
    print("   (This ensures ffmpeg is run inside Docker where the images are stored.)")
    print("3️⃣ Verify the video is saved inside Docker:")
    print(f"   ls /rosbag_data/{folder_name}/output_images/output_video.mp4")
    print("\n✅ Solution 1 Implemented: ffmpeg is run inside Docker to avoid path issues.")
    input("Press Enter when the video is generated...")

    print("\n🎉 ALL STEPS COMPLETED! Your video is ready inside Docker.")

if __name__ == '__main__':
    guide_user()