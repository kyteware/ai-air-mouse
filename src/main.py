import mediapipe as mp
import numpy as np
import cv2
import math

cam = cv2.VideoCapture(0)
win = cv2.namedWindow("capstone")

mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=1)
mp_draw = mp.solutions.drawing_utils

pos = [300, 300]
last_thumb_coords = [0, 0]
delta_thumb_coords = [0, 0]

while 1:
    ret, frame = cam.read()
    if ret:
        x, y, _ = frame.shape
        frame = cv2.flip(frame, 1)
        result = hands.process(frame)
        if result.multi_hand_landmarks:
                thumb = result.multi_hand_landmarks[0].landmark[4]
                delta_thumb_coords = (thumb.x - last_thumb_coords[0], thumb.y - last_thumb_coords[1])
                last_thumb_coords = (thumb.x, thumb.y)

                mp_draw.draw_landmarks(frame, result.multi_hand_landmarks[0], mp_hands.HAND_CONNECTIONS)
        if result.multi_hand_world_landmarks:
            thumb = result.multi_hand_world_landmarks[0].landmark[4]
            index = result.multi_hand_world_landmarks[0].landmark[8]
            dist = math.sqrt((abs(thumb.x - index.x)**2 + abs(thumb.y - index.y)**2 + abs(thumb.z - thumb.z)**2))
            if dist < 0.03:
                print(delta_thumb_coords)
                pos[0] += delta_thumb_coords[0] * 1000
                pos[1] += delta_thumb_coords[1] * 1000
        
        frame = cv2.circle(frame, (int(pos[0]), int(pos[1])), 25, (255,255,0), 3)
        cv2.imshow("capstone", frame)
        cv2.waitKey(1)
    else:
        print("broke")
        break