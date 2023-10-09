from __future__ import print_function
import os

import numpy as np
import cv2 as cv

from multiprocessing.pool import ThreadPool
from collections import deque

from common import clock, draw_str, StatValue

from pathlib import Path
from dotenv import load_dotenv

from optical_flow import *
from img_process import *

class DummyTask:
    def __init__(self, data):
        self.data = data
    def ready(self):
        return True
    def get(self):
        return self.data

def main():
    env_path = Path('.') / '.env'
    load_dotenv(dotenv_path=env_path)

    username = os.environ['CAM_USER']
    password = os.environ['CAM_PASS']
    address = os.environ['CAM_IP']

    cam_url = f"rtsp://{username}:{password}@{address}:554/Streaming/Channels/101/"

    cap = cv.VideoCapture(cam_url)
    # cap = cv.VideoCapture(0)


    img_processing = ImageProcessing()
    first_init = True

    def process_frame(frame, t0, heavy, process):
        # some intensive computation...
        # frame = cv.medianBlur(frame, 19)
        # frame = cv.medianBlur(frame, 19)

        if process:
            if heavy:
                # optical flow
                frame = opt_flow.get_optical_flow(frame)
            else:
                # background subtraction
                frame = img_processing.update(frame)

        return frame, t0

    threadn = cv.getNumberOfCPUs()
    pool = ThreadPool(processes = threadn)
    pending = deque()

    cv_mode = False
    heavy_mode = True
    threaded_mode = True

    latency = StatValue()
    frame_interval = StatValue()
    last_frame_time = clock()
    while True:
        while len(pending) > 0 and pending[0].ready():
            res, t0 = pending.popleft().get()
            latency.update(clock() - t0)
            draw_str(res, (20, 20), "threaded      :  " + str(threaded_mode))
            draw_str(res, (20, 40), "Process CV      :  " + str(cv_mode))
            draw_str(res, (20, 60), "Heavy CV      :  " + str(heavy_mode))
            # draw_str(res, (20, 40), "latency        :  %.1f ms" % (latency.value*1000))
            draw_str(res, (20, 80), "frame interval :  %.1f ms" % (frame_interval.value*1000))
            cv.imshow('threaded video', res)
        if len(pending) < threadn:
            _ret, frame = cap.read()

            if first_init == True:
                opt_flow = OpticalFlow(frame)
                first_init == False

            t = clock()
            frame_interval.update(t - last_frame_time)
            last_frame_time = t
            if threaded_mode:
                task = pool.apply_async(process_frame, (frame.copy(), t, heavy_mode, cv_mode))
            else:
                task = DummyTask(process_frame(frame, t, heavy_mode, cv_mode))
            pending.append(task)
        ch = cv.waitKey(1)
        if ch == ord(' '):
            threaded_mode = not threaded_mode
        if ch == ord('1'):
            heavy_mode = not heavy_mode
        if ch == ord('q'):
            cv_mode = not cv_mode
        if ch == 27:
            break

    print('Done')


if __name__ == '__main__':
    print(__doc__)
    main()
    cv.destroyAllWindows()