import mediapipe as mp
import cv2
import numpy as np
import time

import threading
import paho.mqtt.client as mqtt

MQTT_BROKER = "172.21.20.108"  # e.g., "192.168.1.100"
MQTT_PORT = 1883
MQTT_TOPIC = "alert/person_detected"

mqtt_client = mqtt.Client()
mqtt_client.connect(MQTT_BROKER, MQTT_PORT, 60)
# MediaPipe setup
BaseOptions = mp.tasks.BaseOptions
DetectionResult = mp.tasks.components.containers.DetectionResult
ObjectDetector = mp.tasks.vision.ObjectDetector
ObjectDetectorOptions = mp.tasks.vision.ObjectDetectorOptions
VisionRunningMode = mp.tasks.vision.RunningMode

person_detected = False
person_start_time = None
warning_triggered = False

MODEL_PATH = "./ssd_mobilenet_v2.tflite"
URL = "http://172.20.10.3"

cap = cv2.VideoCapture(URL + ":81/stream")

latest_result = None
result_lock = threading.Lock()


def print_result(result: DetectionResult, output_image: mp.Image, timestamp_ms: int):
    global latest_result
    with result_lock:
        latest_result = result


options = ObjectDetectorOptions(
    base_options=BaseOptions(model_asset_path=MODEL_PATH),
    running_mode=VisionRunningMode.LIVE_STREAM,
    max_results=3,
    result_callback=print_result
)

with ObjectDetector.create_from_options(options) as detector:
    start_time = time.time()
    while True:
        ret, frame = cap.read()
        if not ret:
            break

        frame_timestamp_ms = int((time.time() - start_time) * 1000)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame_rgb)

        # Detect asynchronously
        detector.detect_async(mp_image, frame_timestamp_ms)
        person_detected_this_frame = False
        with result_lock:
            result_copy = latest_result

        if result_copy:
            for detection in result_copy.detections:
                if detection.categories and detection.categories[0].category_name.lower() == 'person':
                    person_detected_this_frame = True

                bbox = detection.bounding_box
                x_min = int(bbox.origin_x)
                y_min = int(bbox.origin_y)
                box_width = int(bbox.width)
                box_height = int(bbox.height)

                cv2.rectangle(frame, (x_min, y_min), (x_min +
                              box_width, y_min + box_height), (0, 255, 0), 2)
                if detection.categories:
                    label = f"{detection.categories[0].category_name} ({detection.categories[0].score:.2f})"
                    cv2.putText(frame, label, (x_min, y_min - 10),
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)
        current_time = time.time()
        if person_detected_this_frame:
            if person_start_time is None:
                person_start_time = current_time  # Start timer
            elif not warning_triggered and current_time - person_start_time >= 10:
                print("⚠️ WARNING: Person detected for 10 seconds!")
                mqtt_client.publish(
                    MQTT_TOPIC, "Person detected for 10 seconds!")
                warning_triggered = True  # Avoid repeated warnings
        else:
            person_start_time = None
            warning_triggered = False
        cv2.imshow("Detections", frame)
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break

cap.release()
cv2.destroyAllWindows()
