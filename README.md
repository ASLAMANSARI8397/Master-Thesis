# Master-Thesis
End-to-End Machine Learning Pipeline for Distance Estimation and human-Robot Interaction in Autonomous Systems

🚀 Overview

This project presents a complete real-time pipeline for detecting humans and robots in video frames, estimating their distance from the camera and from each other, and classifying proximity risk. The system is designed for safety-critical human-robot interaction scenarios, where live video input is continuously analyzed to monitor spatial proximity and alert for dangerous conditions. It supports real-time deployment in indoor or controlled environments, such as educational robotics labs, research platforms, or experimental navigation systems, with modular support for RGB and depth-based sensing.

### ✨ Key Features

- YOLOv8-based object detection (supports `person` and `robot` classes)
- Distance estimation using either:
  - RealSense depth frames (if available), or
  - Focal length–based monocular calculation
- Multi-object tracking and unique ID assignment across frames
- Safety zone classification using color-coded proximity levels:
  - Green: Safe
  - Yellow: Caution
  - Red: High Risk
- Customizable frame skipping logic for efficient real-time inference
- CSV-based logging of timestamp, ID, distance (cm), and angle (deg)
- Interactive Plotly visualization for post-run evaluation

📁 **Directory Structure**

```
project/
├── model/                
│   └── yolov8.pt                 # Trained YOLOv8 model weights (fine-tuned)
│
├── input/                 
│   ├── videos/                   # Optional: sample video files for testing
│   └── frames/                   # RGB image frames captured from live feed
│
├── output/
│   ├── csv/                      # CSV logs with timestamp, ID, distance, angle, status
│   └── plots/                    # Interactive Plotly graphs generated from CSV
│
├── scripts/
│   ├── detection.py              # Core pipeline: detection + tracking + logging
│   ├── distance.py               # Distance and angle estimation logic
│   └── visualizer.py             # CSV to Plotly graph converter
│
├── requirements.txt             # pip freeze output
└── README.md                    # This file (overview, setup, usage)

```
### 🛠️ Installation

Ensure Python 3.8+ is installed on your system.

```bash
# Create a virtual environment
python -m venv venv
source venv/bin/activate        # On macOS/Linux
venv\Scripts\activate           # On Windows

# Install the required dependencies:
pip install -r requirements.txt
```

### ▶️ How to Run

**Run on a video file:**
```bash
python scripts/detection.py --video input/videos/sample.mp4
```

**Run on live webcam feed:**
```bash
python scripts/detection.py --webcam 0
```

### 📊 Sample Output

After running the pipeline, the system generates:

- A `.csv` file with the following structure:


```csv
timestamp    id   distance_cm  angle_deg   status
00:01.000    1    152          -12         Safe
00:01.500    2    98            5          High Risk
00:02.000    1    149          -10         Safe
...
```

- An interactive **Plotly visualization** showing:
  - Distance and angle over time for each tracked ID
  - Color-coded safety zones (Green, Yellow, Red)
  - Hover tooltips for ID, distance, angle, and timestamp

✅ Both output files (`CSV` and `Plotly HTML`) are saved in the `output/` folder automatically after each run.

### 📦 Dependencies

The project relies on the following core Python libraries and tools:

- `ultralytics` – YOLOv8 object detection framework
- `opencv-python` – image processing and video handling
- `numpy` – numerical operations and matrix manipulation
- `plotly` – interactive graph generation from CSV
- `pandas` – structured data handling and CSV logging
- `torch` – PyTorch backend for YOLOv8
- `matplotlib` – optional static graph support (used for debugging)
- `pyrealsense2` – Intel RealSense depth camera SDK (optional, for depth sensing)

To install all required packages:

```bash
pip install -r requirements.txt
```

> 📁 All dependencies are listed in the `requirements.txt` file located at the project folder.

---

### 👤 Author

**Aslam Ansari**  
M.ENG in Mechatronics and Robotics  
[Hochschule Schmalkalden]  
🔗 www.linkedin.com/in/mdaslamansari8

---




