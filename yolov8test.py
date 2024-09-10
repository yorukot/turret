from ultralytics import YOLO
import cv2
import math

# Initialize cameras
camera1_index = 0
camera2_index = 2

cap1 = cv2.VideoCapture(camera1_index)
cap2 = cv2.VideoCapture(camera2_index)

# Set camera resolution
cap1.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap1.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
cap2.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
cap2.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

# Load YOLO model
model = YOLO("yolov8n.pt")
model.classes = [0]  # Detect only 'person'
model.to('cuda')

# Object classes
classNames = ["person", "bicycle", "car", "motorbike", "aeroplane", "bus", "train", "truck", "boat",
              "traffic light", "fire hydrant", "stop sign", "parking meter", "bench", "bird", "cat",
              "dog", "horse", "sheep", "cow", "elephant", "bear", "zebra", "giraffe", "backpack", "umbrella",
              "handbag", "tie", "suitcase", "frisbee", "skis", "snowboard", "sports ball", "kite", "baseball bat",
              "baseball glove", "skateboard", "surfboard", "tennis racket", "bottle", "wine glass", "cup",
              "fork", "knife", "spoon", "bowl", "banana", "apple", "sandwich", "orange", "broccoli",
              "carrot", "hot dog", "pizza", "donut", "cake", "chair", "sofa", "pottedplant", "bed",
              "diningtable", "toilet", "tvmonitor", "laptop", "mouse", "remote", "keyboard", "cell phone",
              "microwave", "oven", "toaster", "sink", "refrigerator", "book", "clock", "vase", "scissors",
              "teddy bear", "hair drier", "toothbrush"]

def process_frame(frame, classNames, model):
    # Convert frame to RGB format
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

    # Perform inference with YOLO model
    results = model(frame_rgb, stream=True)

    # Iterate over results
    for r in results:
        boxes = r.boxes

        for box in boxes:
            # Calculate confidence
            confidence = math.ceil((box.conf[0] * 100)) / 100
            if confidence < 0.5:
                continue

            # Get bounding box coordinates
            x1, y1, x2, y2 = box.xyxy[0]
            x1, y1, x2, y2 = int(x1), int(y1), int(x2), int(y2)

            # Draw bounding box
            cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 0, 255), 3)

            # Class name
            cls = int(box.cls[0])

            # Object details on screen
            org = (x1, y1)
            font = cv2.FONT_HERSHEY_SIMPLEX
            fontScale = 1
            color = (255, 0, 0)
            thickness = 2
            cv2.putText(frame, classNames[cls] + " " + str(confidence), org, font, fontScale, color, thickness)

    return frame

while True:
    # Capture frames from both cameras
    success1, frame1 = cap1.read()
    success2, frame2 = cap2.read()

    if not success1 or not success2:
        print("Failed to capture image from one of the cameras.")
        break

    # Process each frame and draw detection results
    frame2_processed = process_frame(frame2, classNames, model)
    frame1_processed = process_frame(frame1, classNames, model)

    # Display the results
    cv2.imshow('Camera 1', frame1_processed)
    cv2.imshow('Camera 2', frame2_processed)

    # Break the loop on 'q' key press
    if cv2.waitKey(1) == ord('q'):
        break

# Release resources
cap1.release()
cap2.release()
cv2.destroyAllWindows()
