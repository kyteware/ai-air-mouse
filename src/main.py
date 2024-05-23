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

old_index_loc = None
touch_hist = [False] * 10
touching = False

LEFT_CLICK_CUTOFF = 20

def callback(res, img, time):
    # if res.gestures:
        # thumb_loc = [res.hand_landmarks[0][4].x, res.hand_landmarks[0][4].y]
        # index_loc = [res.hand_landmarks[0][8].x, res.hand_landmarks[0][8].y]
        # dist = res.hand_landmarks[0][8].z
        # print(1/math.sqrt((thumb_loc[0] - index_loc[0])**2 + (thumb_loc[1] - index_loc[1])**2) * (-dist)**0.75 * 0.3) # check dist sign
    global old_index_loc, streak, mouse, touching, touch_hist
    if res.gestures:
        gesture = res.gestures[0][0]
        index_loc = [res.hand_landmarks[0][8].x, res.hand_landmarks[0][8].y]
        thumb_loc = [res.hand_landmarks[0][4].x, res.hand_landmarks[0][4].y]

        gesture_score = gesture.score if gesture.category_name == "touching" else 1 - gesture.score

        dist = -(res.hand_landmarks[0][4].z + res.hand_landmarks[0][8].z) / 2
        if dist < 0:
            return
        manual_score = min(max(1/math.sqrt((thumb_loc[0] - index_loc[0])**2 + (thumb_loc[1] - index_loc[1])**2) * dist**0.75 * 0.3, 0), 1)

        score = gesture_score * 0.4 + manual_score * 0.6       

        if old_index_loc:
            if score > 0.7:
                if touch_hist[7:9] == [True] * 2 and touching == False:
                    touching = True
                    mouse.write(e.EV_KEY, e.BTN_LEFT, 1)
                    mouse.syn()
                    mouse.write(e.EV_KEY, e.BTN_LEFT, 0)
                    mouse.syn()
                touch_hist[0:9] = touch_hist[1:10]
                touch_hist[9] = True
            else:
                if touch_hist[7:9] == [False] * 2 and touching == True:
                    touching = False
                touch_hist[0:9] = touch_hist[1:10]
                touch_hist[9] = False
            delta_index = [index_loc[0] - old_index_loc[0], index_loc[1] - old_index_loc[1]]
            mouse.write(e.EV_REL, e.REL_X, int(delta_index[0] * 3000))
            mouse.write(e.EV_REL, e.REL_Y, int(delta_index[1] * 3000))
            mouse.syn()
        old_index_loc = index_loc
    print(touch_hist)

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