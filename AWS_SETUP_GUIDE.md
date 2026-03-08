# AWS Bedrock Infrastructure Setup Guide

## Overview

This guide walks you through setting up the complete AWS Bedrock infrastructure for CareGuide AI, including:
- Bedrock Agent with vision and RAG capabilities
- Bedrock Knowledge Base for medicine data
- Lambda function for serverless processing
- S3 buckets for image and document storage
- IAM roles and permissions

## Prerequisites

1. **AWS Account** with appropriate permissions
2. **AWS CLI** configured: `aws configure`
3. **Python 3.11+** with boto3 installed
4. **AWS Bedrock Access**: Request access to Claude 3.5 Sonnet in your region
5. **Account ID**: You can find this with `aws sts get-caller-identity`

## Step 1: Prepare AWS Environment

### 1.1 Get Your AWS Account ID
```bash
aws sts get-caller-identity
```
Save the `Account` value - you'll need this throughout.

### 1.2 Enable Bedrock Models

Go to AWS Console → Bedrock → Model Access → Request Access to:
- Claude 3.5 Sonnet
- Titan Embeddings G1

This may take a few minutes to process.

### 1.3 Set Environment Variables
```bash
# On Windows PowerShell
$env:AWS_REGION = "us-east-1"
$env:AWS_ACCOUNT_ID = "YOUR_ACCOUNT_ID_HERE"

# On macOS/Linux bash
export AWS_REGION="us-east-1"
export AWS_ACCOUNT_ID="YOUR_ACCOUNT_ID_HERE"
```

## Step 2: Create S3 Buckets

```bash
# Create bucket for prescription images
aws s3 mb s3://careguide-prescriptions --region us-east-1

# Create bucket for documents (KB source)
aws s3 mb s3://careguide-kb-bucket --region us-east-1

# Create bucket for Lambda logs
aws s3 mb s3://careguide-logs --region us-east-1

# Enable versioning for safety
aws s3api put-bucket-versioning \
  --bucket careguide-prescriptions \
  --versioning-configuration Status=Enabled

aws s3api put-bucket-versioning \
  --bucket careguide-kb-bucket \
  --versioning-configuration Status=Enabled
```

## Step 3: Create IAM Roles

### 3.1 Automatic Role Creation (Recommended)
```bash
cd scripts

# This creates all necessary roles
python create_iam_roles.py
```

### 3.2 Manual Role Creation (Alternative)

If you prefer to create roles manually:

1. Go to AWS Console → IAM → Roles → Create Role
2. Trusted entity: AWS Service → bedrock.amazonaws.com
3. Add permissions:
   - Use the policies from `scripts/policies/bedrock_agent_policy.json`
   - Use the policies from `scripts/policies/bedrock_kb_policy.json`

**Save the Role ARN** for the next step.

## Step 4: Create OpenSearch Domain (for Knowledge Base)

Bedrock Knowledge Bases require OpenSearch for vector storage. You have two options:

### Option A: AWS-Managed OpenSearch
```bash
# Create domain
aws opensearchserverless create-collection \
  --name careguide-kb-collection \
  --type SEARCH \
  --region us-east-1

# This creates a serverless OpenSearch cluster
# Save the Collection ARN for Knowledge Base creation
```

### Option B: Self-Managed OpenSearch Domain
```bash
aws opensearch create-domain \
  --domain-name careguide-kb-domain \
  --elasticsearch-version 7.10 \
  --instance-type t3.small.search \
  --instance-count 1 \
  --ebs-options VolumeSize=10,VolumeType=gp2 \
  --access-policies file://opensearch-policy.json \
  --region us-east-1
```

**Create `opensearch-policy.json`:**
```json
{
  "Version": "2012-10-17",
  "Statement": [
    {
      "Effect": "Allow",
      "Principal": {
        "Service": "bedrock.amazonaws.com"
      },
      "Action": "es:*",
      "Resource": "arn:aws:es:*:YOUR_ACCOUNT_ID:domain/careguide-kb-domain/*"
    }
  ]
}
```

## Step 5: Create Bedrock Knowledge Base

### 5.1 Prepare Knowledge Base Configuration

Create `kb-config.json`:
```json
{
  "name": "CareGuide-Medicine-KB",
  "description": "Medicine knowledge base for prescription analysis",
  "dataSourceConfiguration": {
    "s3Configuration": {
      "bucketArn": "arn:aws:s3:::careguide-kb-bucket"
    }
  },
  "storageConfiguration": {
    "type": "OPENSEARCH_SERVERLESS",
    "opensearchServerlessConfiguration": {
      "collectionArn": "arn:aws:aoss:us-east-1:YOUR_ACCOUNT_ID:collection/careguide-kb-collection"
    }
  },
  "roleArn": "arn:aws:iam::YOUR_ACCOUNT_ID:role/BedrockKBExecutionRole"
}
```

