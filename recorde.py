#from picamera import PiCamera
import time

from picamera import PiCamera
from time import sleep
import numpy as np
import cv2 as cv
import argparse



def print_hi(name):
    camera = PiCamera()
    camera.rotation = 180
    date = time.time()
    camera.start_recording('/home/pi/videos/bed1'+str(date)+'.h264')
    sleep(5)
    camera.stop_recording()
    print("finished")

    # # parser = argparse.ArgumentParser(description='This sample demonstrates Lucas-Kanade Optical Flow calculation. \
    # #                                               The example file can be downloaded from: \
    # #                                               https://www.bogotobogo.com/python/OpenCV_Python/images/mean_shift_tracking/slow_traffic_small.mp4')
    # # parser.add_argument('image', type=str, help='path to image file')
    # # args = parser.parse_args()
    # cap = cv.VideoCapture(r"home/pi/slow_traffic_small.mp4")
    # if (cap.isOpened() == False):
    #     print("Error opening video stream or file")
    # # params for ShiTomasi corner detection
    # feature_params = dict(maxCorners=100,
    #                       qualityLevel=0.3,
    #                       minDistance=7,
    #                       blockSize=7)
    # # Parameters for lucas kanade optical flow
    # lk_params = dict(winSize=(15, 15),
    #                  maxLevel=2,
    #                  criteria=(cv.TERM_CRITERIA_EPS | cv.TERM_CRITERIA_COUNT, 10, 0.03))
    # # Create some random colors
    # color = np.random.randint(0, 255, (100, 3))
    # # Take first frame and find corners in it
    # ret, old_frame = cap.read()
    # #cv.imshow("bla" ,old_frame)
    # old_gray = cv.cvtColor(old_frame, cv.COLOR_BGR2GRAY)
    # p0 = cv.goodFeaturesToTrack(old_gray, mask=None, **feature_params)
    # # Create a mask image for drawing purposes
    # mask = np.zeros_like(old_frame)
    # while (1):
    #     ret, frame = cap.read()
    #     frame_gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY)
    #     # calculate optical flow
    #     p1, st, err = cv.calcOpticalFlowPyrLK(old_gray, frame_gray, p0, None, **lk_params)
    #     # Select good points
    #     good_new = p1[st == 1]
    #     good_old = p0[st == 1]
    #     # draw the tracks
    #     for i, (new, old) in enumerate(zip(good_new, good_old)):
    #         a, b = new.ravel()
    #         c, d = old.ravel()
    #         mask = cv.line(mask, (a, b), (c, d), color[i].tolist(), 2)
    #         frame = cv.circle(frame, (a, b), 5, color[i].tolist(), -1)
    #     img = cv.add(frame, mask)
    #     cv.imshow('frame', img)
    #     k = cv.waitKey(30) & 0xff
    #     if k == 27:
    #         break
    #     # Now update the previous frame and previous points
    #     old_gray = frame_gray.copy()
    #     p0 = good_new.reshape(-1, 1, 2)

# Press the green button in the gutter to run the script.
if __name__ == '__main__':
    print_hi('PyCharm')

# See PyCharm help at https://www.jetbrains.com/help/pycharm/
