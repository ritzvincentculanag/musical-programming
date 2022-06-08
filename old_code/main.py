# General imports
import threading

import cv2
import time
import os

# Selective imports
import pygame.time
from threading import Event

from track_hand import TrackHand
from pygame import mixer

# Capture device settings
cap_w, cap_h = 640, 640

cap = cv2.VideoCapture(0)
cap.set(3, cap_w)
cap.set(4, cap_h)

# Image golder settings
folder_path = '../images'
images = os.listdir(folder_path)
images.sort()
overlays = []

for img_path in images:
    img = cv2.imread(f'{folder_path}/{img_path}')
    overlays.append(img)

# FPS settings
previous_time = 0

# Load sounds
mixer.init()

# Create instance of TrackHand
detector = TrackHand(detection_confidence=0.8)

# List of tips for every finger
tip_ids = [4, 8, 12, 16, 20]

# Game state
app_running = True
delta_time = 0.0


def play_note(note):
    if note == 'c':
        c = mixer.Sound('../assets/c.mp3')
        c.play()
    elif note == 'e':
        e = mixer.Sound('../assets/e.mp3')
        e.play()
    time.sleep(1)


# Audio thread
audio = threading.Thread(target=play_note)
audio.start()

while True:
    # Get return and image from capture device
    success, img = cap.read()

    # Get image information
    img = detector.find_hands(img)
    landmarks = detector.find_position(img, draw=False)

    if len(landmarks) != 0:
        fingers = []
        if landmarks[4][1] < landmarks[4 - 1][1] \
                and landmarks[8][2] < landmarks[8 - 2][2] \
                and landmarks[12][2] < landmarks[12 - 2][2] \
                and landmarks[16][2] < landmarks[16 - 2][2] \
                and landmarks[20][2] < landmarks[20 - 2][2]:
            print("C")
            play_note('c')
        elif landmarks[4][1] < landmarks[4 - 1][1] \
                and landmarks[8][2] < landmarks[8 - 2][2]:
            play_note('e')
            print("D")


        # Thumb

        # if landmarks[tip_ids[0]][1]q < landmarks[tip_ids[0] - 1][1] \
        #         and landmarks[tip_ids[1]][2] < landmarks[tip_ids[1] - 2][2] \
        #         and landmarks[tip_ids[2]][2] < landmarks[tip_ids[2] - 2][2] \
        #         and landmarks[tip_ids[3]][2] < landmarks[tip_ids[3] - 2][2] \
        #         and landmarks[tip_ids[4]][2] < landmarks[tip_ids[4] - 2][2]:

        # # 4 fingers
        # for id in range(0, 5):
        #     # Up means lower value
        #     # Down means higher value
        #
        #     if landmarks[tip_ids[id]][1] < landmarks[tip_ids[id] - 1][1] \
        #             and landmarks[tip_ids[id]][2] < landmarks[tip_ids[id] - 1][1]:
        #         c = mixer.Sound('./assets/c.mp3')
        #         c.play()

        # if landmarks[tip_ids[id]][2] < landmarks[tip_ids[id] - 2][2]:
        #     fingers.append(1)
        # else:
        #     fingers.append(0)
        #
        # # Test
        # if landmarks[tip_ids[0]][1] < landmarks[tip_ids[0] - 1][1] \
        #         and landmarks[tip_ids]:
        #     c = mixer.Sound('./assets/c.mp3')
        #     c.play(maxtime=1000)

        # total_fingers = fingers.count(1)
        # print(total_fingers)
        # # if total_fingers == 0:
        # #     c = mixer.Sound('./assets/c.mp3')
        # #     c.play(maxtime=1000)
        # if total_fingers == 1:
        #     c = mixer.Sound('./assets/c.mp3')
        #     c.play(maxtime=1000)
        # elif total_fingers == 2:
        #     e = mixer.Sound('./assets/e.mp3')
        #     e.play(maxtime=1000)

        h, w, c = overlays[1].shape
        img[0:h, 0:w] = overlays[1]

        # Set FPS
        current_time = time.time()
        fps = 1 / (current_time - previous_time)
        previous_time = current_time

        # Render to screen
        cv2.putText(
            img=img,
            text=f'FPS: {int(fps)}',
            org=(500, 40),
            fontFace=cv2.QT_FONT_NORMAL,
            fontScale=1,
            color=(255, 0, 0),
            thickness=3
        )
        cv2.imshow('Musical Programming', img)
        if cv2.waitKey(10) & 0xFF == ord('q'):
            break
