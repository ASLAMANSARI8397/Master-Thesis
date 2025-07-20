.. _data_preprocessing:

Data Preprocessing
===================

This section covers all preprocessing steps required to prepare the dataset for training and evaluation. It includes directory structure setup, annotation strategies, image normalization, frame extraction, and augmentations.

1 - Dataset Structure and Directory Layout
-------------------------------------------
To maintain consistency and scalability, the dataset is organized into the following structure:

::

  project_folder/
  ├── data/
  │   ├── images/        # All raw frames or extracted images
  │   ├── labels/        # Corresponding YOLO-format label files
  │   ├── val/           # Validation images + labels
  │   └── test/          # Optional test set
  └── dataset.yaml       # Dataset configuration file for YOLOv8

All label files follow the YOLO annotation format:

::

  <class_id> <x_center> <y_center> <width> <height>

All coordinates are normalized (between 0 and 1).

2 - Annotation Using LabelMe
------------------------------
LabelMe was chosen for manual annotation due to its ease of use and support for YOLO format conversion.

To annotate:

1. Open LabelMe GUI.
2. Draw bounding boxes over people and robots.
3. Save annotations in JSON format.
4. Use a script to convert JSON files to YOLO text files.

Example conversion snippet:

.. code-block:: bash

   python labelme2yolo.py --input ./annotations --output ./data/labels

3 - Image Normalization and Resizing
-------------------------------------
Before training, images are resized to match the YOLOv8 input size (e.g., 640x640). This ensures consistent model performance.

.. code-block:: python

   import cv2
   img = cv2.imread('image.jpg')
   img_resized = cv2.resize(img, (640, 640))
   img_normalized = img_resized / 255.0

4 - Frame Extraction from Video
--------------------------------
If starting from video data (e.g., from ROS bag conversion), extract frames at regular intervals using OpenCV:

.. code-block:: python

   import cv2
   vidcap = cv2.VideoCapture('video.mp4')
   count = 0
   success, image = vidcap.read()
   while success:
       if count % 15 == 0:
           cv2.imwrite(f"data/images/frame_{count}.jpg", image)
       success, image = vidcap.read()
       count += 1

This avoids redundancy and ensures temporal spacing in your training data.

5 - Data Augmentation Techniques
---------------------------------
To improve generalization, various augmentations are applied using OpenCV and NumPy:

- Horizontal flip
- Gamma correction
- Brightness and contrast adjustment
- Rotation (if needed)

Example: Horizontal flip and gamma correction

.. code-block:: python

   import numpy as np
   flipped = cv2.flip(img, 1)
   gamma = 1.5
   table = np.array([(i / 255.0) ** gamma * 255 for i in np.arange(0, 256)]).astype("uint8")
   corrected = cv2.LUT(img, table)

6 - Data Validation
--------------------
A Python script was written to ensure:

- Every image has a matching label
- No empty label files
- All label files follow YOLO format (5 values per line)

.. code-block:: python

   import os
   for file in os.listdir("data/images"):
       label_file = file.replace(".jpg", ".txt")
       if not os.path.exists(f"data/labels/{label_file}"):
           print("Missing label:", label_file)

This ensures training stability and accurate evaluation.