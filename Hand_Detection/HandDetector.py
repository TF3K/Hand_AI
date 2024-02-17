import cv2 as cv
import mediapipe as mp
import numpy as np
import tensorflow as tf
from tensorflow.keras.models import load_model
from Hand_Detection.Commands import Commands

class HandDetector:
    def __init__(self, cam_index=0):
        self.commands = Commands()
        self.cap = cv.VideoCapture(cam_index)  # Check camera index

        # Check if camera opened successfully
        if not self.cap.isOpened():
            print("Error opening camera!")
            return

        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(max_num_hands=1, min_detection_confidence=0.9)
        self.mpDraw = mp.solutions.drawing_utils
        self.model = load_model('Hand_Detection/mp_hand_gesture')

    def run(self):
        f = open('gesture.names', 'r')
        classNames = f.read().split("\n")
        f.close()
        print(classNames)

        while self.cap.isOpened():
            _, frame = self.cap.read()
            x, y, c = frame.shape
            frame = cv.flip(frame, 1)
            framergb = cv.cvtColor(frame, cv.COLOR_BGR2RGB)
            res = self.hands.process(framergb)
            className = ""

            if res.multi_hand_landmarks:
                landmarks = []
                for handlms in res.multi_hand_landmarks:
                    for lm in handlms.landmark:
                        lmx = int(lm.x * x)
                        lmy = int(lm.y * y)
                        landmarks.append([lmx, lmy])
                    landmarks = np.expand_dims(landmarks, axis=0)  # Add batch dimension
                    prediction = self.model.predict(landmarks)
                    classID = np.argmax(prediction)
                    if 0 <= classID < len(classNames):  # Check valid range
                        className = classNames[classID]
                        self.commands.execute_commands(classID)
                    else:
                        print("Invalid class ID:", classID)
                
            cv.imshow("Hand Detection", frame)
            if cv.waitKey(1) == ord('q'):
                break

        self.cap.release()
        cv.destroyAllWindows()
