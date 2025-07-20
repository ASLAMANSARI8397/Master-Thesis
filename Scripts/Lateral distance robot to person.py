import cv2
import numpy as np
import math
import csv
import os
import pandas as pd
import plotly.express as px
from ultralytics import YOLO
from scipy.spatial import distance as dist

# ----------------------------- #
# 1. Centroid Tracker Class
# ----------------------------- #
class CentroidTracker:
    def __init__(self, max_disappeared=15):
        self.next_object_id = 0
        self.objects = {}
        self.disappeared = {}
        self.max_disappeared = max_disappeared

    def register(self, centroid):
        self.objects[self.next_object_id] = centroid
        self.disappeared[self.next_object_id] = 0
        self.next_object_id += 1

    def deregister(self, object_id):
        del self.objects[object_id]
        del self.disappeared[object_id]

    def update(self, input_centroids):
        if len(input_centroids) == 0:
            for object_id in list(self.disappeared.keys()):
                self.disappeared[object_id] += 1
                if self.disappeared[object_id] > self.max_disappeared:
                    self.deregister(object_id)
            return self.objects

        if len(self.objects) == 0:
            for centroid in input_centroids:
                self.register(centroid)
        else:
            object_ids = list(self.objects.keys())
            object_centroids = list(self.objects.values())

            D = dist.cdist(np.array(object_centroids), input_centroids)
            rows = D.min(axis=1).argsort()
            cols = D.argmin(axis=1)[rows]

            used_rows = set()
            used_cols = set()

            for row, col in zip(rows, cols):
                if row in used_rows or col in used_cols:
                    continue
                object_id = object_ids[row]
                self.objects[object_id] = input_centroids[col]
                self.disappeared[object_id] = 0
                used_rows.add(row)
                used_cols.add(col)

            unused_rows = set(range(D.shape[0])) - used_rows
            for row in unused_rows:
                object_id = object_ids[row]
                self.disappeared[object_id] += 1
                if self.disappeared[object_id] > self.max_disappeared:
                    self.deregister(object_id)

            unused_cols = set(range(D.shape[1])) - used_cols
            for col in unused_cols:
                self.register(input_centroids[col])

        return self.objects

# ----------------------------- #
# 2. Setup
# ----------------------------- #

robot_model = YOLO("Models/robot.pt")
person_model = YOLO("Models/yolov8n.pt")

# Input source: Choose only one
cap = cv2.VideoCapture("Input/5.mp4")    # ← Use this line for video file input
# cap = cv2.VideoCapture(0)              # ← Use this line for webcam input (live)

if not cap.isOpened():
    raise RuntimeError("Could not open video")

FRAME_WIDTH = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
FRAME_HEIGHT = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fps = cap.get(cv2.CAP_PROP_FPS)

KNOWN_ROBOT_WIDTH_CM = 30.0
os.makedirs("Output", exist_ok=True)
csv_file = "Output/robot lateral tracking.csv"
tracking_data = []

tracker = CentroidTracker()

def angle_deg(o, p):
    return (math.degrees(math.atan2(p[1]-o[1], p[0]-o[0])) + 360) % 360

def update_cm_per_pixel(prev_ratio, bbox_px_w, alpha=0.1):
    if bbox_px_w == 0:
        return prev_ratio
    new_ratio = KNOWN_ROBOT_WIDTH_CM / bbox_px_w
    return new_ratio if prev_ratio is None else (1 - alpha) * prev_ratio + alpha * new_ratio

ARM_DEG = 65
LEFT_LIMIT, RIGHT_LIMIT = 90 - ARM_DEG, 90 + ARM_DEG
ARM_LEN = 1000

frame_idx = 0
ratio_cm = None
last_saved_second = -1

print("✅ Starting robot-centered lateral distance detection...")

