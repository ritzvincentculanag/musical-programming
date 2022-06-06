import cv2
import time
import os


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


#


while True:
    success, img = cap.read()

    h, w, c = overlays[1].shape
    img[0:h, 0:w] = overlays[1]

    cv2.imshow('Musical Programming', img)
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
