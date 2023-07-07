import boto3
import boto3.session
import base64
import requests
from datetime import datetime

def create_object_key(file_extension):
    time_stamp = int(datetime.now().timestamp())
    return f"profile-images/avatar_{time_stamp}.{file_extension}"

def create_boto3_session(aws_access_key_id, aws_secret_access_key, region_name):
    my_session = boto3.session.Session(
        aws_access_key_id=aws_access_key_id,
        aws_secret_access_key=aws_secret_access_key,
        region_name=region_name
    )
    return my_session

def upload_s3_from_base64_string(session, bucket_name, base64_string, object_key):
    try:
        s3_r = session.resource('s3')
        obj = s3_r.Object(bucket_name, object_key)
        obj.put(Body=base64.b64decode(base64_string))
        return object_key
    except Exception as err:
        print(str(err))
        return None

def upload_s3_from_url(session, bucket_name, source_url, object_key):
    try:
        s3_r = session.resource('s3')
        obj = s3_r.Object(bucket_name, object_key)
        obj.put(Body=requests.get(source_url).content)
        return object_key
    except Exception as err:
        print(str(err))
        return None
        
