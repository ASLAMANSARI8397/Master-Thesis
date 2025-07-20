# 📘 Master Thesis – End-to-End Machine Learning Pipeline for Distance Estimation and Human-Robot Interaction in Autonomous Systems

This repository contains the complete implementation of my master's thesis project, which focuses on building a real-time person detection and distance estimation system using YOLOv8 and RealSense video data.

---

## 📂 Project Structure

```
project copy/
├── Models/            # YOLOv8 pretrained/custom models (e.g., yolov8n.pt, robot.pt)
├── Input/             # Input videos (e.g., RealSense recordings)
├── Output/            # Output videos, CSV logs, and Plotly visualizations
├── datasets/          # Labelled image dataset (after LabelMe annotations + YOLO conversion)
│   └── robot/
│       ├── images/train/
│       ├── images/val/
│       └── labels/
├── Scripts/           # Python scripts for detection, annotation, and tracking
├── docs/              # Sphinx-based documentation folder
├── requirements.txt   # All Python dependencies
```

---

## 🚀 Features

- YOLOv8-based object detection for both `person` and custom `robot`
- Real-time distance and angle estimation using bounding box + depth logic
- Multi-object ID tracking using centroid distance method
- Safety zone classification (green/yellow/red) based on proximity
- CSV export and interactive Plotly visualization
- ROS bag to video conversion support (with Docker)

---

## 🛠️ Setup Instructions

1. **Clone the repo:**

```bash
git clone https://github.com/ASLAMANSARI8397/Master-Thesis.git
cd Master-Thesis
```

2. **Create virtual environment:**

```bash
python3 -m venv .venv
source .venv/bin/activate  # macOS/Linux
```

3. **Install dependencies:**

```bash
pip install -r requirements.txt
```

---

## 🧠 Model Info

- `yolov8n.pt`: Pretrained on COCO for general objects (used for detecting people)
- `robot.pt`: Custom trained on robot dataset using YOLOv8

---

## 📊 Visual Outputs

- Detection overlays with ID, distance (cm), angle (deg)
- CSV log: timestamp, ID, distance, angle
- Plotly interactive graph for validation

---

## 📄 Documentation

Full Sphinx documentation is available in the `docs/` folder.

To build the HTML:

```bash
cd docs
make html
open build/html/index.html
```