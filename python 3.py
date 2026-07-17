import cv2
import numpy as np

# Create a white image
img = np.ones((500, 700, 3), dtype=np.uint8) * 255
temp = img.copy()

drawing = False
start_x, start_y = -1, -1

# Mouse callback function
def draw_rectangle(event, x, y, flags, param):
    global drawing, start_x, start_y, img, temp

    # Left mouse button pressed
    if event == cv2.EVENT_LBUTTONDOWN:
        drawing = True
        start_x, start_y = x, y

    # Mouse is moving
    elif event == cv2.EVENT_MOUSEMOVE:
        if drawing:
            img = temp.copy()
            cv2.rectangle(img, (start_x, start_y), (x, y), (255, 0, 0), 2)

    # Left mouse button released
    elif event == cv2.EVENT_LBUTTONUP:
        drawing = False
        cv2.rectangle(img, (start_x, start_y), (x, y), (255, 0, 0), 2)
        temp = img.copy()

# Create window
cv2.namedWindow("Draw Rectangle")
cv2.setMouseCallback("Draw Rectangle", draw_rectangle)

while True:
    cv2.imshow("Draw Rectangle", img)

    key = cv2.waitKey(1) & 0xFF

    # Press 'c' to clear the screen
    if key == ord('c'):
        img = np.ones((500, 700, 3), dtype=np.uint8) * 255
        temp = img.copy()

    # Press ESC to exit
    elif key == 27:
        break

cv2.destroyAllWindows()`