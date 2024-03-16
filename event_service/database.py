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

# Initialize the S3 client
s3 = boto3.client('s3',
                              aws_access_key_id=keys.AWS_ACCESS_KEY_ID,
                              aws_secret_access_key=keys.AWS_SECRET_ACCESS_KEY,
                              region_name=keys.REGION_NAME)

# Your S3 bucket name
S3_BUCKET_NAME = 'mykampungevents'



# Name of your DynamoDB table
table_name = 'events'

# Get a reference to the DynamoDB table
table = dynamodb.Table(table_name)

def create_event(event_name, event_start_date, event_end_date, event_description, approval_status, email, capacity, image_data=None):
    event_id = str(uuid.uuid4())
    events_submitted_time = datetime.now().isoformat()
    
    # Prepare the item to be stored in DynamoDB
    item = {
        'event_id': event_id,
        'event_name': event_name,
        'event_start_date': event_start_date,
        'event_end_date': event_end_date,
        'events_submitted_time': events_submitted_time,
        'event_description': event_description,
        'approval_status': approval_status,
        'email': email,
        'capacity': capacity,
    }

    if image_data:
        try:
            # Generate a unique filename for the image
            image_filename = f"{str(uuid.uuid4())}.jpg"

            # Upload the image data to the S3 bucket
            s3.upload_fileobj(image_data, 'mykampungevents', image_filename)

            # Generate the image URL and add it to the item
            image_url = f"https://mykampungevents.s3.amazonaws.com/{image_filename}"
            item['image_url'] = image_url
        except Exception as e:
            print("Error uploading image to S3:", str(e))
            # Handle the error, log it, or return an error response

    # Store the item in DynamoDB
    response = table.put_item(Item=item)

    return response



def get_all_events():
    try:
        response = table.scan(  FilterExpression=Attr('approval_status').eq('approved'))
        items = response.get('Items', [])
        return items
    except botocore.exceptions.ClientError as e:
        # Handle the error, log it, or return an empty list
        print(f"Error: {e}")
        return []
    
# Define a function to retrieve an event by event_id
def get_event(event_id):
    response = dynamodb_client.get_item(
        TableName=table_name,
        Key={'event_id': {'S': event_id}}
    )
    item = response.get('Item')
    return item

def update_event(event_id, event_name, event_start_date, event_end_date, event_description, approval_status, capacity):
    try:
        response = table.update_item(
            Key={'event_id': event_id},
            UpdateExpression='SET event_name = :name, event_start_date = :start_date, event_end_date = :end_date, event_description = :description, approval_status = :approval, #cap = :capacity',
            ExpressionAttributeValues={
                ':name': event_name,
                ':start_date': event_start_date,
                ':end_date': event_end_date,
                ':description': event_description,
                ':approval': approval_status,
                ':capacity': capacity
            },
            ExpressionAttributeNames={
                '#cap': 'capacity'
            },
            ReturnValues='UPDATED_NEW'
        )
        return response
    except Exception as e:
        print(f"Error updating event: {e}")
        return None

# Define a function to delete an event
def delete_event(event_id):
    response = dynamodb_client.delete_item(
        TableName=table_name,
        Key={'event_id': {'S': event_id}}
    )
    return response
