#<=============================== Imports ===================================>#
import cv2 as cv
import numpy as np

# =========================== OpticalFlow Class =========================== #
class OpticalFlow:
    
    def __init__(self, first_frame):
        self.prev_gray = cv.cvtColor(first_frame, cv.COLOR_BGR2GRAY)
        self.mask = np.zeros_like(first_frame)
        self.mask[..., 1] = 255

    def get_optical_flow(self, frame):
        # Converts each frame to grayscale - we previously 
        # only converted the first frame to grayscale
        self.gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)

        # Calculates dense optical flow by Farneback method
        flow = cv.calcOpticalFlowFarneback(self.prev_gray, self.gray, 
                                           None,
                                           0.5, 3, 15, 3, 5, 1.2, 0)

        # Computes the magnitude and angle of the 2D vectors
        magnitude, angle = cv.cartToPolar(flow[..., 0], flow[..., 1])

        # Sets image hue according to the optical flow 
        # direction
        self.mask[..., 0] = angle * 180 / np.pi / 2

        # Sets image value according to the optical flow
        # magnitude (normalized)
        self.mask[..., 2] = cv.normalize(magnitude, None, 0, 255, cv.NORM_MINMAX)

        # Converts HSV to RGB (BGR) color representation
        rgb = cv.cvtColor(self.mask, cv.COLOR_HSV2BGR)

        # Updates previous frame
        self.prev_gray = self.gray

        return frame


