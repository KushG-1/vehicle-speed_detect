from ultralytics import YOLO


class VehicleDetector:
    def __init__(self, model_path='yolov8n.pt'):
        self.model = YOLO(model_path)
        self.classes = self.model.names

    def detect_vehicles(self, frame):
        results = self.model(frame)
        detections = []
        for r in results:
            for box in r.boxes:
                x1, y1, x2, y2 = map(int, box.xyxy[0])
                conf = float(box.conf[0])
                cls = int(box.cls[0])
                if cls in [2, 3, 5, 7] and conf > 0.5:  # Cars, Motorcycles, Trucks, Buses
                    detections.append({
                        'bbox': (x1, y1, x2, y2),
                        'class': self.classes[cls],
                        'confidence': conf
                    })
        return detections