### 5.2 Create Knowledge Base
```bash
aws bedrock-agent create-knowledge-base \
  --name "CareGuide-Medicine-KB" \
  --description "Medicine knowledge base for prescription analysis" \
  --role-arn "arn:aws:iam::YOUR_ACCOUNT_ID:role/BedrockKBExecutionRole" \
  --knowledge-base-configuration "type=VECTOR" \
  --storage-configuration type=OPENSEARCH_SERVERLESS,opensearchServerlessConfiguration="{collectionArn=arn:aws:aoss:us-east-1:YOUR_ACCOUNT_ID:collection/careguide-kb-collection}" \
  --region us-east-1
```

Save the `knowledgeBaseId` from the response.

### 5.3 Create Data Source (S3)
```bash
aws bedrock-agent create-data-source \
  --knowledge-base-id KB_ID_FROM_ABOVE \
  --name "S3-Medicine-Documents" \
  --data-source-configuration "s3Configuration={bucketArn=arn:aws:s3:::careguide-kb-bucket}" \
  --region us-east-1
```

## Step 6: Populate Knowledge Base

### 6.1 Upload Medicine Data to S3
```bash
cd scripts

# This generates and uploads sample medicine documents
python ingest_knowledge_base.py
```

### 6.2 Ingest Documents
```bash
# Update KB_ID in the script, then run:
python ingest_knowledge_base.py
```

The script will:
1. Fetch RxNorm sample medicines
2. Create text chunks optimized for embedding
3. Upload to S3
4. Optionally enrich with OpenFDA adverse events

## Step 7: Create Bedrock Agent

### 7.1 Update Setup Script
Edit `scripts/setup_bedrock_agent.py`:
- Replace `YOUR_ACCOUNT_ID` with your actual account ID
- Replace `KB_ID_PLACEHOLDER` with the KB ID from Step 5
- Replace `AGENT_ROLE_ARN` with the Bedrock Agent role ARN from Step 3

### 7.2 Run Agent Setup
```bash
python scripts/setup_bedrock_agent.py
```

This creates a Bedrock Agent with:
- **Vision Tool**: Analyze prescription images using Claude 3.5 Sonnet
- **RAG Tool**: Query knowledge base for medicine information
- **Translation Tool**: Generate multilingual guidance

Save the `agentId` from the response.

## Step 8: Configure Backend Environment

### 8.1 Create `.env` file in `backend/`
```
AWS_REGION=us-east-1
AWS_ACCOUNT_ID=YOUR_ACCOUNT_ID
BEDROCK_AGENT_ID=AGENT_ID_FROM_STEP_7
BEDROCK_KB_ID=KB_ID_FROM_STEP_5
S3_BUCKET_PRESCRIPTIONS=careguide-prescriptions
S3_BUCKET_DOCUMENTS=careguide-kb-bucket
```

### 8.2 Update Backend Configuration
In `backend/app/main.py`:
```python
import os

BEDROCK_AGENT_ID = os.getenv("BEDROCK_AGENT_ID")
BEDROCK_KB_ID = os.getenv("BEDROCK_KB_ID")
S3_BUCKET = os.getenv("S3_BUCKET_PRESCRIPTIONS")
```

## Step 9: Deploy Lambda Function

### 9.1 Create Deployment Package
```bash
cd backend

# Create deployment directory
mkdir -p lambda-deployment
pip install -r requirements.txt -t lambda-deployment/

# Copy Lambda handler
cp app/aws_lambda_handler.py lambda-deployment/

# Zip the package
(cd lambda-deployment && zip -r ../lambda_function.zip .)
```

### 9.2 Deploy to Lambda
```bash
aws lambda create-function \
  --function-name careguide-prescription-processor \
  --runtime python3.11 \
  --role arn:aws:iam::YOUR_ACCOUNT_ID:role/CareGuideAgentLambdaRole \
  --handler aws_lambda_handler.handler \
  --zip-file fileb://lambda_function.zip \
  --timeout 60 \
  --memory-size 512 \
  --environment "Variables={AWS_REGION=us-east-1,BEDROCK_AGENT_ID=AGENT_ID,BEDROCK_KB_ID=KB_ID}" \
  --region us-east-1
```

