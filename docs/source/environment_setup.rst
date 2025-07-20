
Environment Setup
=================

This section outlines the steps to set up the environment for running the full machine learning pipeline, including Python dependencies and Docker-based ROS bag conversion.

1. Check Python Installation
----------------------------
Ensure Python 3 is installed:

.. code-block:: bash
   :class: code-block-green

   python3 --version

If not installed, download from https://www.python.org/downloads/

2. Create a Virtual Environment
-------------------------------
Use `venv` to isolate dependencies:

.. code-block:: bash
   :class: code-block-green

   python3 -m venv venv

Check that a `venv` folder appears:

.. code-block:: bash
   :class: code-block-green

   ls

Expected output should include:

.. code-block:: none

   venv/

3. Activate the Virtual Environment
-----------------------------------
Depending on OS:

- macOS/Linux:

  .. code-block:: bash
     :class: code-block-green

     source venv/bin/activate

- Windows (cmd):

  .. code-block:: bash
     :class: code-block-green

     venv\Scripts\activate

- Windows (PowerShell):

  .. code-block:: bash
     :class: code-block-green

     .\venv\Scripts\Activate.ps1

4. Install Required Python Packages
-----------------------------------
Use the `requirements.txt` file:

.. code-block:: bash
   :class: code-block-green

   pip install -r requirements.txt

If facing issues:

.. code-block:: bash
   :class: code-block-green

   pip install --no-cache-dir -r requirements.txt

5. Docker Setup for ROS Bag Conversion
--------------------------------------

5.1 Check Docker Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash
   :class: code-block-green

   docker --version

If not installed, download Docker Desktop: https://www.docker.com/products/docker-desktop

5.2 Verify Docker is Running
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash
   :class: code-block-green

   docker info

5.3 Pull ROS Noetic Docker Image
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash
   :class: code-block-green

   docker pull ros:noetic

5.4 Mount External Drive into Docker Container
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Assuming your ROS bag files are in `/Volumes/One_Touch`:

.. code-block:: bash
   :class: code-block-green

   docker run -it --name ros_container \
     --mount type=bind,source=/Volumes/One_Touch,target=/rosbag_data \
     ros:noetic

5.5 Install ROS Tools Inside Container
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash
   :class: code-block-green

   apt update
   apt install -y ros-noetic-image-view ffmpeg

Make ROS auto-load:

.. code-block:: bash
   :class: code-block-green

   echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc
   source ~/.bashrc

5.6 Verify ROS Installation
~~~~~~~~~~~~~~~~~~~~~~~~~~~

.. code-block:: bash
   :class: code-block-green

   roscore

You should see the ROS master node running.

Requirements Summary
--------------------

- Python 3.10+
- Virtual environment (`venv`)
- Required packages:

.. code-block:: bash
   :class: code-block-green

   pip install ultralytics opencv-python numpy pandas plotly scipy

- Docker installed and running:

.. code-block:: bash
   :class: code-block-green

   docker pull osrf/ros:noetic-desktop-full

- No native ROS install required
- Optional developer tools:

.. code-block:: bash
   :class: code-block-green

   pip install black isort flake8

Purpose of this Setup
---------------------

- Reproducible, isolated setup
- Clean dependency management
- OS-independent execution
- Enables Docker-based ROS workflows

Ready to proceed to the next module after environment is set.