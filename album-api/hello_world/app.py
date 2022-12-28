import json
import boto3
import base64
import io
from datetime import datetime
import base64
import six
import uuid
import imghdr
import os


BUCKET_NAME='album-api-image-storage'
DIRECTORY='uploaded_files/'
ALLOWORIGIN="http://album-app.maruuuui.tk"
ACCESS_KEY_ID=os.environ.get('ACCESS_KEY_ID') if os.environ.get('ACCESS_KEY_ID') else "lambda-study-db"
SECRET_ACCESS_KEY=os.environ.get('SECRET_ACCESS_KEY') if os.environ.get('SECRET_ACCESS_KEY') else "lambda-study-db"

def lambda_handler(event, context):
    http_method = event["httpMethod"]
    if http_method == "OPTIONS":
        print("OPTION request")
        return {
        "statusCode": 200, 
        'headers': {
            "Content-Type": 'application/json',
            "Access-Control-Allow-Headers": "Content-Type",
            'Access-Control-Allow-Origin': ALLOWORIGIN,
            'Access-Control-Allow-Methods': 'OPTIONS,GET,POST,DELETE'
        },
        "body": json.dumps({})
    }
    if http_method != "POST":
        raise ValueError("invalid method")
    
    print("POST request")
    req_body = json.loads(event["body"])

    # base64_file = base64.b64decode(req_body['image'])
    # file, file_name = decode_base64_file(base64_file)
    file, file_name = decode_base64_file(req_body['image'])
    client = boto3.client('s3', aws_access_key_id=ACCESS_KEY_ID,
                          aws_secret_access_key=SECRET_ACCESS_KEY)

    client.upload_fileobj(
        file,
        BUCKET_NAME,
        file_name,
        ExtraArgs={'ACL': 'public-read'}
    )
    return {
        'statusCode': 200,
        'body': json.dumps('アップロード完了')
    }


def get_file_extension(file_name, decoded_file):
    extension = imghdr.what(file_name, decoded_file)
    extension = "jpg" if extension == "jpeg" else extension
    return extension


def decode_base64_file(data):
    """
    Fuction to convert base 64 to readable IO bytes and auto-generate file name with extension
    :param data: base64 file input
    :return: tuple containing IO bytes file and filename
    """
    # Check if this is a base64 string
    if isinstance(data, six.string_types):
        # Check if the base64 string is in the "data:" format
        if 'data:' in data and ';base64,' in data:
            # Break out the header from the base64 content
            header, data = data.split(';base64,')

        # Try to decode the file. Return validation error if it fails.
        try:
            decoded_file = base64.b64decode(data)
        except TypeError:
            TypeError('invalid_image')

        # Generate file name:
        file_name = str(uuid.uuid4())[:12]  # 12 characters are more than enough.
        # Get the file name extension:
        file_extension = get_file_extension(file_name, decoded_file)

        complete_file_name = "%s.%s" % (file_name, file_extension,)

        return io.BytesIO(decoded_file), complete_file_name
    else:
        print("not base64",data)