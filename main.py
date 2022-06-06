# General imports
import mediapipe as mp
import numpy as np
import cv2
import uuid
import os

# Selective imports
from pydub import AudioSegment
from pydub.playback import play

# Get sound
sound = AudioSegment.from_mp3('./assets/ting.mp3')

# Prepare things
mp_drawing = mp.solutions.drawing_utils
mp_hands = mp.solutions.hands

# Get video capture device
cap = cv2.VideoCapture(0)

# Create images folder
os.mkdir('images')

# Use Hands in the mp+hands variable with minimum tracking confidence of 50% and
# Minimum detection confidence of 80% and name it as `hands`.
with mp_hands.Hands(min_tracking_confidence=0.8, min_detection_confidence=0.5) as hands:

    while cap.isOpened():
        ret, frame = cap.read()

        # BGR 2 RGB
        image = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        image = cv2.flip(image, 1)
        image.flags.writeable = False

        # Render
        results = hands.process(image)

        # RGB 2 BGR

        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)

        print(results)

        # Rendering results
        if results.multi_hand_landmarks:
            for num, hand in enumerate(results.multi_hand_landmarks):
                mp_drawing.draw_landmarks(image, hand, mp_hands.HAND_CONNECTIONS)

        # Save image
        cv2.imwrite(os.path.join('images', '{}.jpg'.format(uuid.uuid1())), image)

        cv2.imshow('Hand Tracking', image)

        if cv2.waitKey(10) & 0xFF == ord('q'):
            break

cap.release()
cv2.destroyAllWindows()

