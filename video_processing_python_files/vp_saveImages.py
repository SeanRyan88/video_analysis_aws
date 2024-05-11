#Save Image
import os
import cv2
import numpy as np

# def SaveImage(image, filename="first_frame.jpg", directory="/"):
#     print("Run Process SaveImage")
#     if image is not None:
#         # Check if directory exists, create if it doesn't
#         if not os.path.exists(directory):
#             os.makedirs(directory)

#         # Save the image
#         save_path = os.path.join(directory, filename)
#         cv2.imwrite(save_path, image)
#         print(f"Image saved at {save_path}")
#     else:
#         print("No analysis available.")



def SaveImage(image, filename, directory="/"):
    print("Run Process SaveImage")
    # print("Shape of the image:", image.shape)  # Should show (rows, cols, 3) for color images or (rows, cols) for grayscale
    print("Data type of the image:", image.dtype)  # Typically should be uint8
    if isinstance(image, np.ndarray):
        save_path = os.path.join(directory, filename)
        cv2.imwrite(save_path, image)
        print(f"Image saved at {save_path}")
    else:
        print("Provided image is not a valid numpy array.")