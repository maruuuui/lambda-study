import json
import uuid
import os

from util.db import DataBaseAdapter

ALLOWORIGIN = os.environ.get('ALLOWORIGIN') if os.environ.get('ALLOWORIGIN') else "lambda-study-db"


def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

    context: object, required
        Lambda Context runtime methods and attributes

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    http_method = event["httpMethod"]
    if http_method == "GET":
        return get_handler(event)
    elif http_method == "POST":
        return post_handler(event)
    elif http_method == "DELETE":
        return delete_handler(event)
    elif http_method == "OPTIONS":
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
    else:
        raise ValueError("invalid method")


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
                "deadline": (result["deadline"]).strftime('%Y/%m/%d %H:%M:%S'),
            }
        ]
    print(response)
    return {
        "statusCode": 200, 
        'headers': {
            "Content-Type": 'application/json',
            "Access-Control-Allow-Headers": "Content-Type",
            'Access-Control-Allow-Origin': ALLOWORIGIN,
            'Access-Control-Allow-Methods': 'OPTIONS,GET,POST,DELETE'
        },
        "body": json.dumps(response)
    }


def post_handler(event):

    req_body={}
    try:
        req_body = json.loads(event["body"])
    except:
        return {
            "statusCode": 400, 
            'headers': {
                "Content-Type": 'application/json',
                "Access-Control-Allow-Headers": "Content-Type",
                'Access-Control-Allow-Origin': ALLOWORIGIN,
                'Access-Control-Allow-Methods': 'OPTIONS,GET,POST,DELETE'
            },
            "body": "json decode failed"
        }
    
    # keyの存在確認
    keys = req_body.keys()
    if "title" not in keys or "memo" not in keys or "deadline" not in keys:
        return {
            "statusCode": 400, 
            'headers': {
                "Content-Type": 'application/json',
                "Access-Control-Allow-Headers": "Content-Type",
                'Access-Control-Allow-Origin': ALLOWORIGIN,
                'Access-Control-Allow-Methods': 'OPTIONS,GET,POST,DELETE'
            },
            "body": "invalid request body"
        }
    db = DataBaseAdapter()
    result = db.create({
        "id": str(uuid.uuid4()),
        "title": req_body["title"],
        "memo": req_body["memo"],
        "deadline": req_body["deadline"],
    })

    response = {
        "id": result["id"],
        "title": result["title"], 
        "memo": result["memo"],
        "deadline": (result["deadline"]).strftime('%Y/%m/%d %H:%M:%S'),
    }

    print(response)
    return {
        "statusCode": 200, 
        'headers': {
            "Content-Type": 'application/json',
            "Access-Control-Allow-Headers": "Content-Type",
            'Access-Control-Allow-Origin': ALLOWORIGIN,
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
                'Access-Control-Allow-Origin': ALLOWORIGIN,
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
            'Access-Control-Allow-Origin': ALLOWORIGIN,
            'Access-Control-Allow-Methods': 'OPTIONS,GET,POST,DELETE'
        },
        "body": json.dumps(response)
    }

