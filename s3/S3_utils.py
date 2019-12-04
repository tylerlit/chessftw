import boto3
from botocore.exceptions import ClientError

__AWS_ACCESS_KEY_ID__ = "AKIAZ7BZF6DKULO2LWCV"
__AWS_SECRET_ACCESS_KEY__ = "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"

def upload_file(file_name, bucket, object_name=None):
    """Upload a file to an S3 bucket

    :param file_name: File to upload. include full path!
    :param bucket: Bucket to upload to
    :param object_name: S3 object name. This is what we will call it after uploading.
    If not specified then file_name is used
    :return: True if file was uploaded, else False
    """

    # If S3 object_name was not specified, use file_name
    if object_name is None:
        object_name = file_name

    # Upload the file
    s3_client = boto3.client('s3', 
                                aws_access_key_id = __AWS_ACCESS_KEY_ID__,
                                aws_secret_access_key= __AWS_SECRET_ACCESS_KEY__)
    try:
        s3_client.upload_file(file_name, bucket, object_name)

    except ClientError as e:
        print(e.response)
        return False
    return True

def download_file(bucket_name, object_name, file_name):
    """Trys to download a file from s3 bucket

    :param bucket_name: Bucket to download from
    :param object_name: S3 object name
    :param file_name: what the file will be named locally after downloading
    """

    #start up client
    s3_client = boto3.client('s3', 
                                aws_access_key_id = __AWS_ACCESS_KEY_ID__,
                                aws_secret_access_key= __AWS_SECRET_ACCESS_KEY__)

    #do the download
    s3_client.download_file(bucket_name, object_name, file_name)