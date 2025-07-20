Distance and Angle Estimation
=============================

This section explains the complete logic behind estimating both camera-to-person distance and person-to-robot spatial angle using RealSense video input. The system uses two YOLO models simultaneously to detect humans and robots in each frame, enabling real-time spatial awareness.

All steps are implemented using Python, OpenCV, NumPy, and a depth data file extracted from RealSense camera (.npy). This module is standalone and does not require any webcam or ROS install.

1. Dual YOLO Model Architecture
-------------------------------
To differentiate between people and robots, the system runs two YOLOv8 models in parallel:

- One model trained to detect person class (e.g., yolov8n.pt)
- One fine-tuned YOLO model trained to detect robots (e.g., robot.pt)

Each model processes the same RealSense video frame in every iteration.

.. code-block:: python

   from ultralytics import YOLO
   person_model = YOLO("yolov8n.pt")  # Detects humans
   robot_model = YOLO("robot.pt")      # Detects robots

2. RealSense Video Input Handling
----------------------------------
Instead of a webcam, this module uses a pre-recorded RealSense video file (e.g., .mp4) and a corresponding depth map in `.npy` format extracted frame-wise.

.. code-block:: python

   import cv2
   import numpy as np
   cap = cv2.VideoCapture("input_video.mp4")
   depth_data = np.load("depth_array.npy")  # Shape: (N, H, W)

Each frame from cap.read() is paired with a depth map from the .npy file for accurate spatial estimation.

3. Camera-to-Person Distance Estimation
----------------------------------------
To estimate the distance from the camera to a person:

- Use the bounding box center (cx, cy) of each detected person.
- Extract the depth value from the RealSense .npy array at that pixel.
- Ignore any zero or extreme values using filtering.

.. code-block:: python

   cx = int((x1 + x2) / 2)
   cy = int((y1 + y2) / 2)
   raw_distance = depth_data[frame_idx][cy][cx]
   if 20 < raw_distance < 400:  # cm
       final_distance = raw_distance

The result is a stable, per-person distance from the camera.

4. Angle Estimation Logic
--------------------------
The horizontal angle between the detected person and the camera center is computed using focal length and pixel offset.

The formula:

.. math::

   \theta = \arctan\left( \frac{x - c_x}{f_x} \right)

Where:
- :math:`x` is the x-coordinate of bounding box center
- :math:`c_x` is the image center in x-axis (frame.shape[1] / 2)
- :math:`f_x` is focal length in pixels (RealSense: e.g., 604.8672)

.. code-block:: python

   fx = 604.8672
   image_center_x = frame.shape[1] // 2
   angle = np.arctan((cx - image_center_x) / fx) * (180 / np.pi)

This gives angle in degrees, with negative = left, positive = right.

5. Robot Localization using Person ID
--------------------------------------
Once both persons and robots are detected in a frame:

- Assign each detection a unique ID using position tracking.
- Map each robot to the nearest person in angle space (same frame).
- Calculate the relative angle and distance between person and robot.

.. code-block:: python

   from scipy.spatial import distance
   for robot in robots:
       r_angle = robot["angle"]
       nearest_person = min(persons, key=lambda p: abs(p["angle"] - r_angle))
       dist_cm = distance.euclidean(
           (robot["cx"], robot["cy"]), (nearest_person["cx"], nearest_person["cy"])
       )
       if dist_cm < MAX_VALID_DISTANCE:
           # Log person-robot proximity
           spatial_map.append({
               "frame": frame_idx,
               "person_id": nearest_person["id"],
               "robot_id": robot["id"],
               "angle": r_angle,
               "distance": dist_cm
           })

This logic allows continuous tracking of person-robot spatial relations.

6. Filtering and Validation Rules
----------------------------------
To improve real-time usability, the following filtering steps are applied:

- Discard frames where no valid depth is found (depth == 0 or > 500cm).
- Filter out boxes that are too small or have abnormal aspect ratios.
- Frame skipping logic (frame_idx % 2 == 0) to reduce processing.

.. code-block:: python

   MIN_AREA = 1500
   for box in results:
       area = (x2 - x1) * (y2 - y1)
       ratio = (x2 - x1) / (y2 - y1 + 1e-6)
       if area < MIN_AREA or ratio < 0.2 or ratio > 2.5:
           continue  # Skip noisy boxes

This ensures only reliable detections are passed for distance-angle processing.