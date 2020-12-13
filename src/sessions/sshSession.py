import os
import boto3
from boto3.dynamodb.conditions import Key, Attr
import uuid
from datetime import datetime, timedelta
from sessions.ssh_client import SSH

class Sessions():
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
        self.table = self.dynamodb.Table('Sessions')

    def set(self, user_id, server_id):
        now = datetime.now()
        expired = now + timedelta(days=1)
        session = {
            "id": str(uuid.uuid4()),
            "user_id": user_id,
            "server_id": server_id,
            "is_connected": True,
            "current_dir": "/root/",
            "current_os_user": "root",
            "connected_at": now.strftime('%Y-%m-%d %H:%M:%S'),
            "expired_at": expired.strftime('%Y-%m-%d %H:%M:%S')
        }
        res = self.table.put_item(Item=session)
        return session

    def get_by_user_id(self, user_id):
        now = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        try:
            res = self.table.query(
                IndexName='user_id',
                KeyConditionExpression=Key('user_id').eq(user_id),
                FilterExpression=Attr('expired_at').gte(now),
            )
        except Exception as e:
            print(e)
            return None
        
        sessions = res['Items']
        if len(sessions) > 1:
            self._expire_old_session(sessions)
            latest_session = sorted(sessions, key=lambda x: x['connected_at']).pop(-1)
            return latest_session
        elif len(sessions) == 0:
            return self.set(user_id, 1)
        else:
            return sessions[0]

    def expire(self, session):
        option = {
            'Key' : {'id': session.get('id'), 'user_id': session.get('user_id')},
            'UpdateExpression' : 'set #is_connected = :is_connected',
            'ExpressionAttributeNames' : {"#is_connected": "is_connected"},
            'ExpressionAttributeValues' : {":is_connected": False,}
        }

        self.table.update_item(**option)

    def delete(self):
        pass

    def is_connected(self):
        pass

    def _expire_old_session(self, sessions):
        sorted_sessions = sorted(sessions, key=lambda x: x['connected_at'])
        sorted_sessions.pop(-1)

        for session in sorted_sessions:
            # session['is_connected'] = False
            self.expire(session)

        return sorted_sessions