### 9.3 Create S3 Event Trigger
```bash
# Create permission for S3 to invoke Lambda
aws lambda add-permission \
  --function-name careguide-prescription-processor \
  --statement-id AllowS3Invoke \
  --action lambda:InvokeFunction \
  --principal s3.amazonaws.com \
  --source-arn arn:aws:s3:::careguide-prescriptions \
  --region us-east-1

# Create notification on S3 bucket
aws s3api put-bucket-notification-configuration \
  --bucket careguide-prescriptions \
  --notification-configuration '{
    "LambdaFunctionConfigurations": [
      {
        "LambdaFunctionArn": "arn:aws:lambda:us-east-1:YOUR_ACCOUNT_ID:function:careguide-prescription-processor",
        "Events": ["s3:ObjectCreated:*"],
        "Filter": {
          "Key": {
            "FilterRules": [
              {
                "Name": "suffix",
                "Value": ".jpg"
              },
              {
                "Name": "suffix",
                "Value": ".png"
              }
            ]
          }
        }
      }
    ]
  }' \
  --region us-east-1
```

## Step 10: Test the Setup

### 10.1 Test Bedrock Agent Directly
```bash
# Query the agent
aws bedrock-agent-runtime invoke-agent \
  --agent-id AGENT_ID \
  --agent-alias-id AGENT_ALIAS_ID \
  --session-id test-session-1 \
  --input-text "What are the common side effects of Aspirin?" \
  --region us-east-1
```

### 10.2 Test Backend API
```bash
# Start the backend
cd backend
python -m uvicorn app.main:app --reload

# In another terminal, test the AWS provider
curl -X POST http://localhost:8000/upload-prescription \
  -F "file=@path/to/prescription.jpg" \
  -F "provider=aws" \
  -F "language=en"
```

### 10.3 Test Lambda Function
```bash
# Upload an image to trigger Lambda
aws s3 cp test_prescription.jpg s3://careguide-prescriptions/

# Check CloudWatch logs
aws logs tail /aws/lambda/careguide-prescription-processor --follow
```

## Step 11: Monitor and Optimize

### 11.1 CloudWatch Monitoring
```bash
# View Lambda invocations
aws logs tail /aws/lambda/careguide-prescription-processor --follow

# View Bedrock Agent logs
aws logs tail /aws/bedrock/agent/careguide --follow
```

### 11.2 Costs
Monitor costs with AWS Cost Explorer:
- Bedrock model invocations (primary cost)
- S3 storage and requests
- OpenSearch cluster (if not serverless)
- Lambda executions

### 11.3 Performance Tuning
- **Model**: Consider Claude 3.5 Haiku for cost savings
- **KB**: Optimize chunking strategy for better RAG
- **Lambda**: Increase memory for faster cold starts

## Troubleshooting

### Knowledge Base Not Finding Documents
```bash
# Verify data source status
aws bedrock-agent get-data-source \
  --knowledge-base-id KB_ID \
  --data-source-id DS_ID \
  --region us-east-1
```

### Lambda Timeout Issues
- Increase timeout: `--timeout 120`
- Increase memory: `--memory-size 1024`

### Bedrock Model Access Denied
- Verify model is enabled in Bedrock console
- Check IAM role has `bedrock:InvokeModel` permission

### OpenSearch Connection Failed
- Verify security group allows traffic from Lambda
- Check collection/domain status in OpenSearch console

## Next Steps

1. Populate Knowledge Base with real medicine data from RxNorm
2. Set up CI/CD pipeline to auto-deploy Lambda updates
3. Create API Gateway for better rate limiting and authentication
4. Add X-Ray tracing for performance monitoring
5. Implement DynamoDB for prescription analysis history

## Useful Commands Reference

```bash
# List all Bedrock Agents
aws bedrock-agent list-agents --region us-east-1

# List Knowledge Bases
aws bedrock-agent list-knowledge-bases --region us-east-1

# Check Lambda logs
aws logs tail /aws/lambda/careguide-prescription-processor --follow

# Update Lambda function code
aws lambda update-function-code \
  --function-name careguide-prescription-processor \
  --zip-file fileb://lambda_function.zip

# Delete resources (cleanup)
aws s3 rm s3://careguide-prescriptions --recursive
aws s3 rb s3://careguide-prescriptions
aws bedrock-agent delete-agent --agent-id AGENT_ID
aws opensearchserverless delete-collection --id COLLECTION_ID
```

## Support

For issues or questions:
1. Check AWS Bedrock documentation: https://docs.aws.amazon.com/bedrock/
2. Review CloudWatch logs for detailed error messages
3. Test with AWS CLI directly before testing backend
4. Verify all IAM permissions are correctly attached
