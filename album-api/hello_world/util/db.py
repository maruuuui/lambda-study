from datetime import datetime
from dateutil import tz

import os
import boto3
from botocore.exceptions import ClientError

ACCESS_KEY_ID=os.environ.get('ACCESS_KEY_ID') if os.environ.get('ACCESS_KEY_ID') else "localid"
SECRET_ACCESS_KEY=os.environ.get('SECRET_ACCESS_KEY') if os.environ.get('SECRET_ACCESS_KEY') else "localpassword"
DYNAMO_ENDPOINT_URL = os.environ.get('DYNAMO_ENDPOINT_URL') if os.environ.get('DYNAMO_ENDPOINT_URL') else "http://host.docker.internal:8005"
class DataBaseAdapter:
    def __init__(self):
        # データベースへの接続情報
        self.table = boto3.resource(
            'dynamodb', 
            aws_access_key_id=ACCESS_KEY_ID,
            aws_secret_access_key=SECRET_ACCESS_KEY,
            endpoint_url=DYNAMO_ENDPOINT_URL
        ).Table('images')

    def create(self, image):
        JST = tz.gettz('Asia/Tokyo')
        now_str = datetime.now(JST).strftime("%Y/%m/%d %H:%M:%S")
        item = {
                    'id': image["id"],
                    'title': image["title"],
                    'memo': image["memo"],
                    'image_path': image["image_path"],
                    "created_at": now_str,
                }
        try:
            self.table.put_item(
                Item=item
            )
        except ClientError as err:
            raise
        return item

    def update(self, image):
        pass

    def get_all(self):
        print("get_all")
        table = self.table

        images = []
        scan_kwargs = {}
        try:
            done = False
            start_key = None
            while not done:
                if start_key:
                    scan_kwargs['ExclusiveStartKey'] = start_key
                response = table.scan(**scan_kwargs)
                images.extend(response.get('Items', []))
                start_key = response.get('LastEvaluatedKey', None)
                done = start_key is None
        except ClientError as err:
            print(
                "Couldn't scan for images. Here's why: %s: %s",
                err.response['Error']['Code'], err.response['Error']['Message'])
            raise
        return images

    def get(self, id):
        pass

    def delete(self, image_id):
        print("delete", image_id)
        try:
            self.table.delete_item(Key={'id': image_id})
        except ClientError as err:
            raise
        return "deleted"
