import cv2 as cv
import mediapipe as mp
import os
import logging as lg

class HandDetector:
    def __init__(self, cam_index=0):
        self.cap = cv.VideoCapture(cam_index)
        self.mp_hands = mp.solutions.hands

    def detect_peace_hand_sign(self, hand_landmarks):
        if hand_landmarks is not None:
            if (hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_TIP].y <
                hand_landmarks.landmark[mp.solutions.hands.HandLandmark.INDEX_FINGER_DIP].y and
                hand_landmarks.landmark[mp.solutions.hands.HandLandmark.MIDDLE_FINGER_TIP].y <
                hand_landmarks.landmark[mp.solutions.hands.HandLandmark.MIDDLE_FINGER_DIP].y and
                hand_landmarks.landmark[mp.solutions.hands.HandLandmark.RING_FINGER_TIP].y >
                hand_landmarks.landmark[mp.solutions.hands.HandLandmark.RING_FINGER_DIP].y and
                hand_landmarks.landmark[mp.solutions.hands.HandLandmark.PINKY_TIP].y >
                hand_landmarks.landmark[mp.solutions.hands.HandLandmark.PINKY_DIP].y):
                return True
            return False

    def run(self):
        while self.cap.isOpened():
            os.system("clear")
            ret, img = self.cap.read()
            if not ret:
                break

            img = cv.cvtColor(img,cv.COLOR_BGR2RGB)
            res = self.mp_hands.Hands(max_num_hands=1, min_detection_confidence=0.7).process(img)

            img = cv.cvtColor(img,cv.COLOR_RGB2BGR)
            if res.multi_hand_landmarks:
                for hand in res.multi_hand_landmarks:
                    for point in hand.landmark:
                        x, y = int(point.x * img.shape[1]), int(point.y * img.shape[0])
                        cv.circle(img, (x, y), 5, (0, 255, 0), -1)

                    if self.detect_peace_hand_sign(hand):
                        lg.info("Peace hand sign detected!")
                    else:
                        lg.info("Peace hand sign not detected.")

            cv.imshow('Hand Detector', img)
            if cv.waitKey(1) & 0xFF == ord('q'):
                break

        self.cap.release()
        cv.destroyAllWindows()
        
