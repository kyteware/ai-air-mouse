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
est_thumb_pos = None
est_index_pos = None
est_thumb_log_pos = None
est_index_log_pos = None

while 1:
    ret, frame = cam.read()
    if ret:
        x, y, _ = frame.shape
        frame = cv2.flip(frame, 1)
        result = hands.process(frame)
        if result.multi_hand_landmarks: # this will skip if theres no hand
            mp_draw.draw_landmarks(frame, result.multi_hand_landmarks[0], mp_hands.HAND_CONNECTIONS)
            hand_log = result.multi_hand_landmarks[0].landmark
            thumb_log = hand_log[4]
            index_log = hand_log[8]
            hand = result.multi_hand_world_landmarks[0].landmark
            thumb = hand[4]
            index = hand[8]
            
            if est_thumb_pos is None:
                est_thumb_pos = [thumb.x, thumb.y, thumb.z]
                est_index_pos = [index.x, index.y, thumb.z]

            est_thumb_pos[0] += (thumb.x - est_thumb_pos[0]) / 2
            est_thumb_pos[1] += (thumb.y - est_thumb_pos[1]) / 2
            est_thumb_pos[2] += (thumb.z - est_thumb_pos[2]) / 2
            print(est_thumb_pos[2])

            dist1 = math.sqrt((abs(est_index_pos[0] - est_thumb_pos[0])**2 + abs(est_index_pos[1] - est_thumb_pos[1])**2 + abs(est_index_pos[2] - est_thumb_pos[2])**2))
            dist = math.sqrt((abs(thumb.x - index.x)**2 + abs(thumb.y - index.y)**2 + abs(thumb.z - index.z)**2))

            # print(dist1 - dist)
            # if dist < 0.08:
            # print("touching", dist)
        
        frame = cv2.circle(frame, (int(pos[0]), int(pos[1])), 25, (255,255,0), 3)
        cv2.imshow("capstone", frame)
        cv2.waitKey(1)
    else:
        print("broke")
        break