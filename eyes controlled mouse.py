import cv2
import mediapipe as mp
import pyautogui
import numpy as np

frame_width = 640
frame_height = 480

cam = cv2.VideoCapture(0)
cam.set(3, frame_width)
cam.set(4, frame_height)

face_mesh = mp.solutions.face_mesh.FaceMesh(refine_landmarks=True)
screen_w, screen_h = pyautogui.size()

_, frame = cam.read()
frame_h, frame_w, _ = frame.shape

frame_count = 0
frame_skip = 3

click_counter = 0
click_threshold = 30

cursor_size = 50

def draw_big_cursor(frame, x, y, size):
    cv2.circle(frame, (x, y), size, (0, 255, 0), -1)

def draw_eye(frame, landmarks, eye_indices):
    eye_points = np.array([(int(landmarks[i].x * frame_w), int(landmarks[i].y * frame_h)) for i in eye_indices])
    cv2.polylines(frame, [eye_points], isClosed=True, color=(0, 255, 0), thickness=2)

while True:
    _, frame = cam.read()
    frame_count += 1

    if frame_count % frame_skip != 0:
        continue

    frame = cv2.flip(frame, 1)

    small_frame = cv2.resize(frame, (0, 0), fx=5.5, fy=5.5)

    rgb_frame = cv2.cvtColor(small_frame, cv2.COLOR_BGR2RGB)
    output = face_mesh.process(rgb_frame)

    landmark_points = output.multi_face_landmarks

    if landmark_points:
        landmarks = landmark_points[0].landmark


        for id, landmark in enumerate(landmarks[474:478]):
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)
            cv2.circle(frame, (x, y), 3, (0, 255, 0))

            if id == 1:
                screen_x = int(screen_w * landmark.x)
                screen_y = int(screen_h * landmark.y)
                pyautogui.moveTo(screen_x, screen_y)

        left_eye_landmarks = [landmarks[145], landmarks[159]]
        for landmark in left_eye_landmarks:
            x = int(landmark.x * frame_w)
            y = int(landmark.y * frame_h)

            x = max(0, min(x, frame_width - 1))
            y = max(0, min(y, frame_height - 1))

            cv2.circle(frame, (x, y), 3, (0, 255, 255))


        draw_eye(frame, landmarks, list(range(145, 161)))

        draw_big_cursor(frame, x, y, cursor_size)

        blink_distance = left_eye_landmarks[1].y - left_eye_landmarks[0].y
        if blink_distance < 0.02 and click_counter == 0:
            pyautogui.click()

        click_counter = 0
        click_threshold = 30

    cv2.imshow('Eye Controlled Mouse', frame)
    cv2.waitKey(1)