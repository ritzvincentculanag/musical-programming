# General imports
import mediapipe as mp
import cv2
import time
import os


class TrackHand:
    def __init__(
            self,
            mode=False,
            max_hands=2,
            detection_confidence=0.5,
            track_confidence=0.5
    ):
        self.mode = mode
        self.max_hands = max_hands
        self.detection_confidence = detection_confidence
        self.track_confidence = track_confidence

        # Prepare needed modules
        self.mp_hands = mp.solutions.hands
        self.mp_draw = mp.solutions.drawing_utils

        # Create 'Hand' object
        self.hands = self.mp_hands.Hands(
            self.mode,
            self.max_hands,
            self.detection_confidence,
            self.track_confidence
        )

    def find_hands(self, img, draw=True):
        # Flip img
        img = cv2.flip(img, 1)

        # Convert img from BGR to RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Process img
        results = self.hands.process(img_rgb)

        # Check if results contain multiple hands
        if results.multi_hand_landmarks:
            # Iterate over each hand landmarks
            for hand_landmarks in results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(
                        img,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS,
                    )

                # Get id and landmark
                # for id, landmark in enumerate(hand_landmarks.landmark):
                #     # Get height, width, and channel of img
                #     h, w, c = img.shape
                #
                #     # Find position
                #     cx, cy = int(landmark.x * w), int(landmark.y * h)
                #
                #     print(id, cx, cy)





def main():
    # Get capture device
    cap = cv2.VideoCapture(0)

    # Declare variables for FPS
    previous_time = 0
    current_time = 0

    while True:
        success, img = cap.read()

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


if __name__ == '__main__':
    main()
