import json
import boto3
import os

from util.image import decode_base64_file

BUCKET_NAME='album-api-image-storage'
DIRECTORY='uploaded_files/'

ALLOW_ORIGIN=os.environ.get('ALLOWORIGIN') if os.environ.get('ALLOWORIGIN') else "http://localhost:3000"
ACCESS_KEY_ID=os.environ.get('ACCESS_KEY_ID') if os.environ.get('ACCESS_KEY_ID') else "localid"
SECRET_ACCESS_KEY=os.environ.get('SECRET_ACCESS_KEY') if os.environ.get('SECRET_ACCESS_KEY') else "localpassword"
ENDPOINT_URL=os.environ.get('ENDPOINT_URL') if os.environ.get('ENDPOINT_URL') else "http://host.docker.internal:9000"

def lambda_handler(event, context):
    http_method = event["httpMethod"]
    if http_method == "OPTIONS":
        print("OPTION request")
        return {
        "statusCode": 200, 
        'headers': {
            "Content-Type": 'application/json',
            "Access-Control-Allow-Headers": "Content-Type",
            'Access-Control-Allow-Origin': ALLOW_ORIGIN,
            'Access-Control-Allow-Methods': 'OPTIONS,GET,POST,DELETE'
        },
        "body": json.dumps({})
    }
    elif http_method == "GET":
        return get_handler(event)
    elif http_method == "POST":
        return post_handler(event)
    else:
        raise ValueError("invalid method")

def post_handler(event):
    print("POST request")
    req_body = json.loads(event["body"])

    file, file_name = decode_base64_file(req_body['image'], req_body['file_name'])
    client = boto3.client(
        's3', 
        aws_access_key_id=ACCESS_KEY_ID,
        aws_secret_access_key=SECRET_ACCESS_KEY,
        endpoint_url=ENDPOINT_URL
    )

    client.upload_fileobj(
        file,
        BUCKET_NAME,
        file_name,
        ExtraArgs={'ACL': 'public-read', "ContentType": req_body["type"]}
    )
    image_path = ENDPOINT_URL.replace("host.docker.internal", "localhost") + "/" + BUCKET_NAME + "/" + file_name

    print("image_path", image_path)
    return {
        'statusCode': 200,
        'headers': {
            "Content-Type": 'application/json',
            "Access-Control-Allow-Headers": "Content-Type",
            'Access-Control-Allow-Origin': ALLOW_ORIGIN,
            'Access-Control-Allow-Methods': 'OPTIONS,GET,POST,DELETE'
        },
        'body': json.dumps('アップロード完了')
    }

def get_handler(event):
    return {
        'statusCode': 200,
        'headers': {
            "Content-Type": 'application/json',
            "Access-Control-Allow-Headers": "Content-Type",
            'Access-Control-Allow-Origin': ALLOW_ORIGIN,
            'Access-Control-Allow-Methods': 'OPTIONS,GET,POST,DELETE'
        },
        'body': json.dumps([])
    }
