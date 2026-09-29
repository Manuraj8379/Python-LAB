# Program: Display an Image using Pillow
# ==========================================

import os
from PIL import Image

# Full path of the image
image_path = r"D:/microsoft logo.png"

# Check whether the image exists
print("Exists:", os.path.exists(image_path))

try:
    # Open the image
    img = Image.open(image_path)

    # Display image details
    print("Image loaded successfully!")
    print("Image Format:", img.format)
    print("Image Size:", img.size)
    print("Image Mode:", img.mode)

    # Show the image
    img.show()

except FileNotFoundError:
    print("Error: Image not found. Check the path.")

except Exception as e:
    print("Error:", e)
