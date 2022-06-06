# General imports
import mediapipe as mp
import cv2
import time
import os

# Prepare needed modules
mp_hands = mp.solutions.hands
mp_draw = mp.solutions.drawing_utils

previous_time = 0
current_time = 0

# Get capture device
cap = cv2.VideoCapture(0)

# Create 'Hand' object
hands = mp_hands.Hands()

while True:
    success, img = cap.read()

    # Flip img
    img = cv2.flip(img, 1)

    # Convert img from BGR to RGB
    img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    # Process img
    results = hands.process(img_rgb)

    # Check if results contain multiple hands
    if results.multi_hand_landmarks:
        # Iterate over each hand landmarks
        for hand_landmarks in results.multi_hand_landmarks:
            # Get id and landmark
            for id, landmark in enumerate(hand_landmarks.landmark):
                # Get height, width, and channel of img
                h, w, c = img.shape

                # Find position
                cx, cy = int(landmark.x * w), int(landmark.y * h)

                print(id, cx, cy)

                if id == 8:
                    cv2.circle(img, (cx, cy), 15, (255, 0, 255), cv2.FILLED)

            mp_draw.draw_landmarks(
                img,
                hand_landmarks,
                mp_hands.HAND_CONNECTIONS,
            )

    # Get FPS
    current_time = time.time()
    fps = 1 / (current_time - previous_time)
    previous_time = current_time

    # Display FPS
    cv2.putText(
        img=img,
        text=str(int(fps)),
        org=(10, 40),
        fontFace=cv2.QT_FONT_NORMAL,
        fontScale=1,
        color=(255, 255, 255),
        thickness=2
    )

    # Show image on screen
    # arg: 'Track hand' -> The title of the window
    # arg: 'img' -> The image to display
    cv2.imshow('Track Hand', img)

    # Check if user press letter 'q'
    # True -> Break from loop
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break
