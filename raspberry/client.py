import cv2
import zmq
import threading
import time

def camera_thread(camera_index, socket):
    cap = cv2.VideoCapture(camera_index)
    while True:
        ret, frame = cap.read()
        if not ret:
            print(f"無法從攝像頭 {camera_index} 獲取影像")
            continue

        # 將圖像編碼為JPEG格式
        _, buffer = cv2.imencode('.jpg', frame)
        
        # 發送圖像名稱（如 "camera_2"）和圖像數據
        socket.send_string(f"camera_{camera_index}", zmq.SNDMORE)

        # 獲取當前的時間戳，限制到小數點後兩位，並轉換為固定長度的字節格式
        timestamp = "{:.2f}".format(time.time()).zfill(15).encode('utf-8')[:15]
        # 發送圖像數據和時間戳
        socket.send(buffer.tobytes() + timestamp)
        time.sleep(1/30) # 15fps

def main():
    context = zmq.Context()
    socket = context.socket(zmq.PUB)
    socket.bind("tcp://*:5555")

    camera_sources = [0,2,4]  # 可以根據需要添加更多攝像頭
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