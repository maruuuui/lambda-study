import json

from util.db import DataBaseAdapter


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
    db = DataBaseAdapter()

    results = db.get_all()
    response = []
    for result in results:
        response += [
            {
                "title": result["title"], 
                "memo": result["memo"],
                "deadline": (result["deadline"]).strftime('%Y/%m/%d %H:%M:%S'),
            }
        ]
    print(response)
    return {
        "statusCode": 200, 
        'headers': {
            "Access-Control-Allow-Headers": "Content-Type,X-CSRF-TOKEN",
            'Access-Control-Allow-Origin': '*',
            'Access-Control-Allow-Methods': 'OPTIONS,GET,POST,DELETE'
        },
        "body": json.dumps(response)
    }
