import cv2

# Enter the image path
image_path = "Screenshot 2026-07-14 160634.png"  # Replace with your image file name

# Read the image
img = cv2.imread(image_path)

if img is None:
    print("Error: Image not found!")
    exit()

while True:
    print("\n===== IMAGE EDITOR =====")
    print("1. Show Original Image")
    print("2. Convert to Grayscale")
    print("3. Blur Image")
    print("4. Edge Detection")
    print("5. Rotate Image")
    print("6. Flip Image")
    print("7. Save Current Image")
    print("8. Exit")

    choice = int(input("Enter your choice: "))

    if choice == 1:
        cv2.imshow("Original Image", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    elif choice == 2:
        img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        cv2.imshow("Grayscale", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    elif choice == 3:
        img = cv2.GaussianBlur(img, (9, 9), 0)
        cv2.imshow("Blurred Image", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    elif choice == 4:
        if len(img.shape) == 3:
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        else:
            gray = img

        img = cv2.Canny(gray, 100, 200)
        cv2.imshow("Edges", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    elif choice == 5:
        img = cv2.rotate(img, cv2.ROTATE_90_CLOCKWISE)
        cv2.imshow("Rotated Image", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    elif choice == 6:
        img = cv2.flip(img, 1)
        cv2.imshow("Flipped Image", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    elif choice == 7:
        cv2.imwrite("edited_image.jpg", img)
        print("Image saved as edited_image.jpg")

    elif choice == 8:
        print("Exiting...")
        break

    else:
        print("Invalid Choice!")