Requirements
============

This section provides the complete list of Python libraries, package versions, and system tools required to run the distance-angle estimation and ROS-to-video pipeline.

---

1. Python Version
-----------------

The codebase is tested with:

- Python 3.10+

To check your Python version:

.. code-block:: bash
   :class: code-block-green

   python3 --version

---

2. Virtual Environment Setup
----------------------------

Before installing packages, it's recommended to create a virtual environment:

.. code-block:: bash
   :class: code-block-green

   python3 -m venv venv
   source venv/bin/activate

---

3. Required Python Packages
---------------------------

Install the following Python packages using `pip`:

.. code-block:: bash
   :class: code-block-green

   pip install ultralytics opencv-python numpy pandas plotly scipy

To save these in `requirements.txt`:

.. code-block:: bash
   :class: code-block-green

   pip freeze > requirements.txt

---

4. Docker for ROS Bag Processing
--------------------------------

Ensure Docker is installed and running. Pull the ROS image used for bag conversion:

.. code-block:: bash
   :class: code-block-green

   docker pull osrf/ros:noetic-desktop-full

Check Docker is working:

.. code-block:: bash
   :class: code-block-green

   docker --version

---

5. ROS Inside Docker
--------------------

No native ROS installation is needed on the host. All ROS-related tasks (bag play, image extraction) run inside the Docker container.

Mount the external disk using:

.. code-block:: bash
   :class: code-block-green

   docker run -it --name ros_container \
     --mount type=bind,source=/Volumes/One_Touch,target=/rosbag_data \
     osrf/ros:noetic-desktop-full

---

6. Optional (for developers)
----------------------------

For linting and development:

.. code-block:: bash
   :class: code-block-green

   pip install black isort flake8

---

 Purpose of `requirements.rst`

- Helps **you or any user** recreate the same environment.
- Keeps the setup **clean, version-controlled, and OS-independent**.
- Ensures the Docker+Python pipeline runs end-to-end without manual guesswork.

---

Would you like me to generate the full `.rst` file now named `requirements.rst` using all your formatting rules?