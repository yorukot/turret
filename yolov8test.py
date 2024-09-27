import cv2
import time
from ultralytics import YOLO
import torch

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")

model = YOLO("yolov8n-pose.pt")

camera_sources = [0]

caps = [cv2.VideoCapture(src) for src in camera_sources]

# Store timestamps for each camera
timestamps = [0] * len(camera_sources)


def process_frame(frame):
    results = model(frame)

    annotated_frame = results[0].plot()
    
    coords = results[0]
    print(coords)
    return annotated_frame, coords


while True:
    for i, cap in enumerate(caps):
        ret, frame = cap.read()
        if not ret:
            print(f"無法從攝像頭 {i} 獲取影像")
            continue

        current_time = time.time()
        if timestamps[i] != 0:
            time_interval = current_time - timestamps[i]
            print(f"Camera {i} - Time interval: {time_interval:.3f} seconds")
        timestamps[i] = current_time

        annotated_frame, coords = process_frame(frame)

        cv2.imshow(f"Camera {i}", annotated_frame)
        if i == 3:
            "a"

    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

for cap in caps:
    cap.release()
cv2.destroyAllWindows()