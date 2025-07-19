import boto3
import json
import sys

def main():
    """
    Script to manually invoke an AWS Lambda function for testing purposes.
    
    Usage:
        python invoke_lambda.py <function_name>
        python invoke_lambda.py  # Will prompt for function name
    """
    if len(sys.argv) > 1:
        function_name = sys.argv[1]
    else:
        function_name = input("Enter the Lambda function name: ")

    if not function_name.strip():
        print("Error: Function name cannot be empty")
        sys.exit(1)

    client = boto3.client('lambda')
    
    try:
        print(f"Invoking Lambda function: {function_name}")
        response = client.invoke(
            FunctionName=function_name,
            InvocationType='RequestResponse',
            Payload=json.dumps({})
        )
        
        print(f"Status code: {response['StatusCode']}")
        
        payload = response['Payload'].read()
        response_data = json.loads(payload.decode())
        
        print("Response payload:")
        print(json.dumps(response_data, indent=2))
        
        if response['StatusCode'] == 200:
            print("\n Lambda function executed successfully!")
        else:
            print(f"\n Lambda function failed with status code: {response['StatusCode']}")
            
    except client.exceptions.ResourceNotFoundException:
        print(f" Error: Lambda function '{function_name}' not found")
        print("Please check the function name and ensure it exists in your AWS account")
    except client.exceptions.ClientError as e:
        print(f" AWS Error: {e}")
    except Exception as e:
        print(f" Error invoking Lambda: {e}")

if __name__ == "__main__":
    main() 