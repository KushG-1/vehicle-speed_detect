import csv
from datetime import datetime


class Logger:
    def __init__(self, filename="log.csv"):
        with open(filename, mode="w", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(["Timestamp", "Vehicle Class", "Speed (km/h)", "License Plate"])

    def log(self, vehicle_class, speed, plate):
        with open("log.csv", mode="a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow([datetime.now().isoformat(), vehicle_class, speed, plate])
