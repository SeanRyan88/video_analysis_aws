#Standard Python Lib
import json
import os
import boto3

# Installed via requirements.txt
from botocore.exceptions import ClientError
import numpy as np


import time
from typing import List, Tuple
from urllib.parse import unquote_plus
from dotenv import load_dotenv

import cv2
import mediapipe as mp

# Local modules to be include
import video_processing_python_files.vp_gifCreater
# import video_processing_python_files.vp_calculateAngle
import video_processing_python_files.vp_analysePose 
import video_processing_python_files.vp_runAnalysis
import video_processing_python_files.vp_saveImages


def process_messages(messages: List[dict], sqs_client: boto3.client):
    print("Run Process Process_messages")
    """
    Processes messages retrieved from an SQS queue, extracting S3 bucket and key details,
    downloading and processing the corresponding video files, and then deleting the messages
    from the queue to prevent reprocessing.

    Args:
    messages (List[dict]): A list of message dictionaries received from SQS.
    sqs_client (boto3.client): A Boto3 SQS client used to delete messages after processing.

    Returns:
    None
    """
    for message in messages:
        print(message)
        receipt_handle = message['ReceiptHandle']
        body = json.loads(message['Body'])
        s3_key = body['Records'][0]['s3']['object']['key']
        s3_bucket = body['Records'][0]['s3']['bucket']['name']
        # Handles the formating of the sqs message
        object_key = unquote_plus(s3_key)

        process_video_file(s3_bucket, object_key)
        
        # sqs_client.delete_message(
        #     QueueUrl=sqs_queue_url,
        #     ReceiptHandle=receipt_handle
        # )

def process_video_file(s3_bucket: str, s3_key: str):
    print("Run Process process_video_files")
    """
    Retrieves a video file from an S3 bucket, processes the video, uploads the results
    (a text file and potentially two GIFs) to another S3 bucket, and then cleans up by deleting
    the local video and GIF files to free up disk space.

    Args:
        s3_bucket (str): The name of the S3 bucket where the video file is stored.
        s3_key (str): The key of the video file in the S3 bucket.

    Returns:
        None
    """
    local_filename = '/tmp/' + s3_key.split('/')[-1]
    gif1 = gif2 = None  # Initialize to ensure scope beyond the try block

    print(f"Processing {s3_key}.......")
    print("File name = ", local_filename)
    print("S3 Bucket name = ", s3_bucket)
    print("S3 Key  = ", s3_key)

    try:
        s3 = boto3.client('s3', region_name='us-east-1')
        s3.download_file(s3_bucket, s3_key, local_filename)
        print(f"Downloaded {s3_key} to {local_filename}")
        
    except Exception as e:
        print(f"Error downloading video: {e}")
        return

    try:
        # Placeholder for actual video processing module
        # TEMP TURN OFF
        # results_text, images = vp_runAnalysis.process_video(local_filename)

        print("Local File Name = ", local_filename)

        # TEMP TESTING
        AnalysisArray = video_processing_python_files.vp_analysePose.AnalysePose(local_filename)

        print("Analysis Returned: ", local_filename)
        # Save 3 images
        video_processing_python_files.vp_analysePose.SaveImage(AnalysisArray[0], filename="image_1.jpg")
        video_processing_python_files.vp_analysePose.SaveImage(AnalysisArray[1], filename="image_2.jpg")
        video_processing_python_files.vp_analysePose.SaveImage(AnalysisArray[2], filename="image_3.jpg")

        # Combine Images
        # images = [AnalysisArray[0], AnalysisArray[1], AnalysisArray[2]]
        images = ["image_1.jpg", "image_2.jpg", "image_3.jpg"]

        # Error processing/uploading results for Test Video4.mp4: name 'mp' is not defined
        # Error polling SQS: name 'results_text' is not defined


        # Converts Images into gif
        # create_gif(image_paths, output_path, duration = 500)
        results_gif = video_processing_python_files.vp_gifCreater.create_gif(images, "Output_Test.gif")
        
        #results_text, gif1, gif2 = 'dummy results text', '/tmp/dummy1.gif', '/tmp/dummy2.gif'
        print(f"Processed {s3_key} successfully, results ready to upload.")

        # To reference text file based on results:
        results_text = "You're doing Great!"

        # Upload results back to another S3 bucket
        print("Upload Results")
        upload_results(S3_BUCKET_NAME, s3_key, results_gif, results_text)
    except Exception as e:
        print(f"Error processing/uploading results for {s3_key}: {e}")
    finally:

        # Clean up: Delete the local video file and any generated GIFs
        cleanup_files([local_filename]) #, results_gif])

def cleanup_files(files):
    print("Run Process cleanup_files")
    """ Removes specified files from the filesystem if they exist. """
    for file_path in files:
        if file_path and os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"Deleted {file_path}")
            except Exception as e:
                print(f"Failed to delete {file_path}: {e}")       

def upload_results(bucket_name: str, base_key: str, results_text: str, gif1: str):
    print("Run Process upload_results")
    """
    Uploads processing results including a text file and two GIFs to an S3 bucket.

    Args:
    bucket_name (str): The name of the S3 bucket where the results will be uploaded.
    base_key (str): The base S3 key of the original video file; used to determine result file names.
    results_text (str): The contents of the result text file.
    gif1 (str): The file path of the first GIF result.
    gif2 (str): The file path of the second GIF result.

    Returns:
    None
    """
    
    print(f"Uploading {base_key}.......")

    s3 = boto3.client('s3', region_name='us-east-1')
    result_prefix = base_key.replace('.mp4', '')
    folder_name = result_prefix + '/'
    object_name = f"{folder_name}{result_prefix}"
  
    try:
        # Write text results
        s3.put_object(Bucket=bucket_name, Key=object_name + '_results.txt', Body=results_text)
        # Write gif results
        s3.upload_file(gif1, bucket_name, result_prefix + '_1.gif')
        #3.upload_file(gif2, bucket_name, result_prefix + '_2.gif')
    except Exception as e:
            print(f"Error uploading video: {e}")
    print(f"Uploaded {object_name + '_results.txt'} sucessfully.......")


load_dotenv()

# Access environment variables
S3_BUCKET_NAME = os.getenv('AWS_S3_BUCKET_NAME')
SQS_QUEUE_URL = os.getenv('AWS_SQS_QUEUE_URL')



if __name__ == '__main__':
    print("Run main")
    # The URL of the SQS queue from which messages are received
    # Create SQS client
    sqs = boto3.client('sqs', region_name='us-east-1')

    # Specify your queue URL
    sqs_queue_url = SQS_QUEUE_URL

    # Continuously poll the queue for new messages
    while True:
        try:
            # Long polling for messages from the SQS queue to reduce the number of empty responses and lower costs
            print("Polling SQS.......")
            response = sqs.receive_message(
                QueueUrl=sqs_queue_url,
                MaxNumberOfMessages=10,  # Retrieve up to 10 messages in one request
                WaitTimeSeconds=20       # Wait up to 20 seconds for a message if the queue is initially empty
            )

            # Check if there are any new messages
            messages = response.get('Messages', [])
            if messages:
                # Process each message using the process_messages function
                process_messages(messages, sqs)
        except Exception as e:
            print(f"Error polling SQS: {e}")
            time.sleep(10)  # Wait a bit before retrying to avoid flooding logs with error messages