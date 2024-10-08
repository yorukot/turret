import time
import cv2
import torch
import zmq
import numpy as np
from ultralytics import YOLO

device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
model = YOLO("../model/yolov8n-pose.pt", verbose=False)

context = zmq.Context()
socket = context.socket(zmq.SUB)
socket.connect("tcp://localhost:5555")

socket.setsockopt_string(zmq.SUBSCRIBE, "camera_0")
socket.setsockopt_string(zmq.SUBSCRIBE, "camera_2")
socket.setsockopt_string(zmq.SUBSCRIBE, "camera_4")
socket.setsockopt_string(zmq.SUBSCRIBE, "camera_6")

while True:
    try:
        topic = socket.recv_string()
        image_bytes = socket.recv()
    except ValueError as e:
        print(f"Socket解析錯誤: {e}")
        continue;


    # 假設時間戳固定為13個字節長
    timestamp_size = 15
    image_data = image_bytes[:-timestamp_size]
    timestamp_bytes = image_bytes[-timestamp_size:]
    try:
        timestamp = float(timestamp_bytes.decode('utf-8'))
    except ValueError as e:
        print(f"時間戳解析錯誤: {e}")
        continue;
        
    current_time = time.time()
    time_difference = current_time - timestamp  # 計算超過的時間

    if time_difference > 0.1:
        print(f"警告: 圖像 {topic} 已經過時，超過的時間為 {time_difference:.2f} 秒")
        continue

    nparr = np.frombuffer(image_bytes, np.uint8)
    frame = cv2.imdecode(nparr, cv2.IMREAD_COLOR)

    results = model(frame)
    annotated_frame = results[0].plot()

    cv2.imshow(f"Received - {topic}", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cv2.destroyAllWindows()
