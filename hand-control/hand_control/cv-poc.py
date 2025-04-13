import cv2
import mediapipe as mp
import numpy as np

# 초기화
cap = cv2.VideoCapture(0)
mp_hands = mp.solutions.hands
mp_drawing = mp.solutions.drawing_utils

hands = mp_hands.Hands(
    max_num_hands=1,
    min_detection_confidence=0.7,
    min_tracking_confidence=0.7
)

# 각도 계산 함수
def calc_angle(a, b, c):
    ba = np.array([a.x - b.x, a.y - b.y, a.z - b.z])
    bc = np.array([c.x - b.x, c.y - b.y, c.z - b.z])
    cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-6)
    angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
    return np.degrees(angle)

# 손이 펴졌는지 판단 (각도 기반)
def is_hand_open_by_angle(hand_landmarks, threshold=160):
    finger_joint_sets = [
        (5, 6, 8),    # 검지
        (9, 10, 12),  # 중지
        (13, 14, 16), # 약지
        (17, 18, 20), # 새끼
    ]

    extended_fingers = 0

    for mcp, pip, tip in finger_joint_sets:
        angle = calc_angle(
            hand_landmarks.landmark[mcp],
            hand_landmarks.landmark[pip],
            hand_landmarks.landmark[tip]
        )
        # 디버깅 출력
        print(f"Finger {pip} angle: {angle:.2f}")
        if angle > threshold:
            extended_fingers += 1

    return extended_fingers >= 3  # 대부분 손가락이 펴져 있으면 손을 폈다고 판단

# 메인 루프
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    result = hands.process(rgb)

    label = ""

    if result.multi_hand_landmarks:
        for hand_landmarks in result.multi_hand_landmarks:
            if is_hand_open_by_angle(hand_landmarks):
                label = "open hand"
            else:
                label = "close hand"

            # 손 랜드마크 그리기
            mp_drawing.draw_landmarks(frame, hand_landmarks, mp_hands.HAND_CONNECTIONS)

    # 상태 텍스트 표시
    cv2.putText(frame, label, (30, 50),
                cv2.FONT_HERSHEY_SIMPLEX, 1.2, (0, 255, 0), 3)

    cv2.imshow("Hand Pose Detection (Angle-Based)", frame)

    if cv2.waitKey(1) & 0xFF == 27:  # ESC 키로 종료
        break

cap.release()
cv2.destroyAllWindows()