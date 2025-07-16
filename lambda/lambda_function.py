import boto3
import os
import json

def lambda_handler(event, context):
    """
    AWS Lambda function to list all objects in a specified S3 bucket and send an SNS notification.
    - Lists all objects in the S3 bucket defined by the BUCKET_NAME environment variable.
    - Publishes a message to the SNS topic defined by the SNS_TOPIC_ARN environment variable.
    """
    s3 = boto3.client('s3')
    sns = boto3.client('sns')
    bucket_name = os.environ.get('BUCKET_NAME')
    sns_topic_arn = os.environ.get('SNS_TOPIC_ARN')

    # List objects in the S3 bucket
    try:
        response = s3.list_objects_v2(Bucket=bucket_name)
        objects = response.get('Contents', [])
        object_keys = [obj['Key'] for obj in objects]
    except Exception as e:
        object_keys = []
        error_message = f"Error listing objects in bucket {bucket_name}: {str(e)}"
    else:
        error_message = None

    # Prepare the message
    message = {
        'bucket': bucket_name,
        'object_count': len(object_keys),
        'objects': object_keys,
        'error': error_message,
        'event': event
    }

    # Publish to SNS
    try:
        sns.publish(
            TopicArn=sns_topic_arn,
            Message=json.dumps(message),
            Subject=f"Lambda Execution Report for {bucket_name}"
        )
    except Exception as e:
        print(f"Error publishing to SNS: {str(e)}")

    return {
        'statusCode': 200 if not error_message else 500,
        'body': json.dumps(message)
    } 