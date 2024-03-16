import boto3
import botocore
import key_config as keys
from botocore.exceptions import ClientError

dynamodb = boto3.resource('dynamodb',
                          aws_access_key_id=keys.AWS_ACCESS_KEY_ID,
                          aws_secret_access_key=keys.AWS_SECRET_ACCESS_KEY,
                          region_name=keys.REGION_NAME)
dynamodb_client = boto3.client('dynamodb',
                              aws_access_key_id=keys.AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=keys.AWS_SECRET_ACCESS_KEY,
                              region_name=keys.REGION_NAME)

DYNAMODB_TABLE_NAME = 'Users'
table = dynamodb.Table(DYNAMODB_TABLE_NAME)

def check_user_credentials(email, password):
    try:
        response = table.get_item(
            Key={'email': email}
        )
        user_item = response.get('Item')

        if user_item:
            # Check if the provided password matches the stored password
            if user_item['password'] == password:
                return True

    except ClientError as e:
        # Handle any potential errors here
        print("Error:", e)

    return False

def get_user_role(email):
    try:
        response = table.get_item(
            Key={'email': email}
        )
        user_item = response.get('Item')

        if user_item and 'role' in user_item:
            return user_item['role']

    except ClientError as e:
        # Handle any potential errors here
        print("Error:", e)

    return None
