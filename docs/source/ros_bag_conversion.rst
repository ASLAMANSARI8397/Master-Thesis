ROS Bag to Video Conversion
===========================

This section provides a complete guide to extract image frames from a `.bag` file and convert them into a playable video using ROS tools. The workflow is tailored for macOS with Docker and supports `.bag` files stored on an external hard drive.

1. Verify External Hard Drive Mount
-----------------------------------
Ensure your external drive (e.g., `One_Touch`) is mounted. To check available drives, run:

.. code-block:: bash
   :class: code-block-green

   ls /Volumes

You should see your external drive listed, such as:

.. code-block:: text

   One_Touch

2. Create and Launch Docker Container
-------------------------------------
Mount your external drive into the Docker container at `/rosbag_data`:

.. code-block:: bash
   :class: code-block-green

   docker run -it --name ros_container \
     --mount type=bind,source=/Volumes/One_Touch,target=/rosbag_data \
     ros:noetic

This launches a container named `ros_container` and mounts your external hard drive into it.

3. Install ROS Tools in Container
---------------------------------
Once inside the container, install the tools for image extraction and video conversion:

.. code-block:: bash
   :class: code-block-green

   apt update
   apt install -y ros-noetic-image-view ffmpeg

To persist the ROS environment across sessions:

.. code-block:: bash
   :class: code-block-green

   echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc
   source ~/.bashrc

4. Check ROS Bag Info
---------------------
Use `rosbag info` to inspect the file and confirm the image topic:

.. code-block:: bash
   :class: code-block-green

   rosbag info /rosbag_data/your_file.bag

Look for the correct topic such as `/camera/image_raw`.

5. Start ROS Core and Play Bag File
-----------------------------------
In **Terminal #1** (Docker container):

.. code-block:: bash
   :class: code-block-green

   roscore

In **Terminal #2** (another Docker terminal):

.. code-block:: bash
   :class: code-block-green

   rosbag play /rosbag_data/your_file.bag --clock

6. Extract Images from ROS Bag
------------------------------
In **Terminal #3** (same Docker container), create output folder:

.. code-block:: bash
   :class: code-block-green

   mkdir -p /rosbag_data/output_images

Run the image extraction tool:

.. code-block:: bash
   :class: code-block-green

   rosrun image_view extract_images \
     _filename_format:=frame%04d.jpg \
     image:=/camera/image_raw \
     _sec_per_frame:=0.0 \
     _output_folder:=/rosbag_data/output_images

This will save all frames from the `.bag` file as images.

7. Convert Extracted Images to Video
------------------------------------
Use `ffmpeg` to convert extracted frames into a video:

.. code-block:: bash
   :class: code-block-green

   cd /rosbag_data/output_images
   ffmpeg -framerate 10 -i frame%04d.jpg -c:v libx264 -pix_fmt yuv420p output_video.mp4

This creates `output_video.mp4` from the extracted frames.

8. Copy Video to Host System
----------------------------
To copy the video file from the container to your host macOS system:

In a new macOS terminal, find the container ID:

.. code-block:: bash
   :class: code-block-green

   docker ps

Then use:

.. code-block:: bash
   :class: code-block-green

   docker cp ros_container:/rosbag_data/output_images/output_video.mp4 ~/Desktop/

This copies the video to your Desktop.