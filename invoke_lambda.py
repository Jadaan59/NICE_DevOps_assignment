import boto3
import json
import sys

# This script invokes an AWS Lambda function by name and prints the response.
# You must have AWS credentials configured (via aws configure or environment variables).

def main():
    if len(sys.argv) > 1:
        function_name = sys.argv[1]
    else:
        function_name = input("Enter the Lambda function name: ")

    client = boto3.client('lambda')
    try:
        response = client.invoke(
            FunctionName=function_name,
            InvocationType='RequestResponse',
            Payload=json.dumps({})
        )
        print("Status code:", response['StatusCode'])
        payload = response['Payload'].read()
        print("Response payload:", payload.decode())
    except Exception as e:
        print("Error invoking Lambda:", e)

if __name__ == "__main__":
    main() 