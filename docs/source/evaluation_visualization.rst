.. _evaluation_visualization:

Evaluation and Visualization
===========================

This module handles the visual analysis and graphical validation of the distance-angle estimation logic. After extracting the spatial data (person ID, distance, and angle per frame), the data is exported to a CSV and then visualized using Plotly.

Color-coded danger zones and real-time tracking visualizations are generated to ensure spatial safety analysis is both interpretable and actionable.

1. CSV Output Structure and Logging Logic
----------------------------------------

During frame-by-frame processing, valid detections are logged into a CSV file with the following columns:

- `timestamp`: Frame number or time-based key
- `person_id`: Unique identifier for each tracked person
- `distance_cm`: Distance from camera to person
- `angle_deg`: Horizontal angle from image center

Example code snippet:

.. code-block:: python
   :class: code-block-green

   import pandas as pd

   csv_log = []
   csv_log.append({
       "timestamp": frame_idx,
       "person_id": person_id,
       "distance_cm": final_distance,
       "angle_deg": angle
   })
   df = pd.DataFrame(csv_log)
   df.to_csv("output_data.csv", index=False)

This file serves as the input to the interactive visualization phase.

2. Plotly Visualization with Danger Zones
----------------------------------------

The system uses Plotly Express to create a dynamic scatter plot of person location over time:

- X-axis: angle_deg
- Y-axis: distance_cm
- Color: Encodes proximity-based safety zone

Zone coloring logic:

- Red: distance < 100 cm (Danger zone)
- Yellow: 100-200 cm (Caution)
- Green: > 200 cm (Safe)

.. code-block:: python
   :class: code-block-green

   def classify_zone(distance):
       if distance < 100:
           return "Danger"
       elif distance < 200:
           return "Caution"
       else:
           return "Safe"

   df["zone"] = df["distance_cm"].apply(classify_zone)

   import plotly.express as px

   fig = px.scatter(
       df,
       x="angle_deg",
       y="distance_cm",
       color="zone",
       hover_data=["timestamp", "person_id", "distance_cm", "angle_deg"],
       title="Distance vs Angle (Color-Coded Zones)"
   )
   fig.show()

3. Hover Tooltips for Tracking Analysis
--------------------------------------

Each point in the Plotly chart includes hover tooltips with:

- Person ID
- Frame timestamp
- Distance (in cm)
- Angle (in degrees)

This enables frame-wise tracking of an individual’s position over time and highlights who entered the danger zone.

.. code-block:: python
   :class: code-block-green

   hover_data=["timestamp", "person_id", "distance_cm", "angle_deg"]

This feature makes the analysis extremely intuitive and interpretable even for non-technical stakeholders.

4. Smoothing Logic with Moving Average
--------------------------------------

To reduce frame-by-frame noise and improve clarity, the system applies a moving average smoothing filter:

- Smooths jitter in distance and angle readings
- Helps highlight true entry/exit trends from the danger zone

.. code-block:: python
   :class: code-block-green

   df["distance_smoothed"] = df["distance_cm"].rolling(window=5).mean()
   df["angle_smoothed"] = df["angle_deg"].rolling(window=5).mean()

   fig = px.scatter(
       df,
       x="angle_smoothed",
       y="distance_smoothed",
       color="zone",
       hover_data=["timestamp", "person_id"]
   )
   fig.show()

The smoothing window (window=5) can be tuned based on the frame rate.

5. Summary of Visualization Logic
---------------------------------

This module provides the final visual feedback layer for the system:

- CSV export from real-time spatial logic
- Color-coded danger zone classification
- Interactive Plotly plots for spatial insight
- Hover tooltips for per-frame analysis
- Optional smoothing for better trend clarity

This visual layer is essential for stakeholders to understand spatial safety in complex environments, especially in multi-human and robot-interacting systems.