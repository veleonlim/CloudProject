import uuid
import boto3
import botocore
import key_config as keys
from boto3.dynamodb.conditions import Attr
from datetime import datetime

dynamodb =boto3.resource('dynamodb',
                         aws_access_key_id=keys.AWS_ACCESS_KEY_ID,
                         aws_secret_access_key=keys.AWS_SECRET_ACCESS_KEY,
                         region_name=keys.REGION_NAME)

dynamodb_client = boto3.client('dynamodb',
                              aws_access_key_id=keys.AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=keys.AWS_SECRET_ACCESS_KEY,
                              region_name=keys.REGION_NAME)

# Name of your DynamoDB table
table_name = 'events'

# Get a reference to the DynamoDB table
table = dynamodb.Table(table_name)

# # Define a function to retrieve all events that have not been approved
def get_unapproved_events():
     try:
         response = table.scan(
             FilterExpression=Attr('approval_status').eq('pending')
         )
         items = response.get('Items', [])
         return items
     except botocore.exceptions.ClientError as e:
         # Handle the error, log it, or return an empty list
         print(f"Error: {e}")
         return []

# Define a function to approve an event
def approve_event(event_id):
    try:
        response = table.update_item(
            Key={'event_id': event_id},
            UpdateExpression='SET approval_status = :status',
            ExpressionAttributeValues={
                ':status': 'approved'
            },
            ReturnValues='UPDATED_NEW'
        )
        return response
    except Exception as e:
        print(e)

# define a function to reject an event
def reject_event(event_id):
    try:
        response = table.update_item(
            Key={'event_id': event_id},
            UpdateExpression='SET approval_status = :status',
            ExpressionAttributeValues={
                ':status': 'rejected'
            },
            ReturnValues='UPDATED_NEW'
        )
        return response
    except Exception as e:
        print(e)