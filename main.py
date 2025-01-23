import cv2
import threading
from gui import SpeedDetectionGUI
from vehicle_detection import VehicleDetector
from speed_estimation import SpeedEstimator
from license_plate_recognition import LicensePlateRecognizer
from logger import Logger


class SpeedDetectionSystem:
    def __init__(self):
        self.gui = SpeedDetectionGUI()
        self.vehicle_detector = VehicleDetector()
        self.speed_estimator = SpeedEstimator()
        self.plate_recognizer = LicensePlateRecognizer()
        self.logger = Logger()
        self.running = False
        self.gui.set_start_command(self.start_detection)
        self.gui.set_stop_command(self.stop_detection)

    def start_detection(self):
        if not self.running:
            self.running = True
            source = self.gui.get_video_source()
            self.capture = cv2.VideoCapture(0 if source == "Webcam" else source)
            if not self.capture.isOpened():
                self.gui.update_status("Failed to open video source!")
                self.running = False
                return
            self.gui.update_status("Running")
            threading.Thread(target=self.process_video, daemon=True).start()

    def stop_detection(self):
        self.running = False
        if hasattr(self, "capture"):
            self.capture.release()
        self.gui.update_status("Stopped")

    def process_video(self):
        while self.running:
            ret, frame = self.capture.read()
            if not ret:
                break
            detections = self.vehicle_detector.detect_vehicles(frame)
            for det in detections:
                bbox = det["bbox"]
                x1, y1, x2, y2 = bbox
                cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
                center_x = (x1 + x2) // 2
                center_y = (y1 + y2) // 2
                speed = self.speed_estimator.calculate_speed(f"{center_x}_{center_y}", (center_x, center_y), int(self.capture.get(cv2.CAP_PROP_POS_FRAMES)))
                if speed:
                    if speed > self.gui.speed_limit:
                        color = (0, 0, 255)  # Red for speeding
                    else:
                        color = (0, 255, 0)  # Green for normal
                    cv2.putText(frame, f"{speed:.1f} km/h", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
                    self.logger.log(det["class"], speed, None)
                    self.gui.log_box.insert(tk.END, f"{det['class']} | {speed:.1f} km/h\n")
            self.gui.update_image(frame)
        self.capture.release()
        self.gui.update_status("Stopped")

    def run(self):
        self.gui.run()


if __name__ == "__main__":
    SpeedDetectionSystem().run()
