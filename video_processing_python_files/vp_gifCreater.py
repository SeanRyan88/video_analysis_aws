# ~/Desktop/Desktop - Sean's Quantum/Uni/2024_S1_FIT5120_PJ/CapstoneProject/GIT/Video Analysis/video_analysis_aws/.conda
from PIL import Image
import cv2
import os


######################################################
# Local Writing
# def create_gif(image_paths, output_path, duration = 500):
#     images = []
#     for path in image_paths:
#         # Ensure the image exists
#         if os.path.exists(path):
#             # Open the image and append to the list
#             images.append(Image.open(path))
#         else:
#             print(f"Image {path} not found.")
#             return

#     # Save the images as a GIF
#     images[0].save(output_path, save_all=True, append_images=images[1:], optimize=False, duration=duration, loop=0)
#     print(f"GIF saved successfully at {output_path}")


######################################################
# # Create gif based on image paths
# def create_gif(inputImagesPath, duration = 500):
#     print("Run Process create_gif")
#     images = []
#     for path in inputImagesPath:
#         images.append(Image.open(path))
#         return images[0]        # Confirm correct syntax to return
#         print(f"GIF saved successfully at {output_path}")
#     print(f"Image {path} not found.")

######################################################
# Create gif based on images parsed
def create_gif(images, output_path, duration=500):
    print("Run Process create_gif")
    pil_images = []
    
    # Convert each OpenCV BGR image to a PIL Image
    for image in images:
        try:
            # Convert from OpenCV BGR to RGB format
            image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            pil_image = Image.fromarray(image_rgb)
            pil_images.append(pil_image)
        except Exception as e:
            print(f"Failed to convert an image: {e}")
            return None  # Early return on failure
    
    # Save the images as a GIF
    try:
        if pil_images:
            pil_images[0].save(output_path, save_all=True, append_images=pil_images[1:], optimize=False, duration=duration, loop=0)
            print(f"GIF saved successfully at {output_path}")
        else:
            print("No images were processed. GIF not created.")
    except Exception as e:
        print(f"Failed to save GIF: {e}")
        return None
    
    return output_path

# Example usage:
# Assuming `images` is a list of three OpenCV images
# images = [cv2.imread('frame1.jpg'), cv2.imread('frame2.jpg'), cv2.imread('frame3.jpg')]
# output_path = 'path/to/output.gif'
# result = create_gif(images, output_path)
# if result:
#     print(f"GIF was created successfully at {result}")
# else:
#     print("An error occurred while creating the GIF.")



######################################################
# #Testing
# # List of image paths
# path = "/Users/seanryan/Desktop/Desktop - Sean's Quantum/Uni/2024_S1_FIT5120_PJ/Local ActiveAging/VideoAnalysis/Example_output/"
# image1_path = path+'1 max_frame.jpg'
# image2_path = path+'1 min_frame.jpg'
# image3_path = path+'2 max_frame.jpg'

# image_paths = [image1_path, image2_path, image3_path]

# # Output path for the GIF
# output_gif_path = path+'output.gif'

# # Duration of each frame in the GIF (in milliseconds)
# frame_duration = 500

# create_gif(image_paths, output_gif_path, frame_duration)
