import math


class SpeedEstimator:
    def __init__(self, distance_meters=10, fps=30):
        self.distance_meters = distance_meters
        self.fps = fps
        self.tracked_objects = {}

    def calculate_speed(self, object_id, center_point, frame_number):
        if object_id not in self.tracked_objects:
            self.tracked_objects[object_id] = {
                'points': [(center_point, frame_number)],
                'speeds': []
            }
        else:
            self.tracked_objects[object_id]['points'].append((center_point, frame_number))

        if len(self.tracked_objects[object_id]['points']) >= 2:
            point1, frame1 = self.tracked_objects[object_id]['points'][-2]
            point2, frame2 = self.tracked_objects[object_id]['points'][-1]
            pixel_distance = math.sqrt((point2[0] - point1[0]) ** 2 + (point2[1] - point1[1]) ** 2)
            real_distance = pixel_distance * (self.distance_meters / 100)
            time_diff = (frame2 - frame1) / self.fps
            if time_diff > 0:
                speed = (real_distance / time_diff) * 3.6  # m/s to km/h
                self.tracked_objects[object_id]['speeds'].append(speed)
                return sum(self.tracked_objects[object_id]['speeds'][-3:]) / len(self.tracked_objects[object_id]['speeds'][-3:])
        return None
