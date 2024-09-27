import cv2
import zmq
import numpy as np

context = zmq.Context()
socket = context.socket(zmq.PUB)
socket.bind("tcp://*:5555")

camera_sources = [0, 2, 4]
caps = [cv2.VideoCapture(src) for src in camera_sources]

while True:
    for i, cap in enumerate(caps):
        ret, frame = cap.read()
        if not ret:
            print(f"無法從攝像頭 {i} 獲取影像")
            continue

        _, buffer = cv2.imencode('.jpg', frame)
        
        socket.send_string(f"camera_{i}", zmq.SNDMORE)
        socket.send(buffer.tobytes())


    if cv2.waitKey(1) & 0xFF == ord("q"):
        break

# 释放资源
for cap in caps:
    cap.release()
cv2.destroyAllWindows()