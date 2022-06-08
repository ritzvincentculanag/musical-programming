# General imports
import os.path

import mediapipe as mp
import cv2 as cv
import pygame
import cvzone
import uuid
import os


class Tracker:

    def __init__(
            self,
            mode=False,
            max_hands=2,
            confidence_detection=0.5,
            confidence_tracking=0.5
    ):
        # Hands settings
        self.mode = mode
        self.max_hands = max_hands
        self.confidence_tracking = confidence_tracking
        self.confidence_detection = confidence_detection

        # Mediapipe settings
        self.mp_hands = mp.solutions.hands
        self.mp_drawing = mp.solutions.drawing_utils

        # Tracker settings
        self.results = None
        self.hands = self.mp_hands.Hands(
            static_image_mode=self.mode,
            max_num_hands=self.max_hands,
            min_detection_confidence=self.confidence_detection,
            min_tracking_confidence=self.confidence_tracking,
        )

        # Camera settings
        self.cap = cv.VideoCapture(0)

        # Pygame mixer settings
        self.mixer = pygame.mixer
        self.mixer.init()

    def track_hand(self):
        success, image = self.cap.read()

        # To improve performance
        image.flags.writeable = False
        image = cv.cvtColor(image, cv.COLOR_BGR2RGB)
        self.results = self.hands.process(image)

        # Draw hand annotations to image
        image.flags.writeable = True
        image = cv.cvtColor(image, cv.COLOR_RGB2BGR)
        if self.results.multi_hand_landmarks:
            for hand_landmarks in self.results.multi_hand_landmarks:
                self.mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    self.mp_hands.HAND_CONNECTIONS
                )

        return image

    def track_position(self, img_to_track):
        landmarks = []

        if self.results.multi_hand_landmarks:
            hand = self.results.multi_hand_landmarks[0]

            for lid, landmark in enumerate(hand.landmark):
                h, w, c = img_to_track.shape

                cx, cy = int(landmark.x * w), int(landmark.y * h)
                landmarks.append([lid, cx, cy])

        return landmarks


if __name__ == '__main__':
    tracker = Tracker()
    tracker.track_hand()

    # Create folder to store pictures
    if os.path.isdir('captures'):
        print('directory exists')
    else:
        os.mkdir('captures')

    # Note sounds
    c_note = tracker.mixer.Sound('../assets/c.mp3')
    d_note = tracker.mixer.Sound('../assets/d.mp3')
    e_note = tracker.mixer.Sound('../assets/e.mp3')
    f_note = tracker.mixer.Sound('../assets/f.mp3')
    g_note = tracker.mixer.Sound('../assets/g.mp3')
    a_note = tracker.mixer.Sound('../assets/a.mp3')

    # Filters
    img_filter = tracker.track_hand()
    cloud = cv.imread('../images/cloud.png', cv.IMREAD_UNCHANGED)
    capture_sound = tracker.mixer.Sound('../assets/shutter.mp3')

    img_h, img_w, img_c = img_filter.shape
    cloud_h, cloud_w, cloud_c = cloud.shape

    while True:
        img = tracker.track_hand()
        img_landmarks = tracker.track_position(img)

        if img_landmarks:
            # Finger tips
            thumb_tip = img_landmarks[4]
            index_tip = img_landmarks[8]
            middle_tip = img_landmarks[12]
            ring_tip = img_landmarks[16]
            pinky_tip = img_landmarks[20]

            # Finger dips
            thumb_dip = img_landmarks[3]
            index_dip = img_landmarks[6]
            middle_dip = img_landmarks[10]
            ring_dip = img_landmarks[14]
            pinky_dip = img_landmarks[18]

            # Notes
            c = thumb_tip[1] < thumb_dip[1]
            d = index_tip[2] > index_dip[2]
            e = middle_tip[2] > middle_dip[2]
            f = ring_tip[2] > ring_dip[2]
            g = pinky_tip[2] > pinky_dip[2]
            a = d and e and f and g

            # Hand signs
            peace = c and f and g

            if a:
                a_note.play()
            elif peace:
                img = cvzone.overlayPNG(img, cloud, [0, 0])
                cv.imshow('Tracker', cv.flip(img, 1))
                cv.imwrite(os.path.join('captures', '{}.jpg').format(uuid.uuid1()), cv.flip(img, 1))

                capture_sound.play()

                cv.waitKey(1000)
            elif d:
                d_note.play()
            elif e:
                e_note.play()
            elif f:
                f_note.play()
            elif g:
                g_note.play()
            elif c:
                c_note.play()

        cv.imshow('Tracker', cv.flip(img, 1))
        if cv.waitKey(10) & 0xFF == ord('q'):
            break

    tracker.cap.release()
    cv.destroyAllWindows()
