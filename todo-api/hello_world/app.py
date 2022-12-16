import json

import requests

import mysql.connector

def lambda_handler(event, context):
    """Sample pure Lambda function

    Parameters
    ----------
    event: dict, required
        API Gateway Lambda Proxy Input Format

        Event doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html#api-gateway-simple-proxy-for-lambda-input-format

    context: object, required
        Lambda Context runtime methods and attributes

        Context doc: https://docs.aws.amazon.com/lambda/latest/dg/python-context-object.html

    Returns
    ------
    API Gateway Lambda Proxy Output Format: dict

        Return doc: https://docs.aws.amazon.com/apigateway/latest/developerguide/set-up-lambda-proxy-integrations.html
    """

    results = connect_db()
    response = []
    for result in results:
        response +=[
            {
                "name":result["name"],
                "age":result["age"]
            }
        ]

    return {
        "statusCode":200,
        "body":json.dumps({"results":response})
    }

def connect_db():    
    # データベースへの接続とカーソルの生成
    sql = "select * from sample;"
    conn = mysql.connector.connect(
        host = "lambda-study-db",
        port ="3306",
        user = "root",
        password = "rootpass",
        database = "sample_db"
    )
    print("connected!")
    cur = conn.cursor(dictionary=True)

    cur.execute(sql)
    results = cur.fetchall()
    # 接続を閉じる
    cur.close()
    conn.close()
    return results