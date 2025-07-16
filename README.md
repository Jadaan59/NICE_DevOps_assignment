# NICE DevOps Assignment

## Project Overview
This project demonstrates how to build and deploy a fully automated serverless application on AWS using Infrastructure as Code (IaC). It is designed for students learning AWS, DevOps, and serverless concepts.

### Features
- All AWS resources are defined in code using AWS CDK (Python)
- Lambda function lists S3 objects and sends an SNS email notification
- S3 bucket is created and populated with sample files
- IAM role with least-privilege permissions
- SNS topic with email subscription
- CI/CD deployment using GitHub Actions
- Manual Lambda trigger for testing

---

## Project Structure
```
infra/           # AWS CDK code (Python)
lambda/          # Lambda function code (Python)
sample_files/    # Files to upload to S3 during deployment
EXPLANATION.md   # Detailed learning explanations
README.md        # This file
```

---

## Prerequisites
- AWS account with programmatic access (Access Key ID & Secret)
- AWS CLI configured locally (`aws configure`)
- Python 3.8+
- Node.js & npm (for AWS CDK CLI)
- AWS CDK CLI (`npm install -g aws-cdk`)
- Git

---

## Setup & Deployment
### 1. Clone the repository:

```sh
git clone https://github.com/Jadaan59/NICE_DevOps_assignment.git
cd NICE_DevOps_assignment
```

### 2. Install dependencies:

```sh
cd infra
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

### 3. Bootstrap your AWS environment (first time only):

```sh
cdk bootstrap
```

### 4. Deploy the stack:

```sh
cdk deploy
```
- You will see outputs for the S3 bucket, Lambda, and SNS topic.
- Check your email (the one you set in the code) and confirm the SNS subscription.

### 5. Upload sample files to S3:
- Add files to the `sample_files/` folder.
- Use the AWS CLI or a script to upload them (instructions will be provided).

---

## Manual Lambda Test
You can manually trigger the Lambda function for testing:

### Using AWS CLI:

```sh
aws lambda invoke \
  --function-name <LambdaFunctionName> \
  --payload '{}' \
  output.json
```
Replace `<LambdaFunctionName>` with the name output by the CDK deploy.

### Using AWS Console:
- Go to AWS Lambda in the console
- Find your function
- Click "Test" and use an empty event (`{}`)

---

## GitHub Actions CI/CD
- The project includes a GitHub Actions workflow (to be added) that deploys your stack when manually triggered from GitHub.
- You must add your AWS credentials as GitHub repository secrets (`AWS_ACCESS_KEY_ID`, `AWS_SECRET_ACCESS_KEY`, and optionally `AWS_REGION`).

---

## Learning Resources
- See `EXPLANATION.md` for a detailed explanation of each part of the project.
- AWS CDK Docs: https://docs.aws.amazon.com/cdk/latest/guide/home.html
- AWS Lambda Docs: https://docs.aws.amazon.com/lambda/latest/dg/welcome.html
- AWS S3 Docs: https://docs.aws.amazon.com/s3/index.html
- AWS SNS Docs: https://docs.aws.amazon.com/sns/latest/dg/welcome.html

---

## Notes
- This project uses placeholder values for the S3 bucket name and SNS email. Change them in the code before deploying to your own AWS account.
- The S3 bucket and all resources will be **destroyed** if you delete the stack (for learning/demo only).
- For any questions, see the code comments and `EXPLANATION.md`. 