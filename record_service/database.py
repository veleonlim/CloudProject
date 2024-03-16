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
table_name = 'record'

# Get a reference to the DynamoDB table
table = dynamodb.Table(table_name)

# function call when user Join an event
def create_record(record_id, event_id, email):
    response = table.put_item(
        Item={
            'record_id': record_id,
            'event_id': event_id,
            'email': email,
        }
    )
    return response

# Single delete AKA user "unjoin" an event
def delete_record(record_id):
    response = table.delete_item(
        Key={
            'record_id': record_id
        }
    )
    return response

# multiple delete AKA admin removed the event
def delete_records_of_event(event_id):
    try:
        # Scan Whole Table
        response = table.scan(
            FilterExpression=Attr('event_id').eq(event_id)
        )
        
        for item in response.get('Items', []):
            record_id = item.get('record_id')
            table.delete_item(
                Key={'record_id': record_id}
            )
        
        return True  # Return True to indicate successful deletion
    
    except botocore.exceptions.ClientError as e:
        # Handle the error, log it, or return False to indicate failure
        print(f"Error: {e}")
        return False

#Retrieve count of per event records
def get_event_joined_count_by_id(event_id):
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