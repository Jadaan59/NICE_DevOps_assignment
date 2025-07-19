from aws_cdk import (
    Stack,
    aws_s3 as s3,
    aws_lambda as _lambda,
    aws_iam as iam,
    aws_sns as sns,
    aws_sns_subscriptions as subs,
    Duration,
    CfnOutput,
)
from constructs import Construct
import os

class InfraStack(Stack):
    def __init__(self, scope: Construct, construct_id: str, **kwargs) -> None:
        super().__init__(scope, construct_id, **kwargs)

        # Configuration - Update these values before deployment
        bucket_name = "my-devops-assignment-bucket-" + os.getenv('CDK_DEFAULT_ACCOUNT', 'demo')
        email_address = os.getenv('SNS_EMAIL', 'your-email@example.com')  # Set this environment variable

        # Create S3 bucket for storing files
        bucket = s3.Bucket(self, "AssignmentBucket",
            bucket_name=bucket_name,
            removal_policy=s3.RemovalPolicy.DESTROY,
            auto_delete_objects=True
        )

        # Create SNS topic for Lambda execution notifications
        topic = sns.Topic(self, "AssignmentTopic",
            display_name="Lambda Execution Notifications"
        )

        # Add email subscription to receive notifications
        topic.add_subscription(subs.EmailSubscription(email_address))

        # Create IAM role for Lambda with least-privilege permissions
        lambda_role = iam.Role(self, "LambdaExecutionRole",
            assumed_by=iam.ServicePrincipal("lambda.amazonaws.com")
        )
        
        # Grant S3 read access to the specific bucket
        bucket.grant_read(lambda_role)
        
        # Grant SNS publish access to the topic
        topic.grant_publish(lambda_role)
        
        # Add basic Lambda execution permissions
        lambda_role.add_managed_policy(iam.ManagedPolicy.from_aws_managed_policy_name("service-role/AWSLambdaBasicExecutionRole"))

        # Create Lambda function
        lambda_fn = _lambda.Function(self, "ListS3AndNotifyLambda",
            runtime=_lambda.Runtime.PYTHON_3_9,
            handler="lambda_function.lambda_handler",
            code=_lambda.Code.from_asset(os.path.join(os.path.dirname(__file__), '../../lambda')),
            environment={
                "BUCKET_NAME": bucket.bucket_name,
                "SNS_TOPIC_ARN": topic.topic_arn
            },
            role=lambda_role,
            timeout=Duration.seconds(30)
        )

        # Output useful information for deployment
        CfnOutput(self, "BucketName", value=bucket.bucket_name)
        CfnOutput(self, "LambdaFunctionName", value=lambda_fn.function_name)
        CfnOutput(self, "SnsTopicArn", value=topic.topic_arn)
        CfnOutput(self, "SnsSubscriptionEmail", value=email_address)
