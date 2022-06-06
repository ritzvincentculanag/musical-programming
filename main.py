# General imports
import cv2
import time
import os

# Selective imports
from track_hand import TrackHand
from pygame import mixer

# Capture device settings
cap_w, cap_h = 640, 640

cap = cv2.VideoCapture(0)
cap.set(3, cap_w)
cap.set(4, cap_h)

# Image golder settings
folder_path = 'images'
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

e = mixer.Sound('./assets/e.mp3')
f = mixer.Sound('./assets/f.mp3')
g = mixer.Sound('./assets/g.mp3')
a = mixer.Sound('./assets/a.mp3')

# Create instance of TrackHand
detector = TrackHand(detection_confidence=0.8)

# List of tips for every finger
tip_ids = [4, 8, 12, 16, 20]

while True:
    success, img = cap.read()

    # Get image information
    img = detector.find_hands(img)
    landmarks = detector.find_position(img, draw=False)

    if len(landmarks) != 0:
        fingers = []

        # Thumb
        if landmarks[tip_ids[0]][1] < landmarks[tip_ids[0] - 1][1]:
            fingers.append(1)
        else:
            fingers.append(0)

        # 4 fingers
        for id in range(1, 5):
            # Up means lower value
            # Down means higher value
            if landmarks[tip_ids[id]][2] < landmarks[tip_ids[id] - 2][2]:
                fingers.append(1)
            else:
                fingers.append(0)

        total_fingers = fingers.count(1)
        if total_fingers == 1:
            c = mixer.Sound('./assets/c.mp3')
            c.play()
            c.stop()
        elif total_fingers == 2:
            d = mixer.Sound('./assets/d.mp3')
            d.play()
            d.stop()

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
