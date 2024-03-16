import boto3
import botocore
import key_config as keys
from boto3.dynamodb.conditions import Attr, Key


dynamodb =boto3.resource('dynamodb',
                         aws_access_key_id=keys.AWS_ACCESS_KEY_ID,
                         aws_secret_access_key=keys.AWS_SECRET_ACCESS_KEY,
                         region_name=keys.REGION_NAME)
dynamodb_client = boto3.client('dynamodb',
                              aws_access_key_id=keys.AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=keys.AWS_SECRET_ACCESS_KEY,
                              region_name=keys.REGION_NAME)

# Name of your DynamoDB table
table_name = 'comments'

# Get a reference to the DynamoDB table
table = dynamodb.Table(table_name)
# Define a function to add comment
def create_comment(comment_id,event_id, email, comment, comment_submitted_time):
    response = table.put_item(
        Item={
            'comment_id': comment_id,
            'event_id': event_id,
            'email': email,
            'comment': comment,
            'comment_submitted_time': comment_submitted_time
        }
    )
    return response

def get_comments_by_event_id(event_id):
    try:
        response = table.scan(
            FilterExpression=Attr('event_id').eq(event_id)
        )
        items = response.get('Items', [])
        return items
    except botocore.exceptions.ClientError as e:
        # Handle the error, log it, or return an empty list
        print(f"Error: {e}")
        return []



