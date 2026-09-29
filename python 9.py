import cv2

cap = cv2.VideoCapture(0)

flip_mode = None  # None, 0 (vertical), 1 (horizontal), -1 (both)

def on_click(event, x, y, flags, param):
    global flip_mode
    if event == cv2.EVENT_LBUTTONDOWN:
        # Cycle: None -> horizontal -> vertical -> both -> None
        if flip_mode is None:
            flip_mode = 1
        elif flip_mode == 1:
            flip_mode = 0
        elif flip_mode == 0:
            flip_mode = -1
        else:
            flip_mode = None

cv2.namedWindow("Webcam")
cv2.setMouseCallback("Webcam", on_click)

while True:
    ret, frame = cap.read()
    if not ret:
        break

    if flip_mode is not None:
        frame = cv2.flip(frame, flip_mode)

    label = {None: "Normal", 1: "Horizontal", 0: "Vertical", -1: "Both"}[flip_mode]
    cv2.putText(frame, label, (10, 30), cv2.FONT_HERSHEY_SIMPLEX,
                1, (0, 255, 0), 2)

    cv2.imshow("Webcam", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
