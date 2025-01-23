import cv2
import pytesseract


class LicensePlateRecognizer:
    def __init__(self):
        self.license_plate_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_russian_plate_number.xml')

    def detect_license_plate(self, frame):
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        plates = self.license_plate_cascade.detectMultiScale(gray, 1.1, 4)
        for (x, y, w, h) in plates:
            plate_img = gray[y:y + h, x:x + w]
            text = pytesseract.image_to_string(plate_img, config='--psm 8').strip()
            if text:
                return {'text': text, 'bbox': (x, y, w, h)}
        return None
