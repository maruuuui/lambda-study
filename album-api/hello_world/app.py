import json
import boto3
import os
import uuid

from util.image import decode_base64_file
from util.db import DataBaseAdapter

BUCKET_NAME='album-api-image-storage'
DIRECTORY='uploaded_files/'

ALLOW_ORIGIN=os.environ.get('ALLOW_ORIGIN') if os.environ.get('ALLOW_ORIGIN') else "http://localhost:3000"
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
    elif http_method == "DELETE":
        return delete_handler(event)
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

    db = DataBaseAdapter()
    result = db.create({
        "id": str(uuid.uuid4()),
        "title": req_body["title"],
        "memo": req_body["memo"],
        "image_path": image_path,
    })

    response = {
        "id": result["id"],
        "title": result["title"], 
        "memo": result["memo"],
        "image_path": result["image_path"],
        "created_at": result["created_at"],
    }

    print(response)

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
    db = DataBaseAdapter()

    results = db.get_all()
    response = []
    for result in results:
        response += [
            {
                "id": result["id"],
                "title": result["title"], 
                "memo": result["memo"],
                "image_path": result["image_path"],
                "created_at": result["created_at"],
            }
        ]
    print(response)
    return {
        "statusCode": 200, 
        'headers': {
            "Content-Type": 'application/json',
            "Access-Control-Allow-Headers": "Content-Type",
            'Access-Control-Allow-Origin': ALLOW_ORIGIN,
            'Access-Control-Allow-Methods': 'OPTIONS,GET,POST,DELETE'
        },
        "body": json.dumps(response)
    }

def delete_handler(event):
    try:
        todo_id = event["pathParameters"]["id"]
    except:
        return {
            "statusCode": 400, 
            'headers': {
                "Content-Type": 'application/json',
                "Access-Control-Allow-Headers": "Content-Type",
                'Access-Control-Allow-Origin': ALLOW_ORIGIN,
                'Access-Control-Allow-Methods': 'OPTIONS,GET,POST,DELETE'
            },
            "body": "json decode failed"
        }

    db = DataBaseAdapter()
    result = db.delete(todo_id)

    response = result

    print(response)

    return {
        "statusCode": 200, 
        'headers': {
            "Content-Type": 'application/json',
            "Access-Control-Allow-Headers": "Content-Type",
            'Access-Control-Allow-Origin': ALLOW_ORIGIN,
            'Access-Control-Allow-Methods': 'OPTIONS,GET,POST,DELETE'
        },
        "body": json.dumps(response)
    }
