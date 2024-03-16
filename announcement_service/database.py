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
table_name = 'announcements'

# Get a reference to the DynamoDB table
table = dynamodb.Table(table_name)

def create_announcement( announcement_name, announcement_start_date,announcement_end_date, announcement_description, email,image_data=None):
    announcement_id = str(uuid.uuid4())
    announcement_submitted_time = datetime.now().isoformat()
    print(image_data)
    # Prepare the item to be stored in DynamoDB
    item = {
        'announcement_id':   announcement_id,
        'announcement_name': announcement_name,
        'announcement_start_date': announcement_start_date,
        'announcement_end_date': announcement_end_date,
        'announcement_submitted_time': announcement_submitted_time,
        'announcement_description': announcement_description,
        'email': email,
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



def get_all_announcement():
    try:
        response = table.scan()
        items = response.get('Items', [])
        return items
    except botocore.exceptions.ClientError as e:
        # Handle the error, log it, or return an empty list
        print(f"Error: {e}")
        return []
    
# Define a function to retrieve an event by event_id
def get_announcement(announcement_id):
    response = dynamodb_client.get_item(
        TableName=table_name,
        Key={'announcement_id': {'S': announcement_id}}
    )
    item = response.get('Item')
    return item


def update_announcement(announcement_id, announcement_name, announcement_start_date, announcement_end_date, announcement_description):
    try:
        response = table.update_item(
            Key={'announcement_id': announcement_id},
            UpdateExpression='SET announcement_name = :name, announcement_start_date = :start_date, announcement_end_date = :end_date, announcement_description = :description',
            ExpressionAttributeValues={
                ':name': announcement_name,
                ':start_date': announcement_start_date,
                ':end_date': announcement_end_date,
                ':description': announcement_description,
            },
            ReturnValues='UPDATED_NEW'
        )
        return response
    except Exception as e:
        print(f"Error updating announcement: {e}")
        return None

# Define a function to delete an event
def delete_announcement(announcement_id):
    response = dynamodb_client.delete_item(
        TableName=table_name,
        Key={'announcement_id': {'S': announcement_id}}
    )
    return response

