import cv2
import zmq
import numpy as np
import threading

def camera_thread(camera_index, socket):
    cap = cv2.VideoCapture(camera_index)
    while True:
        ret, frame = cap.read()
        if not ret:
            print(f"無法從攝像頭 {camera_index} 獲取影像")
            continue

        _, buffer = cv2.imencode('.jpg', frame)
        
        socket.send_string(f"camera_{camera_index}", zmq.SNDMORE)
        socket.send(buffer.tobytes())

def main():
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:5555")

    camera_sources = [0, 2, 4]  # 可以根據需要添加更多攝像頭
    threads = []

    for i in camera_sources:
        thread = threading.Thread(target=camera_thread, args=(i, socket))
        thread.start()
        threads.append(thread)

    # 主線程等待所有攝像頭線程結束
    for thread in threads:
        thread.join()

if __name__ == '__main__':
    main()