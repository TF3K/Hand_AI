import cv2 as cv
import mediapipe as mp
import numpy as np
import tensorflow as tf
import time
from tensorflow.keras.models import load_model
from Hand_Detection.Commands import Commands

class HandDetector:
    def __init__(self, cam_index=0):
        self.commands = Commands()
        self.cap = cv.VideoCapture(cam_index)  # Check camera index
        self.exe_dict = {}
        self.mpHands = mp.solutions.hands
        self.hands = self.mpHands.Hands(max_num_hands=1, min_detection_confidence=0.9)
        self.mpDraw = mp.solutions.drawing_utils
        self.model = load_model('Hand_Detection/mp_hand_gesture')
        self.cooldown_duration = 5
        self.last_execution_time = 0

    def run(self):
        f = open('gesture.names', 'r')
        classNames = f.read().split("\n")
        f.close()
        print(classNames)

        while self.cap.isOpened():
            current_time = time.time()
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
                    if 0 <= classID < len(classNames): # Check valid range
                        className = classNames[classID]
                        if classID not in self.exe_dict:
                            self.exe_dict[classID] = {'exe_nb':0, 'exe_cd':self.cooldown_duration}

                        if self.exe_dict[classID]['exe_nb'] == 0:
                            self.commands.execute_commands(classID)
                            self.exe_dict[classID]['exe_nb'] = 1
                            self.last_execution_time = current_time
                            
                        if current_time - self.last_execution_time >= 1:
                            self.exe_dict[classID]['exe_cd'] -= 1
                            if self.exe_dict[classID]['exe_cd'] == 0:
                                self.exe_dict[classID]['exe_cd'] = 5
                                self.exe_dict[classID]['exe_nb'] = 0  # Reset exe_nb to 0
                    else:
                        print("Invalid class ID:", classID)
                    
                cv.putText(frame, className, (10, 50), cv.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv.LINE_AA)
                self.mpDraw.draw_landmarks(frame, handlms, self.mpHands.HAND_CONNECTIONS)
                
            cv.imshow("Hand Detection", frame)
            if cv.waitKey(1) == ord('q'):
                break

        self.cap.release()
        cv.destroyAllWindows()
