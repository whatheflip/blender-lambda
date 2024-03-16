import boto3
import json
import logging
import os
import sys

# from https://gist.github.com/niranjv/fb95e716151642e8ca553b0e38dd152e
logger = logging.getLogger()
for h in logger.handlers:
    logger.removeHandler(h)
h = logging.StreamHandler(sys.stdout)
FORMAT = '[%(levelname)s] %(message)s'
h.setFormatter(logging.Formatter(FORMAT))
logger.addHandler(h)
logger.setLevel(logging.INFO)

S3_BUCKET_NAME = os.environ['S3_BUCKET_NAME']
LOCAL_RENDER_FILE = '/tmp/render_file.blend'


def handler(event, context):
    try:
        received_body = event['Records'][0]['body']
        record = json.loads(received_body)

        file_name = record['file_name']
        frame = record['frame']
        support_files = record['support_files']

        logger.info(f'Received message for file: {file_name} and frame: {frame}')

        retrieve_files_from_s3(file_name, support_files)

        frame_str = str(frame).zfill(4)
        output_file = f'/tmp/rendered_{frame_str}.png'
        render_frame(frame, output_file)

        upload_file_to_s3(output_file)

        logger.info('Done.')
    except Exception as e:
        logger.exception(e)
        raise e


def render_frame(frame, output_file):
    logger.info(f'Rendering frame: {frame}')

    # os.system(f"blender -b -P render_frame.py -- {LOCAL_RENDER_FILE} {output_file} {frame}")

    os.system(f"blender --factory-startup -b file.blend -P render_frame.py -E CYCLES -o output -s {frame} -e {frame} -a -- INPUT_FRAMES=Input_frames INPUT_COVER=Input_cover COVER_FILENAME=Cover_combined_alpha_clear_reduced.png OUTPUT_PRE_RENDER=Output_pre_render OUTPUT_FINAL_VIDEO=Output_final_video TEXT_FRONT=000000001111111122222222 TEXT_SIDE=ABCD EFGH IJKL MNOP TEXT_BACK=WHATEFLIP BASE_FRAMES=Page_numbers_reduced COLOR_COVER=FF0009 COLOR_TEXT=FF72BD COLOR_BACKGROUND=FFDD5C OUTPUT_PRE_RENDER_TRASH=Output_pre_render_trash")

    logger.info(f'Rendering frame: {frame} done')


def retrieve_files_from_s3(file_name, support_files):
    logger.info(f'Retrieving file: {file_name} from S3 bucket: {S3_BUCKET_NAME}')

    s3 = boto3.resource('s3')
    bucket = s3.Bucket(S3_BUCKET_NAME)
    bucket.download_file(file_name, LOCAL_RENDER_FILE)

    logger.info(f'Retrieving file: {file_name} from S3 bucket: {S3_BUCKET_NAME} done')

      # Function to download files from a specific S3 folder to a local directory
    def download_directory_from_s3(s3_folder, local_path):
        if not os.path.exists(local_path):
            os.makedirs(local_path)
        for obj in bucket.objects.filter(Prefix=s3_folder):
            if obj.key[-1] != '/':  # Avoid trying to download "directory" keys
                local_file_path = os.path.join(local_path, os.path.basename(obj.key))
                bucket.download_file(obj.key, local_file_path)
                logger.info(f"Downloaded {obj.key} to {local_file_path}")

    # Retrieve the main file
    bucket.download_file(file_name, LOCAL_RENDER_FILE)
    logger.info(f'Retrieving file: {file_name} from S3 bucket: {S3_BUCKET_NAME} done')

    # Download support files
    support_file_paths = {
        "Input_frames": "Input_frames/",
        "Input_cover": "Input_cover/",
        "Output_pre_render": "Output_pre_render/",
        "Output_pre_render_trash": "Output_pre_render_trash/"
    }
    
    for local_dir, s3_path in support_file_paths.items():
        s3_full_path = f'{s3_path}'  # Assuming the s3_path includes the bucket name part
        download_directory_from_s3(s3_full_path, local_dir)
        logger.info(f"Completed downloading {s3_full_path}")

    # for file in support_files:
    #     logger.info(f'Retrieving file: {file} from S3 bucket: {S3_BUCKET_NAME}')

    #     bucket.download_file(file, f'/tmp/{file}')

    #     logger.info(f'Retrieving file: {file} from S3 bucket: {S3_BUCKET_NAME} done')


def upload_file_to_s3(file_name):
    logger.info(f'Uploading file: {file_name} to S3 bucket: {S3_BUCKET_NAME}')

    s3 = boto3.resource('s3')
    bucket = s3.Bucket(S3_BUCKET_NAME)
    bucket.upload_file(file_name, os.path.basename(file_name))

    logger.info(f'Uploading file: {file_name} to S3 bucket: {S3_BUCKET_NAME} done')
