import cv2 as cv
from tracker import *

class ImageProcessing:
    def __init__(self):
        self.object_detector = cv.createBackgroundSubtractorMOG2(history=100, varThreshold=50, detectShadows=False)
        self.tracker = EuclideanDistTracker()

    def update(self, current_frame):
        # current_frame = cv.medianBlur(current_frame, 19)
        # current_frame = cv.medianBlur(current_frame, 19)

        gray = cv.cvtColor(current_frame, cv.COLOR_BGR2GRAY)
        mask = self.object_detector.apply(gray)
        _, mask = cv.threshold(mask, 254, 255, cv.THRESH_BINARY)
        contours, _ = cv.findContours(mask, cv.RETR_TREE, cv.CHAIN_APPROX_SIMPLE)
        detections = []
        for cnt in contours:
            # Calculate area and remove small elements
            area = cv.contourArea(cnt)
            if area > 500:
                x, y, w, h = cv.boundingRect(cnt)
                detections.append([x, y, w, h])

        boxes_ids = self.tracker.update(detections)
        for box_id in boxes_ids:
            x, y, w, h, id = box_id
            cv.putText(gray, str(id), (x, y - 15), cv.FONT_HERSHEY_PLAIN, 2, (255, 0, 0), 2)
            cv.rectangle(gray, (x, y), (x + w, y + h), (0, 255, 0), 3)
        

        return gray