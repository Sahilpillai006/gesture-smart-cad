import cv2
import mediapipe as mp
import numpy as np
import math

# ---------------- INIT ----------------
mp_hands = mp.solutions.hands
hands = mp_hands.Hands(max_num_hands=2)
mp_draw = mp.solutions.drawing_utils

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 720)

# ---------------- CONSTANTS ----------------
ERASE_RADIUS = 30
MIN_POINTS = 40
CLOSE_THRESH = 30
DEPTH = 200

FOCAL_LEN = 900
CAM_DIST = 600

# ---------------- DATA ----------------
current_path = []
shapes = []  # each: {base, scale, offset, rotation}

prev_two_hand_dist = None
prev_mid = None
prev_angle = None

# ---------------- UTILS ----------------
def dist(a, b):
    return math.hypot(a[0] - b[0], a[1] - b[1])

def angle_between(p1, p2):
    return math.atan2(p2[1] - p1[1], p2[0] - p1[0])

def fingers_up(hand):
    lm = hand.landmark
    tips = [8, 12, 16, 20]
    return [1 if lm[t].y < lm[t - 2].y else 0 for t in tips]

def hand_pinch(lm, w, h, thresh=35):
    ix, iy = int(lm[8].x * w), int(lm[8].y * h)
    tx, ty = int(lm[4].x * w), int(lm[4].y * h)
    return dist((ix, iy), (tx, ty)) < thresh

# ---------------- PROJECTION ----------------
def project_point(x, y, z, cx, cy):
    px = int(cx + (x * FOCAL_LEN) / (z + CAM_DIST))
    py = int(cy + (y * FOCAL_LEN) / (z + CAM_DIST))
    return px, py

# ---------------- ERASE ----------------
def erase_shape(shape, center):
    new_base = [p for p in shape["base"] if dist(p, center) > ERASE_RADIUS]
    return new_base if len(new_base) >= 3 else None

# ---------------- MAIN LOOP ----------------
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    res = hands.process(rgb)

    # ---------------- ONE HAND ----------------
    if res.multi_hand_landmarks and len(res.multi_hand_landmarks) == 1:
        hand = res.multi_hand_landmarks[0]
        mp_draw.draw_landmarks(frame, hand, mp_hands.HAND_CONNECTIONS)

        lm = hand.landmark
        ix, iy = int(lm[8].x * w), int(lm[8].y * h)
        fingers = fingers_up(hand)

        draw_mode = fingers == [1, 0, 0, 0]
        erase_mode = fingers == [1, 1, 0, 0]

        if draw_mode:
            current_path.append((ix, iy))
        else:
            if len(current_path) > MIN_POINTS:
                if dist(current_path[0], current_path[-1]) < CLOSE_THRESH:
                    shapes.append({
                        "base": current_path.copy(),
                        "scale": 1.0,
                        "offset": [0, 0],
                        "rotation": 0.0
                    })
            current_path = []

        if erase_mode:
            new_shapes = []
            for s in shapes:
                cleaned = erase_shape(s, (ix, iy))
                if cleaned:
                    s["base"] = cleaned
                    new_shapes.append(s)
            shapes = new_shapes
            cv2.circle(frame, (ix, iy), ERASE_RADIUS, (0, 0, 255), 2)

    # ---------------- TWO HANDS ----------------
    elif res.multi_hand_landmarks and len(res.multi_hand_landmarks) == 2 and shapes:
        hand1, hand2 = res.multi_hand_landmarks
        mp_draw.draw_landmarks(frame, hand1, mp_hands.HAND_CONNECTIONS)
        mp_draw.draw_landmarks(frame, hand2, mp_hands.HAND_CONNECTIONS)

        lm1, lm2 = hand1.landmark, hand2.landmark
        x1, y1 = int(lm1[8].x * w), int(lm1[8].y * h)
        x2, y2 = int(lm2[8].x * w), int(lm2[8].y * h)

        curr_dist = dist((x1, y1), (x2, y2))
        mid_x, mid_y = (x1 + x2) // 2, (y1 + y2) // 2
        curr_angle = angle_between((x1, y1), (x2, y2))

        pinch1 = hand_pinch(lm1, w, h)
        pinch2 = hand_pinch(lm2, w, h)

        shape = shapes[-1]

        # SCALE
        if prev_two_hand_dist is not None:
            sf = curr_dist / prev_two_hand_dist
            shape["scale"] *= sf
            shape["scale"] = max(0.2, min(shape["scale"], 3.0))
        prev_two_hand_dist = curr_dist

        # DRAG
        if pinch1 and pinch2:
            if prev_mid is not None:
                dx = mid_x - prev_mid[0]
                dy = mid_y - prev_mid[1]
                shape["offset"][0] += dx
                shape["offset"][1] += dy
            prev_mid = (mid_x, mid_y)
        else:
            prev_mid = None

        # ROTATE
        if prev_angle is not None:
            shape["rotation"] += (curr_angle - prev_angle)
        prev_angle = curr_angle

    else:
        prev_two_hand_dist = None
        prev_mid = None
        prev_angle = None

    # ---------------- DRAW CURRENT PATH ----------------
    for i in range(1, len(current_path)):
        cv2.line(frame, current_path[i - 1], current_path[i], (0, 200, 0), 2)

    # ---------------- TRUE 3D DRAW ----------------
    for s in shapes:
        base = s["base"]
        scale = s["scale"]
        ox, oy = s["offset"]
        rot = s["rotation"]

        cx0 = sum(p[0] for p in base) / len(base)
        cy0 = sum(p[1] for p in base) / len(base)

        cos_r, sin_r = math.cos(rot), math.sin(rot)

        def transform(x, y):
            x -= cx0
            y -= cy0
            x, y = x * scale, y * scale
            x, y = x * cos_r - y * sin_r, x * sin_r + y * cos_r
            return x + ox, y + oy

        top_3d = [( *transform(x, y), 0 ) for x, y in base]
        bot_3d = [( *transform(x, y), DEPTH ) for x, y in base]

        top_2d = [project_point(x, y, z, int(cx0), int(cy0)) for x, y, z in top_3d]
        bot_2d = [project_point(x, y, z, int(cx0), int(cy0)) for x, y, z in bot_3d]

        for i in range(len(top_2d)):
            cv2.line(frame, top_2d[i], top_2d[(i + 1) % len(top_2d)], (0, 255, 0), 2)
            cv2.line(frame, bot_2d[i], bot_2d[(i + 1) % len(bot_2d)], (255, 255, 0), 2)
            cv2.line(frame, top_2d[i], bot_2d[i], (255, 0, 255), 2)

    # ---------------- UI ----------------
    cv2.putText(
        frame,
        "1 Hand: Draw | 2 Hands: Scale + Drag + Rotate | TRUE 3D",
        (20, 40),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.8, (255, 255, 255), 2
    )

    cv2.imshow("Gesture Smart CAD – Final", frame)

    key = cv2.waitKey(1)
    if key == 27:
        break
    elif key == ord('r'):
        shapes.clear()
        current_path.clear()

cap.release()
cv2.destroyAllWindows()