from ultralytics import YOLO

camera1_index = '' # Input your camera

model = YOLO('yolov8n-pose.pt')

results = model(source=camera1_index, stream=True, show=True, conf=0.3)
