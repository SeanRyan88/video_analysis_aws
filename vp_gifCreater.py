# ~/Desktop/Desktop - Sean's Quantum/Uni/2024_S1_FIT5120_PJ/CapstoneProject/GIT/Video Analysis/video_analysis_aws/.conda
from PIL import Image
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
# S3 Writing - return images
def create_gif(inputImagesPath, duration = 500):
    images = []
    for path in inputImagesPath:
        images.append(Image.open(path))
        return images[0]        # Confirm correct syntax to return
        print(f"GIF saved successfully at {output_path}")
    print(f"Image {path} not found.")

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
