import mediapipe as mp
from mediapipe.tasks.python import vision, BaseOptions
import numpy as np
import cv2
import math
from time import time

cam = cv2.VideoCapture(0)

pos = [500., 500.]
old_thumb_loc = None
streak = 0

def callback(res, img, time):
    global old_thumb_loc, streak
    if res.gestures:
        gesture = res.gestures[0][0]
        thumb_loc = [res.hand_landmarks[0][5].x, res.hand_landmarks[0][5].y]
        if old_thumb_loc and gesture.category_name == "touching":
            streak += 1
            delta_thumb = [thumb_loc[0] - old_thumb_loc[0], thumb_loc[1] - old_thumb_loc[1]]
            pos[0] += delta_thumb[0]
            pos[1] += delta_thumb[1]
        else:
            if streak > 0:
                print(streak)
            if streak < 15 and streak > 1:
                print("left click")
            streak = 0
        old_thumb_loc = thumb_loc
    # print(pos)

base_options = BaseOptions("ai-model/export/gesture_recognizer.task")
options = vision.GestureRecognizerOptions(base_options, running_mode=vision.RunningMode.LIVE_STREAM, result_callback=callback)
recognizer = vision.GestureRecognizer.create_from_options(options)

start = math.floor(time() * 1000)

while 1:
    ret, frame = cam.read()
    if ret:
        frame = cv2.flip(frame, 1)
        img = mp.Image(image_format=mp.ImageFormat.SRGB, data=frame)
        recognizer.recognize_async(img, math.floor(time() * 1000) - start)
    else:
        print("broke")
        break