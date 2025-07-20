Model Training
==============

This section explains in detail how the object detection model was trained for the distance and angle estimation system. The process includes dataset preparation, transfer learning using YOLOv8, configuration settings, training execution, and evaluation.

1 - Dataset Preparation and Configuration
-----------------------------------------
Before training, the dataset must be structured according to YOLO format:

- Images are stored in:
  - /images/train
  - /images/val
- Corresponding labels in:
  - /labels/train
  - /labels/val

Each label file is a `.txt` file containing bounding boxes and class IDs in YOLO format.

Create a configuration file called `dataset.yaml` with the following structure:

.. code-block:: yaml

   path: /absolute/path/to/dataset
   train: images/train
   val: images/val
   nc: 2
   names: ['person', 'robot']

Here:
- `nc` is the number of classes.
- `names` must match the class indices used during annotation.

2 - Model Selection and Transfer Learning Strategy
--------------------------------------------------
We use YOLOv8 (You Only Look Once version 8) from the `ultralytics` package for object detection due to its lightweight architecture and real-time performance.

Instead of training from scratch, transfer learning is applied using a pre-trained base model:

.. code-block:: bash
   :class: code-block-green

   yolo task=detect mode=train \
        model=robot.pt \
        data=dataset.yaml \
        epochs=50 \
        imgsz=640 \
        batch=16 \
        name=yolov8_robot_train

Here:
- `robot.pt` is the checkpoint trained on a similar robotics dataset.
- `dataset.yaml` provides training and validation splits.
- `imgsz` controls input resolution.
- `batch` is tuned based on available GPU memory.

3 - Training Environment Setup
------------------------------
Make sure you're running training inside a virtual environment with `ultralytics` installed.

Activate your environment and navigate to the training folder.
Use the following command to install the training library if not already present:

.. code-block:: bash
   :class: code-block-green

   pip install ultralytics

If GPU support is enabled, ensure CUDA drivers are installed. Training will auto-switch to GPU if available.

4 - Monitoring Training Metrics
-------------------------------
The training process outputs real-time metrics like:
- Box loss
- Class loss
- mAP@0.5
- Precision / Recall

After training, results will be available in the `runs/detect/yolov8_robot_train` folder.

To visualize training curves:

.. code-block:: bash
   :class: code-block-green

   tensorboard --logdir runs/detect

Open your browser at `http://localhost:6006` to view the metrics.

5 - Exporting the Trained Model
-------------------------------
Once training is complete, export the best model weights as follows:

.. code-block:: bash
   :class: code-block-green

   yolo export model=runs/detect/yolov8_robot_train/weights/best.pt format=onnx

This converts the PyTorch weights to ONNX for easier integration into ROS or other environments.

6 - Evaluate Model on Validation Data
-------------------------------------
To test the trained model on new data:

.. code-block:: bash
   :class: code-block-green

   yolo task=detect mode=val \
        model=runs/detect/yolov8_robot_train/weights/best.pt \
        data=dataset.yaml

You will receive evaluation metrics including mAP, precision, and recall.

This concludes the full training workflow for your real-time detection system.