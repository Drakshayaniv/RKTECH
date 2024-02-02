import cv2
import mediapipe as mp
import pyautogui

# points on index and thumb
x1 = y1 = x2 = y2 = 0
# to use webcam
webcam = cv2.VideoCapture(0)
# recognize hands
my_hands = mp.solutions.hands.Hands()
# to draw points on hand
drawing_utils = mp.solutions.drawing_utils
while True:
    # to read image using cv2
    _, image = webcam.read()
    # to flip the image
    image = cv2.flip(image, 1)
    frame_height, frame_width, _ = image.shape
    rgb_image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    output = my_hands.process(rgb_image)
    # multiple hands
    hands = output.multi_hand_landmarks
    if hands:
        for hand in hands:
            drawing_utils.draw_landmarks(image, hand)
            landmarks = hand.landmark
            for ids, landmark in enumerate(landmarks):
                # to take x and y points from frame
                x = int(landmark.x * frame_width)
                y = int(landmark.y * frame_height)
                # id == 8  denotes index finger
                if ids == 8:
                    cv2.circle(img=image, center=(x, y), radius=8, color=(255, 0, 0), thickness=3)
                    x1 = x
                    y1 = y
                # ids==4 denotes thumb finger
                if ids == 4:
                    cv2.circle(img=image, center=(x, y), radius=8, color=(255, 0, 0), thickness=3)
                    x2 = x
                    y2 = y
        # to calculate distance between index and thumb finger to increase\decrease the volume
        dist = ((x2 - x1) ** 2 + (y2 - y1) ** 2) ** 0.5 // 4
        cv2.line(image, (x1, y1), (x2, y2), (255, 255, 255), 2)
        if dist > 49:
            pyautogui.press("volumeup")
        else:
            pyautogui.press("volumedown")
    cv2.imshow("Volume Control Using Hand-Gestures", image)
    key = cv2.waitKey(10)
    # to stop execution press 1(ASCII of 1 is 49)
    if key == 49:
        break
webcam.release()
cv2.destroyAllWindows()
