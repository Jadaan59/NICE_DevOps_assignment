import boto3
import os
import json
import logging

# Configure logging
logger = logging.getLogger()
logger.setLevel(logging.INFO)

def lambda_handler(event, context):
    """
    AWS Lambda function that lists all objects in an S3 bucket and sends an SNS notification.
    
    Args:
        event: Lambda event object
        context: Lambda context object
        
    Returns:
        dict: Response containing execution status and bucket information
    """
    s3 = boto3.client('s3')
    sns = boto3.client('sns')
    bucket_name = os.environ.get('BUCKET_NAME')
    sns_topic_arn = os.environ.get('SNS_TOPIC_ARN')

    if not bucket_name or not sns_topic_arn:
        error_msg = "Missing required environment variables: BUCKET_NAME or SNS_TOPIC_ARN"
        logger.error(error_msg)
        return {
            'statusCode': 500,
            'body': json.dumps({'error': error_msg})
        }

    # List objects in the S3 bucket
    try:
        logger.info(f"Listing objects in bucket: {bucket_name}")
        response = s3.list_objects_v2(Bucket=bucket_name)
        objects = response.get('Contents', [])
        object_keys = [obj['Key'] for obj in objects]
        logger.info(f"Found {len(object_keys)} objects in bucket")
    except Exception as e:
        object_keys = []
        error_message = f"Error listing objects in bucket {bucket_name}: {str(e)}"
        logger.error(error_message)
    else:
        error_message = None

    # Prepare the notification message
    message = {
        'bucket': bucket_name,
        'object_count': len(object_keys),
        'objects': object_keys,
        'error': error_message,
        'event': event,
        'timestamp': context.get_remaining_time_in_millis()
    }

    # Publish to SNS topic
    try:
        logger.info(f"Publishing message to SNS topic: {sns_topic_arn}")
        sns.publish(
            TopicArn=sns_topic_arn,
            Message=json.dumps(message, default=str),
            Subject=f"Lambda Execution Report - {bucket_name}"
        )
        logger.info("Successfully published message to SNS")
    except Exception as e:
        error_msg = f"Error publishing to SNS: {str(e)}"
        logger.error(error_msg)
        message['sns_error'] = error_msg

    return {
        'statusCode': 200 if not error_message else 500,
        'body': json.dumps(message, default=str)
    } 