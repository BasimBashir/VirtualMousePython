import cv2
import mediapipe as mp
import pyautogui

cap = cv2.VideoCapture(0)       # for video capturing
hand_detector = mp.solutions.hands.Hands()  # for detecting hands
drawing_utils = mp.solutions.drawing_utils  # for drawing points on hand
screen_width, screen_height = pyautogui.size()  # to get the display's width and height
index_y = 0  # initializing to a value as 0 it will change after loop runs

while True:
    _, frame = cap.read()                      # only need frame or 2nd var so that's why using _
    frame = cv2.flip(frame, 1)                 # to get non-mirrored effect of window
    frame_height, frame_width, _ = frame.shape           # getting width and height from frame(output video window)
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)   # converting BGR to RGB
    output = hand_detector.process(rgb_frame)            # getting the hand detection from frame
    hands = output.multi_hand_landmarks                  # assigning detected landmarks to a var
    if hands:                                            # if hands gets detected
        for hand in hands:                               # draw the loop on fingers in hand
            drawing_utils.draw_landmarks(frame, hand)    # drawing landmarks on fingers
            landmarks = hand.landmark                    # storing to another var
            for id, landmark in enumerate(landmarks):    # getting landmarks as tuple return in id and landmark
                x = int(landmark.x * frame_width)        # setting the landmarks to a position on screen
                y = int(landmark.y * frame_height)

                if id == 8:  # Index finger id
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255), thickness=2)  # encircle finger
                    index_x = screen_width/frame_width * x
                    index_y = screen_height/frame_height * y
                    pyautogui.moveTo(index_x, index_y)         # getting the effect of moving finger as cursor movement

                if id == 12:  # middle id  (change this if you want another finger{can google hand landmarks to change})
                    cv2.circle(img=frame, center=(x, y), radius=10, color=(0, 255, 255), thickness=3)
                    thumb_x = screen_width/frame_width * x
                    thumb_y = screen_height/frame_height * y
                    print('Outside', abs(index_y - thumb_y))

                    if abs(index_y - thumb_y) < 20:    # getting the absolute diff of both fingers getting closed in px
                        pyautogui.click()       # click happens if it gets closed
                        pyautogui.sleep(1)

    cv2.imshow('Virtual Mouse', frame)
    keyCode = cv2.waitKey(1)

    if cv2.getWindowProperty('Virtual Mouse', cv2.WND_PROP_VISIBLE) < 1:
        break

cv2.destroyAllWindows()
