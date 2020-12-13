import os
import boto3
from boto3.dynamodb.conditions import Key, Attr

class Servers():
    def __init__(self):
        self.dynamodb_endpoint = os.getenv('DYNAMO_ENDPOINT', 'http://dynamodb:8000')
        self.region = os.getenv('AWS_REGION', 'ap-northeast-1')
        self.aws_access_key_id = os.getenv('AWS_ACCESS_KEY_ID', 'DUMMY')
        self.aws_secret_access_key = os.getenv('AWS_SECRET_ACCESS_KEY', 'DUMMY')
        self.session = boto3.Session(
            aws_access_key_id=self.aws_access_key_id,
            aws_secret_access_key=self.aws_secret_access_key,
            region_name=self.region,
        )
        self.dynamodb = self.session.resource('dynamodb', endpoint_url=self.dynamodb_endpoint)
        self.table = self.dynamodb.Table('Servers')

    def list(self):
        res = self.table.scan()
        print(res)
        return res['Items']

    def get(self, server_id):
        res = self.table.query(
            KeyConditionExpression=Key('id').eq(server_id)
        )
        return res['Items'][0]

    def insert(self):
        pass

    def update(self):
        pass

    def delete(self):
        pass
