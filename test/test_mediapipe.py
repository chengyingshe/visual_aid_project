import _init_path
from camera.utils import *
import mediapipe as mp
import cv2

mp_hands = mp.solutions.hands
hands = mp_hands.Hands()
cap = cv2.VideoCapture(0)

while cap.isOpened():
    # 读取摄像头帧
    ret, frame = cap.read()
    if not ret:
        break
    
    # 转换帧颜色为 RGB
    frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    
    # 检测手部
    results = hands.process(frame_rgb)
    
    if results.multi_hand_landmarks:
        # 遍历检测到的每只手
        index_finger_pos = []
        for hand_landmarks in results.multi_hand_landmarks:
            # 获取食指的坐标
            index_finger = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP]
            x = int(index_finger.x * frame.shape[1])
            y = int(index_finger.y * frame.shape[0])
            cv2.circle(frame, (x, y), 5, (0, 0, 255), -1)
            index_finger_pos.append((x, y))
        if len(index_finger_pos) == 2 and \
                index_finger_pos[0][0] != index_finger_pos[1][0] and index_finger_pos[0][1] != index_finger_pos[1][1]:
            cv2.rectangle(frame, index_finger_pos[0], index_finger_pos[1], (0, 255, 0), 2)
            cropped_image = crop_image_from(frame, index_finger_pos)
            cv2.imshow('Cropped Image', cropped_image)

    # 显示帧
    cv2.imshow('Hand Detection', frame)
    
    # 检测按键输入
    if cv2.waitKey(10) & 0xFF == ord('q'):
        break

# 释放摄像头并关闭窗口
cap.release()
cv2.destroyAllWindows()