# ----------------------------- #
# 3. Main Loop
# ----------------------------- #
while True:
    ok, frame = cap.read()
    if not ok:
        break
    frame_idx += 1
    t_sec = cap.get(cv2.CAP_PROP_POS_MSEC) / 1000.0
    current_second = int(t_sec)

    robot_box = None
    for r in robot_model(frame, verbose=False):
        for b in r.boxes:
            if r.names[b.cls[0].item()] == "robot":
                robot_box = b.xyxy[0].cpu().numpy().astype(int)
                break
        if robot_box is not None:
            break

    if robot_box is None:
        cv2.imshow("Robot centered tracking", frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
        continue

    x1, y1, x2, y2 = robot_box
    origin = ((x1 + x2) // 2, (y1 + y2) // 2)
    ratio_cm = update_cm_per_pixel(ratio_cm, x2 - x1)

    cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 0), 2)
    cv2.putText(frame, "Robot", (x1, y1 - 10),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 0, 0), 2)

    left_pt = (int(origin[0] + ARM_LEN * math.cos(math.radians(90 - ARM_DEG))),
               int(origin[1] + ARM_LEN * math.sin(math.radians(90 - ARM_DEG))))
    right_pt = (int(origin[0] + ARM_LEN * math.cos(math.radians(90 + ARM_DEG))),
                int(origin[1] + ARM_LEN * math.sin(math.radians(90 + ARM_DEG))))

    vmask = np.zeros_like(frame)
    cv2.fillPoly(vmask, [np.array([origin, left_pt, right_pt])], (120, 120, 120))
    frame = cv2.addWeighted(frame, 1, vmask, 0.5, 0)
    cv2.line(frame, origin, left_pt, (0, 255, 0), 2)
    cv2.line(frame, origin, right_pt, (0, 255, 0), 2)

    detected_centroids = []
    bbox_map = {}

    for r in person_model(frame, verbose=False):
        for b in r.boxes:
            if r.names[b.cls[0].item()] != "person":
                continue
            px1, py1, px2, py2 = b.xyxy[0].cpu().numpy().astype(int)
            pcx, pcy = (px1 + px2) // 2, (py1 + py2) // 2
            ang = angle_deg(origin, (pcx, pcy))
            if LEFT_LIMIT <= ang <= RIGHT_LIMIT:
                continue
            detected_centroids.append((pcx, pcy))
            bbox_map[(pcx, pcy)] = (px1, py1, px2, py2)

    objects = tracker.update(np.array(detected_centroids))
    detected_in_this_frame = []

    for object_id, (pcx, pcy) in objects.items():
        if (pcx, pcy) not in bbox_map:
            continue

        px1, py1, px2, py2 = bbox_map[(pcx, pcy)]
        lat_px = abs(pcx - origin[0])
        lat_cm = int(lat_px * ratio_cm) if ratio_cm else lat_px
        quadrant = "Right" if pcx >= origin[0] else "Left"

        cv2.rectangle(frame, (px1, py1), (px2, py2), (0, 255, 0), 2)
        cv2.line(frame, origin, (pcx, pcy), (0, 255, 0), 2)
        cv2.putText(frame, f"ID:{object_id} {quadrant}", (px1, py1 - 12),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), 2)
        cv2.putText(frame, f"Lat:{lat_cm}cm", (px1, py1 + 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.55, (0, 255, 0), 2)

        detected_in_this_frame.append({
            "Timestamp (s)": round(t_sec, 2),
            "ID": object_id,
            "Quadrant": quadrant,
            "Lateral Distance (cm)": lat_cm
        })

    if current_second != last_saved_second:
        if detected_in_this_frame:
            tracking_data.extend(detected_in_this_frame)
        else:
            tracking_data.append({
                "Timestamp (s)": round(t_sec, 2),
                "ID": None,
                "Quadrant": None,
                "Lateral Distance (cm)": None
            })
        last_saved_second = current_second

    cv2.imshow("Robot centered tracking", frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# ----------------------------- #
# 4. Save Results
# ----------------------------- #
cap.release()
cv2.destroyAllWindows()

df = pd.DataFrame(tracking_data)
df.to_csv(csv_file, index=False)
print(f"✅ Tracking data saved to {csv_file}!")

if not df.empty:
    def danger_color(dist):
        if pd.isna(dist):
            return 'Gray'
        elif dist <= 10:
            return 'Red'
        elif dist <= 20:
            return 'Orange'
        else:
            return 'Green'

    df['Danger Level'] = df['Lateral Distance (cm)'].apply(danger_color)

    fig = px.scatter(
        df,
        x="Timestamp (s)",
        y="Lateral Distance (cm)",
        color="Danger Level",
        color_discrete_map={"Red": "red", "Orange": "orange", "Green": "green", "Gray": "gray"},
        hover_data=["ID", "Quadrant"],
        title="Lateral Distance from Robot Over Time"
    )
    fig.update_layout(
        xaxis_title="Time (Seconds)",
        yaxis_title="Lateral Distance (cm)",
        hovermode="closest"
    )
    fig.show()
else:
    print("❗ No valid data to plot.")