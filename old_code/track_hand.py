# General imports
import mediapipe as mp
import cv2
import time


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
            static_image_mode=self.mode,
            max_num_hands=self.max_hands,
            min_detection_confidence=self.detection_confidence,
            min_tracking_confidence=self.track_confidence
        )

        self.results = None

    def find_hands(self, img, draw=True):
        # Flip img
        img = cv2.flip(img, 1)

        # Convert img from BGR to RGB
        img_rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Process img
        self.results = self.hands.process(img_rgb)

        # Check if results contain multiple hands
        if self.results.multi_hand_landmarks:
            # Iterate over each hand landmarks
            for hand_landmarks in self.results.multi_hand_landmarks:
                if draw:
                    self.mp_draw.draw_landmarks(
                        img,
                        hand_landmarks,
                        self.mp_hands.HAND_CONNECTIONS,
                    )

        return img

    def find_position(self, img, hand_number=0, draw=True):
        # Create landmark list
        landmarks = []

        # Check if results contain multiple hands
        if self.results.multi_hand_landmarks:
            # Get hand
            hand = self.results.multi_hand_landmarks[hand_number]

            # Get id and landmark
            for id, landmark in enumerate(hand.landmark):
                # Get height, width, and channel of img
                h, w, c = img.shape

                # Find and add position
                cx, cy = int(landmark.x * w), int(landmark.y * h)
                landmarks.append([id, cx, cy])

                if draw:
                    cv2.circle(img, (cx, cy), 5, (255, 0, 255), cv2.FILLED)

        return landmarks


def main():
    # Get capture device
    cap = cv2.VideoCapture(0)

    # Declare variables for FPS
    previous_time = 0
    current_time = 0

    detector = TrackHand()

    while True:
        success, img = cap.read()
        img = detector.find_hands(img)
        landmarks = detector.find_position(img)
        if len(landmarks) != 0:
            print(landmarks[4])

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
