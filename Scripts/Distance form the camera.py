import cv2
import numpy as np
import pandas as pd
import plotly.express as px
from ultralytics import YOLO
from collections import deque
from scipy.spatial import distance as dist

# Load YOLO model
model = YOLO("Models/yolov8n.pt")

# Camera calibration values
FOCAL_LENGTH_X = 604.8672  # fx
KNOWN_WIDTH = 45  # Average shoulder width in cm

# Thresholds
DISTANCE_THRESHOLD = 100
MAX_VALID_DISTANCE = 400

# Initialize
tracking_data = []
frame_skip = 2
fps = 30
saved_seconds = set()
smoothing_buffer = {}
buffer_size = 3

# Persistent tracking
class PersistentTracker:
    def __init__(self, max_disappeared=30, max_distance=100):
        self.next_id = 0
        self.tracked_objects = {}

    def update(self, detections, frame_number):
        if len(detections) == 0:
            for obj_id in list(self.tracked_objects.keys()):
                center, last_seen = self.tracked_objects[obj_id]
                if frame_number - last_seen > 30:
                    del self.tracked_objects[obj_id]
            return self.tracked_objects

        updated_objects = {}
        for detection in detections:
            x1, y1, x2, y2 = detection
            center = ((x1 + x2) // 2, (y1 + y2) // 2)

            matched_id = None
            min_distance = 100

            for obj_id, (prev_center, last_seen) in self.tracked_objects.items():
                d = dist.euclidean(center, prev_center)
                if d < min_distance:
                    min_distance = d
                    matched_id = obj_id

            if matched_id is not None:
                updated_objects[matched_id] = (center, frame_number)
                del self.tracked_objects[matched_id]
            else:
                updated_objects[self.next_id] = (center, frame_number)
                self.next_id += 1

        for obj_id, (prev_center, last_seen) in self.tracked_objects.items():
            if frame_number - last_seen <= 30:
                updated_objects[obj_id] = (prev_center, last_seen)

        self.tracked_objects = updated_objects
        return self.tracked_objects

tracker = PersistentTracker()

# ✅ Toggle input here
input_source = "Input/1.mp4"   # ← For video file input
#input_source = 0                 # ← For live webcam input

results = model.predict(
    source=input_source,
    conf=0.5,
    iou=0.45,
    classes=[0],
    stream=True
)

frame_count = 0
print("Press 'q' or 'ESC' to exit.")

for result in results:
    frame_count += 1
    if frame_count % frame_skip != 0:
        continue

    frame = result.orig_img
    if frame is None:
        break

    frame_height, frame_width = frame.shape[:2]
    detections = []

    for box in result.boxes:
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        detections.append((x1, y1, x2, y2))

    tracked_objects = tracker.update(detections, frame_count)
    video_time_sec = frame_count / fps
    current_second = int(video_time_sec)

    for obj_id, (center, last_seen) in tracked_objects.items():
        cx, cy = center

        closest_bbox = None
        min_dist = 1e9
        for (x1, y1, x2, y2) in detections:
            bbox_center = ((x1 + x2) // 2, (y1 + y2) // 2)
            d = dist.euclidean(center, bbox_center)
            if d < min_dist:
                min_dist = d
                closest_bbox = (x1, y1, x2, y2)

        if closest_bbox is None:
            continue

        x1, y1, x2, y2 = closest_bbox
        pixel_width = x2 - x1

        distance_to_camera = (KNOWN_WIDTH * FOCAL_LENGTH_X) / pixel_width if pixel_width > 0 else 0

        if obj_id not in smoothing_buffer:
            smoothing_buffer[obj_id] = deque(maxlen=buffer_size)
        smoothing_buffer[obj_id].append(distance_to_camera)
        smoothed = np.mean(smoothing_buffer[obj_id])

        # ✅ Apply Tolerance Logic
        if smoothed > 200:
            final_distance = smoothed * 1.5  # 50%
        elif smoothed > 100:
            final_distance = smoothed * 1.3  # 30%
        else:
            final_distance = smoothed * 1.25  # 25%
        final_distance = int(round(final_distance))

        # ✅ Angle
        angle = np.degrees(np.arctan2((cx - frame_width // 2), FOCAL_LENGTH_X))
        angle = int(round(angle))

        # ✅ Color logic
        if final_distance < DISTANCE_THRESHOLD:
            line_color = (0, 0, 255)
            box_color = (0, 0, 255)
        elif final_distance < 2 * DISTANCE_THRESHOLD:
            line_color = (0, 255, 255)
            box_color = (0, 255, 255)
        else:
            line_color = (255, 0, 0)
            box_color = (0, 255, 0)

        # ✅ Draw
        cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 2)
        cv2.circle(frame, (cx, cy), 5, box_color, -1)
        cv2.line(frame, (frame_width // 2, frame_height), (cx, cy), line_color, 2)
        cv2.putText(frame, f"ID:{obj_id} Angle: {angle} deg", (cx + 10, cy - 20),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, box_color, 2)
        cv2.putText(frame, f"Distance: {final_distance} cm", (cx + 10, cy + 10),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.5, box_color, 2)

        # ✅ Save CSV row
        if current_second not in saved_seconds:
            tracking_data.append({
                "Timestamp (s)": round(video_time_sec, 2),
                "ID": obj_id,
                "Angle (deg)": angle,
                "Distance to Camera (cm)": final_distance
            })
            saved_seconds.add(current_second)

    cv2.imshow("Tracking within 400cm", frame)
    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or key == 27:
        break

cv2.destroyAllWindows()

# ✅ Save CSV

df = pd.DataFrame(tracking_data)
df.to_csv("Output/distance from camera to person.csv", index=False)
print("✅ Tracking data saved to Output/tracking_data_below_400cm.csv!")

# ✅ Plot with Green–Orange–Red Zones
if not df.empty:
    def get_zone(distance):
        if distance < DISTANCE_THRESHOLD:
            return 'Danger (Red)'
        elif distance < 2 * DISTANCE_THRESHOLD:
            return 'Caution (Orange)'
        else:
            return 'Safe (Green)'

    df['Zone'] = df['Distance to Camera (cm)'].apply(get_zone)

    fig = px.scatter(
        df,
        x="Timestamp (s)",
        y="Distance to Camera (cm)",
        color="Zone",
        color_discrete_map={
            'Danger (Red)': 'red',
            'Caution (Orange)': 'orange',
            'Safe (Green)': 'green'
        },
        hover_data=["ID", "Angle (deg)"],
        title="Distance Over Time (Below 400cm Only)"
    )
    fig.update_layout(
        xaxis_title="Time (Seconds)",
        yaxis_title="Distance to Camera (cm)",
        hovermode="closest"
    )
    fig.show()
else:
    print("❗ No valid data to plot.")