import cv2
import mediapipe as mp
import numpy as np
import serial
import time

# 시리얼 포트 설정 (본인 환경에 맞게 수정)
ser = serial.Serial('/dev/tty.usbmodem1301', 9600)
time.sleep(2)  # 아두이노 초기화 시간

# MediaPipe 초기화
cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

finger_joint_sets = [
    (5, 6, 8),    # 검지
    (9, 10, 12),  # 중지
    (13, 14, 16),  # 약지
    (17, 18, 20),  # 새끼
]

# 각도 계산 함수


def calc_angle(a, b, c):
    ba = np.array([a.x - b.x, a.y - b.y, a.z - b.z])
    bc = np.array([c.x - b.x, c.y - b.y, c.z - b.z])
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba)
                                     * np.linalg.norm(bc) + 1e-6)
    angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
    return np.degrees(angle)

# 손이 펴졌는지 판단


def is_hand_open_by_angle(hand_landmarks, threshold=160):

    extended_fingers = 0

    for mcp, pip, tip in finger_joint_sets:
        angle = calc_angle(
            hand_landmarks.landmark[mcp],
            hand_landmarks.landmark[pip],
            hand_landmarks.landmark[tip]
        )
        if angle > threshold:
            extended_fingers += 1

    return extended_fingers >= 3


def calculate_hand_fold_degree(hand_landmarks):
    angles = []

    for mcp, pip, tip in finger_joint_sets:
        angle = calc_angle(
            hand_landmarks.landmark[mcp],
            hand_landmarks.landmark[pip],
            hand_landmarks.landmark[tip]
        )
        angles.append(angle)

    avg_angle = np.mean(angles)

    return int(avg_angle)


# 메인 루프
prev_state = None

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    label = ""
    fold_degree = 180

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            is_open = is_hand_open_by_angle(hand_landmarks)
            label = "open" if is_open else "close"

            # if label != prev_state:
            # ser.write(label.encode())
            # prev_state = label

            mp_drawing.draw_landmarks(
                frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

            fold_degree = calculate_hand_fold_degree(hand_landmarks)

    # TODO : 40~180도를 0~90도로 정규화
    norm_fold_degree = int((1-max((fold_degree - 40), 0) / 140) * 90)

    cv2.putText(frame, label, (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
    cv2.putText(frame, f"Fold Degree: {fold_degree}", (30, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)
    cv2.putText(frame, f"Norm Fold Degree: {norm_fold_degree}", (30, 150),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

    cv2.imshow("Hand Control", frame)

    if cv2.waitKey(1) & 0xFF == 27:
        break

    if ser.in_waiting > 0:
        line = ser.readline().decode().strip()
        if line == "ready":
            ser.write(f"{norm_fold_degree}\n".encode())
            print(norm_fold_degree)
        else:
            print(line)

cap.release()
ser.close()
cv2.destroyAllWindows()
