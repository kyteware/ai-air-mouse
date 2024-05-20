import mediapipe as mp
from mediapipe.tasks.python import vision, BaseOptions
import numpy as np
import cv2
import math
from time import time
from evdev import UInput, AbsInfo,  ecodes as e

cam = cv2.VideoCapture(0)

cap = {
    e.EV_KEY : [e.BTN_LEFT, e.BTN_RIGHT],
    e.EV_REL : [e.REL_X, e.REL_Y]
} 
mouse = UInput(cap, name="stupid-glove", version=0x3)
print(mouse)

pos = [500., 500.]
old_thumb_loc = None
streak = 0

LEFT_CLICK_CUTOFF = 20

def callback(res, img, time):
    global old_thumb_loc, streak, mouse
    if res.gestures:
        gesture = res.gestures[0][0]
        thumb_loc = [res.hand_landmarks[0][5].x, res.hand_landmarks[0][5].y]
        if old_thumb_loc and gesture.category_name == "touching" and gesture.score > 0.7:
            streak += 1
            delta_thumb = [thumb_loc[0] - old_thumb_loc[0], thumb_loc[1] - old_thumb_loc[1]]
            pos[0] += delta_thumb[0]
            pos[1] += delta_thumb[1]
            mouse.write(e.EV_REL, e.REL_X, int(delta_thumb[0] * 3000))
            mouse.write(e.EV_REL, e.REL_Y, int(delta_thumb[1] * 3000))
            mouse.syn()
        else:
            if streak < LEFT_CLICK_CUTOFF and streak > 1:
                print("emitting")
                mouse.write(e.EV_KEY, e.BTN_LEFT, 1)
                mouse.syn()
                mouse.write(e.EV_KEY, e.BTN_LEFT, 0)
                mouse.syn()
            streak = 0
        old_thumb_loc = thumb_loc

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