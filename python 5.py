import cv2
import numpy as np
import mediapipe as mp
import os
import urllib.request

from mediapipe.tasks import python
from mediapipe.tasks.python import vision


# ==========================================
# 1. DOWNLOAD HAND MODEL
# ==========================================

MODEL_URL = (
    "https://storage.googleapis.com/"
    "mediapipe-models/hand_landmarker/"
    "hand_landmarker/float16/1/"
    "hand_landmarker.task"
)

MODEL_PATH = "hand_landmarker.task"

if not os.path.exists(MODEL_PATH):

    print("Downloading hand model...")

    urllib.request.urlretrieve(
        MODEL_URL,
        MODEL_PATH
    )

    print("Model downloaded successfully!")


# ==========================================
# 2. START WEBCAM
# ==========================================

cap = cv2.VideoCapture(0)

if not cap.isOpened():

    print("Cannot access webcam")
    exit()


# ==========================================
# 3. DRAWING SETTINGS
# ==========================================

canvas = None

color = (0, 0, 255)

thickness = 5

prev_x = None
prev_y = None

show_shapes = False


# ==========================================
# 4. MEDIAPIPE HAND LANDMARKER
# ==========================================

base_options = python.BaseOptions(
    model_asset_path=MODEL_PATH
)

options = vision.HandLandmarkerOptions(

    base_options=base_options,

    running_mode=vision.RunningMode.VIDEO,

    num_hands=1,

    min_hand_detection_confidence=0.7,

    min_hand_presence_confidence=0.7,

    min_tracking_confidence=0.7

)

landmarker = vision.HandLandmarker.create_from_options(
    options
)


# ==========================================
# 5. HAND CONNECTIONS
# ==========================================

CONNECTIONS = [

    (0, 1), (1, 2), (2, 3), (3, 4),

    (0, 5), (5, 6), (6, 7), (7, 8),

    (5, 9), (9, 10), (10, 11), (11, 12),

    (9, 13), (13, 14), (14, 15), (15, 16),

    (13, 17), (17, 18), (18, 19), (19, 20),

    (0, 17)

]


# ==========================================
# 6. DRAW HAND LANDMARKS
# ==========================================

def draw_hand(frame, landmarks):

    h, w, _ = frame.shape

    points = []

    for landmark in landmarks:

        x = int(landmark.x * w)

        y = int(landmark.y * h)

        points.append((x, y))

        cv2.circle(
            frame,
            (x, y),
            4,
            (0, 255, 0),
            -1
        )

    for start, end in CONNECTIONS:

        cv2.line(
            frame,
            points[start],
            points[end],
            (255, 255, 0),
            2
        )


# ==========================================
# 7. SHAPE RECOGNITION
# ==========================================

def recognize_shapes(canvas):

    gray = cv2.cvtColor(
        canvas,
        cv2.COLOR_BGR2GRAY
    )

    _, thresh = cv2.threshold(
        gray,
        50,
        255,
        cv2.THRESH_BINARY
    )

    contours, _ = cv2.findContours(

        thresh,

        cv2.RETR_EXTERNAL,

        cv2.CHAIN_APPROX_SIMPLE

    )

    output = canvas.copy()

    for contour in contours:

        area = cv2.contourArea(contour)

        if area < 500:

            continue

        perimeter = cv2.arcLength(
            contour,
            True
        )

        approx = cv2.approxPolyDP(
            contour,
            0.04 * perimeter,
            True
        )

        corners = len(approx)

        if corners == 3:

            shape = "Triangle"

        elif corners == 4:

            x, y, w, h = cv2.boundingRect(
                contour
            )

            ratio = w / float(h)

            if 0.85 <= ratio <= 1.15:

                shape = "Square"

            else:

                shape = "Rectangle"

        elif corners > 6:

            shape = "Circle"

        else:

            shape = "Unknown"

        cv2.drawContours(

            output,

            [contour],

            -1,

            (0, 255, 255),

            2

        )

        x, y, w, h = cv2.boundingRect(
            contour
        )

        cv2.putText(

            output,

            shape,

            (x, max(y - 10, 20)),

            cv2.FONT_HERSHEY_SIMPLEX,

            0.7,

            (0, 255, 255),

            2

        )

    return output


# ==========================================
# 8. MAIN LOOP
# ==========================================

frame_timestamp = 0


while True:

    ret, frame = cap.read()

    if not ret:

        print("Cannot read webcam")

        break

    frame = cv2.flip(frame, 1)

    if canvas is None:

        canvas = np.zeros_like(frame)

    h, w, _ = frame.shape

    rgb_frame = cv2.cvtColor(

        frame,

        cv2.COLOR_BGR2RGB

    )

    mp_image = mp.Image(

        image_format=mp.ImageFormat.SRGB,

        data=rgb_frame

    )

    frame_timestamp += 33

    detection_result = landmarker.detect_for_video(

        mp_image,

        frame_timestamp

    )

    hand_found = False

    if detection_result.hand_landmarks:

        hand_found = True

        landmarks = detection_result.hand_landmarks[0]

        draw_hand(
            frame,
            landmarks
        )

        # Index finger landmarks
        index_tip = landmarks[8]

        index_pip = landmarks[6]

        x = int(index_tip.x * w)

        y = int(index_tip.y * h)

        if 0 <= x < w and 0 <= y < h:

            # Index finger up
            index_up = index_tip.y < index_pip.y

            if index_up:

                if prev_x is not None:

                    cv2.line(

                        canvas,

                        (prev_x, prev_y),

                        (x, y),

                        color,

                        thickness

                    )

                prev_x = x

                prev_y = y

            else:

                prev_x = None

                prev_y = None

    else:

        prev_x = None

        prev_y = None

    # ======================================
    # DISPLAY RESULT
    # ======================================

    result = cv2.add(
        frame,
        canvas
    )

    if show_shapes:

        result = recognize_shapes(result)

    cv2.putText(

        result,

        "Index Finger: Draw",

        (10, 30),

        cv2.FONT_HERSHEY_SIMPLEX,

        0.6,

        (255, 255, 255),

        2

    )

    cv2.putText(

        result,

        "C: Clear | S: Shapes | Q: Quit",

        (10, 60),

        cv2.FONT_HERSHEY_SIMPLEX,

        0.6,

        (255, 255, 255),

        2

    )

    cv2.putText(

        result,

        "R: Red | G: Green | B: Blue",

        (10, 90),

        cv2.FONT_HERSHEY_SIMPLEX,

        0.6,

        (255, 255, 255),

        2

    )

    cv2.imshow(

        "AI Virtual Drawing Board",

        result

    )

    key = cv2.waitKey(1) & 0xFF

    # ======================================
    # KEYBOARD CONTROLS
    # ======================================

    if key == ord('c'):

        canvas = np.zeros_like(frame)

        prev_x = None

        prev_y = None

    elif key == ord('r'):

        color = (0, 0, 255)

    elif key == ord('g'):

        color = (0, 255, 0)

    elif key == ord('b'):

        color = (255, 0, 0)

    elif key == ord('s'):

        show_shapes = not show_shapes

    elif key == ord('q'):

        break


# ==========================================
# 9. RELEASE RESOURCES
# ==========================================

cap.release()

landmarker.close()

cv2.destroyAllWindows()
