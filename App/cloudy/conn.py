import base64
import json

import boto3

from botocore.exceptions import ClientError


def get_secret():

    secret_name = "arn:aws:secretsmanager:us-east-1:851217607308:secret:CloudyDB-PnSugq"
    region_name = "us-east-1"

    session = boto3.session.Session()
    sts_connection = session.client('sts')
    assume_role_object = sts_connection.assume_role(
        RoleArn='arn:aws:iam::851217607308:role/SecretsManagerCloudy',
        RoleSessionName="AssumeRoleSession1"
    )

    new_session = boto3.session.Session(
        aws_access_key_id=assume_role_object['Credentials']['AccessKeyId'],
        aws_secret_access_key=assume_role_object['Credentials']['SecretAccessKey'],
        aws_session_token=assume_role_object['Credentials']['SessionToken']
    )

    client = new_session.client(
        service_name='secretsmanager',
        region_name=region_name
    )

    try:
        get_secret_value_response = client.get_secret_value(
            SecretId=secret_name
        )
    except ClientError:
        return None
    else:
        if 'SecretString' in get_secret_value_response:
            secret = get_secret_value_response['SecretString']
        else:
            secret = base64.b64decode(get_secret_value_response['SecretBinary'])
        return json.loads(secret)
