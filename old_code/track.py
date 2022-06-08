# General imports
import cv2
import time
import os

# Selective imports
from track_hand import TrackHand
# from pygame import mixer


class Track:
    def __init__(self):
        # Capture device settings
        self.cap_w = 640
        self.cap_h = 640
        self.cap = cv2.VideoCapture(0)
        self.cap.set(3, self.cap_w)
        self.cap.set(4, self.cap_h)

        # Images settings
        self.folder_path = '../images'
        self.images = os.listdir(self.folder_path)
        self.images.sort()
        self.overlays = []
        for img_path in self.images:
            img = cv2.imread(f'{self.folder_path}/{img_path}')
            self.overlays.append(img)

        # Tracking settings
        self.detector = TrackHand(detection_confidence=0.8)  # Instance of TrackHand()
        self.tip_ids = [4, 8, 12, 16, 20]  # Finger points

        # Mixer settings
        # TODO: Initialize mixer

        # FPS settings
        self.previous_time = time.time()

    def track(self):
        success, img = self.cap.read()
        img = self.detector.find_hands(img)
        landmarks = self.detector.find_position(img)

        if not len(landmarks) == 0:
            fingers = []

            # Track thumb
            if landmarks[self.tip_ids[0]][1] < landmarks[self.tip_ids[0] - 1][1]:
                fingers.append(1)
            else:
                fingers.append(0)

            # Track other 4 fingers
            for lid in range(1, 5):
                if landmarks[self.tip_ids[lid]][2] < landmarks[self.tip_ids[lid] - 2][2]:
                    fingers.append(1)
                else:
                    fingers.append(0)

            total_fingers = fingers.count(1)
            print(total_fingers)

        # Draw image numbrers on screen
        h, w, c = self.overlays[1].shape
        img[0:h, 0:w] = self.overlays[1]

        # # Set FPS
        # current_time = time.time()
        # fps = 1 / (current_time - self.previous_time)
        # self.previous_time = current_time
        #
        # # Render points and connections to hand
        # cv2.putText(
        #     img=img,
        #     text=f'FPS: {int(fps)}',
        #     org=(500, 40),
        #     fontFace=cv2.QT_FONT_NORMAL,
        #     fontScale=1,
        #     color=(255, 0, 0),
        #     thickness=3
        # )
        cv2.imshow('Musical Programming', img)



