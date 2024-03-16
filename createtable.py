import boto3
import key_config as keys
# Get the service resource.

dynamodb =boto3.resource('dynamodb',
                         aws_access_key_id=keys.AWS_ACCESS_KEY_ID,
                         aws_secret_access_key=keys.AWS_SECRET_ACCESS_KEY,
                         region_name=keys.REGION_NAME)
# Create the DynamoDB table.
# table = dynamodb.create_table(
#     TableName='users',
#     KeySchema=[
#         {
#             'AttributeName': 'username',
#             'KeyType': 'HASH'
#         },
#         {
#             'AttributeName': 'last_name',
#             'KeyType': 'RANGE'
#         }
#     ],
#     AttributeDefinitions=[
#         {
#             'AttributeName': 'username',
#             'AttributeType': 'S'
#         },
#         {
#             'AttributeName': 'last_name',
#             'AttributeType': 'S'
#         },
#     ],
#     ProvisionedThroughput={
#         'ReadCapacityUnits': 5,
#         'WriteCapacityUnits': 5
#     }
# )

# Wait until the table exists.
# table.wait_until_exists()

# # Print out some data about the table.
# print(table.item_count)

