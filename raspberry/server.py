import cv2
import zmq
import numpy as np
from ultralytics import YOLO

# 初始化 YOLO 模型
model = YOLO("yolov8n-pose.pt", verbose=False)

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5555")

socket.setsockopt_string(zmq.SUBSCRIBE, "camera_0")
socket.setsockopt_string(zmq.SUBSCRIBE, "camera_2")
socket.setsockopt_string(zmq.SUBSCRIBE, "camera_4")

while True:
    topic = socket.recv_string()
    image_bytes = socket.recv()

    nparr = np.frombuffer(image_bytes, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    results = model(frame)
    annotated_frame = results[0].plot()

    cv2.imshow(f"Received - {topic}", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
