import mediapipe as mp
import numpy as np
import cv2

cam = cv2.VideoCapture(0)
# win = cv2.namedWindow("capstone")

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
mp_draw = mp.solutions.drawing_utils

while 1:
    ret, frame = cam.read()
    if ret:
        print("hi")
        x, y, _ = frame.shape
        frame = cv2.flip(frame, 1)
        # rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        result = hands.process(frame)

        if result.multi_hand_landmarks:
            landmarks = []
            for handslms in result.multi_hand_landmarks:
                for lm in handslms.landmark:
                    lmx = int(lm.x * x)
                    lmy = int(lm.y * y)
                    landmarks.append([lmx, lmy])

                mp_draw.draw_landmarks(frame, handslms, mp_hands.HAND_CONNECTIONS)
        
        cv2.imshow("capstone", frame)
        cv2.waitKey(1)
    else:
        break