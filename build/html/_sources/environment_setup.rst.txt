Environment Setup
=================

1 - Check Python Installation
-------------------------------

Before setting up your environment, ensure that Python 3 is properly installed on your system.

To check the Python version, run the following command in your terminal:

.. code-block:: bash
   :class: code-block-green

   python3 --version

If Python is installed, you should see output similar to this:

.. code-block:: bash
   :class: code-block-green

   Python 3.10.12

If you receive an error, Python is not installed. In that case, download and install it from the official Python website:

`Download Python <https://www.python.org/downloads/>`_

2 - Create a Virtual Environment
----------------------------------

A virtual environment helps isolate your project's dependencies from the global Python installation, keeping your setup clean and manageable.

To create a virtual environment, open your terminal **inside your project folder** and run:

.. code-block:: bash
   :class: code-block-green

   python3 -m venv venv

This command will generate a folder named ``venv`` containing all necessary files for the isolated environment.

After running it, check that a ``venv`` folder has appeared in your project directory:

.. code-block:: bash
   :class: code-block-green

   ls

Expected output:

.. code-block:: bash
   :class: code-block-green

   venv

.. note::

   If you already have a ``venv`` folder, you can skip this step.

3 - Activate the Virtual Environment
--------------------------------------

After creating the virtual environment, you need to **activate it** in order to use the isolated Python environment for your project.

This step is **crucial** because any Python packages you install after activation will stay inside the virtual environment, keeping your system Python untouched and preventing version conflicts.

Activation steps differ slightly depending on your operating system:

**- For macOS or Linux users, run this command:

.. code-block:: bash
   :class: code-block-green

   source venv/bin/activate

**- For Windows users using Command Prompt (cmd.exe)**, run:

.. code-block:: bash
   :class: code-block-green

   venv\Scripts\activate

**- For Windows users using PowerShell**, use:

.. code-block:: bash
   :class: code-block-green

   .\venv\Scripts\Activate.ps1

Once the environment is activated, your terminal prompt will change to show the name of the virtual environment, like this:

.. code-block:: bash
   :class: code-block-green

   (venv) your-computer:project-folder$

This prefix ``(venv)`` confirms that the environment is now active.

.. note::

    You must activate the environment every time you open a new terminal before working on your project.

   If you forget to activate it, packages may be installed globally or not found at all.

4 - Install Dependencies from requirements.txt
------------------------------------------------

Once your virtual environment is activated, install all the required Python packages directly from the provided `requirements.txt` file. This ensures consistent dependencies across systems.

To do so, run:

.. code-block:: bash
   :class: code-block-green

   pip install -r requirements.txt

This command reads the list of required packages from `requirements.txt` and installs them all at once.

If you face any permission-related issues, try adding the `--no-cache-dir` flag:

.. code-block:: bash
   :class: code-block-green

   pip install --no-cache-dir -r requirements.txt

.. note::

    Make sure the `requirements.txt` file is located in the **root directory** of your project. If it's in a subfolder, adjust the path accordingly.

Once installed, you’re ready to proceed with documentation setup and code execution.

5 - Setting Up Docker for ROS Bag Playback
--------------------------------------------

To ensure compatibility and isolate system dependencies, we use Docker for running ROS tools like ``roscore``, ``rosbag``, and ``image_view``. This allows anyone to extract images from ``.bag`` files and convert them into video format without installing ROS directly on the host system.

 **What Is Docker?**

Docker is a containerization platform that lets you package applications and their dependencies together. For this project, Docker allows you to run ROS Noetic (Ubuntu 20.04) in an isolated environment.

5.1 - Check if Docker Is Installed
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Run the following command in the terminal to check if Docker is already installed:

.. code-block:: bash
   :class: code-block-green

   docker --version

If Docker is not installed, download and install it from:  
`https://www.docker.com/products/docker-desktop`

5.2 - Verify Docker Service
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Ensure the Docker service is running:

.. code-block:: bash
   :class: code-block-green

   docker info

If this command fails, launch **Docker Desktop** manually from Applications or the search bar.

5.3 - Pull the ROS Noetic Image
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Download the official ROS Noetic image (Ubuntu 20.04):

.. code-block:: bash
   :class: code-block-green

   docker pull ros:noetic

This step might take a few minutes depending on your internet speed.

5.4 - Run a Container with Mounted External Drive
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Assuming your ``.bag`` files are stored in ``/Volumes/One_Touch``, mount this path into the Docker container as ``/rosbag_data``:

.. code-block:: bash
   :class: code-block-green

   docker run -it --name ros_container \
     --mount type=bind,source=/Volumes/One_Touch,target=/rosbag_data \
     ros:noetic

This launches a container named ``ros_container`` and mounts your external hard drive into it.

5.5 - Inside Docker: Install Required ROS Tools
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Once inside the container (you’ll see a root shell), install the necessary tools for image extraction and video conversion:

.. code-block:: bash
   :class: code-block-green

   apt update
   apt install -y ros-noetic-image-view ffmpeg

You can also make the ROS environment load automatically in every new session:

.. code-block:: bash
   :class: code-block-green

   echo "source /opt/ros/noetic/setup.bash" >> ~/.bashrc
   source ~/.bashrc

5.6 - Verify ROS Installation
^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

Check that ROS is correctly installed by running the following command inside the container:

.. code-block:: bash
   :class: code-block-green

   roscore

You should see the ROS master node start up successfully without any errors. This confirms that your ROS environment is properly configured and ready for use.

.. code-block:: text
   :class: code-block-green

   ... logging to /root/.ros/log/...
   started roslaunch server http://localhost:XXXXX/
   ros_comm version 1.15.X
   ...