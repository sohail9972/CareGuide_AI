# AWS Bedrock Infrastructure Setup - Complete Guide

Complete, step-by-step guide to deploy CareGuide AI on AWS with Bedrock infrastructure.

## 📋 Table of Contents

1. [Quick Start](#quick-start-5-minutes)
2. [Prerequisites](#prerequisites)
3. [Setup Steps](#setup-steps)
4. [Configuration & Testing](#configuration--testing)
5. [Production Deployment](#production-deployment)
6. [Troubleshooting](#troubleshooting)

---

## Quick Start (5 minutes)

For AWS-experienced users:

```bash
# 1. Clone and navigate
git clone <your-repo>
cd CareGuide_AI

# 2. Run interactive setup wizard
cd scripts
python aws_setup_wizard.py

# 3. Update backend/.env with returned IDs
# 4. Deploy Lambda and test
cd ../backend
python -m uvicorn app.main:app --reload
```

**Full guide below for detailed instructions.**

---

## Prerequisites

### AWS Account Requirements
- ✅ AWS account with billing enabled
- ✅ IAM permissions to create: EC2, Lambda, S3, DynamoDB, Bedrock
- ✅ Bedrock model access approved (Claude 3.5 Sonnet, Titan Embeddings)

### Local Requirements
- ✅ **Python 3.11+** installed
- ✅ **AWS CLI** configured (`aws configure`)
- ✅ **Git** for version control
- ✅ **pip** package manager
- ✅ **Virtual environment** (optional but recommended)

### Verify Prerequisites
```bash
# Check Python version
python --version

# Check AWS CLI
aws sts get-caller-identity

# Install boto3
pip install boto3
```

---

## Setup Steps

### Step 1: Enable Bedrock Models (5-10 minutes)

Before anything else, request access to Claude models:

1. **Go to AWS Console**:
   - Login to AWS Management Console
   - Navigate to **Bedrock** service
   - Click **Model access** (left sidebar under "Get started")

2. **Request Model Access**:
   - Click **Request model access**
   - Check: `Claude 3.5 Sonnet` (required for vision)
   - Check: `Titan Embeddings G1` (required for KB)
   - Click **Request access** and wait for confirmation (usually immediate)

3. **Verify Access**:
   ```bash
   aws bedrock list-foundation-models --region us-east-1 | grep -i claude
   ```

### Step 2: Get AWS Account ID

```bash
# Save to environment variable
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
echo "Account ID: $ACCOUNT_ID"
```

### Step 3: Create S3 Buckets

```bash
# Create three S3 buckets
aws s3 mb s3://careguide-prescriptions-$ACCOUNT_ID --region us-east-1
aws s3 mb s3://careguide-kb-bucket-$ACCOUNT_ID --region us-east-1
aws s3 mb s3://careguide-results-$ACCOUNT_ID --region us-east-1

# Enable versioning for safety
aws s3api put-bucket-versioning \
  --bucket careguide-prescriptions-$ACCOUNT_ID \
  --versioning-configuration Status=Enabled --region us-east-1
```

**Verify**:
```bash
aws s3 ls | grep careguide
```

### Step 4: Create IAM Roles

**Option A: Automatic (Recommended)**

```bash
cd scripts
python create_iam_roles.py
```

This creates three roles with appropriate permissions:
- `BedrockAgentExecutionRole` - For Bedrock Agent
- `BedrockKBExecutionRole` - For Knowledge Base
- `CareGuideAgentLambdaRole` - For Lambda function

**Option B: Manual via AWS Console**

If automatic fails, create manually:
1. Go to **IAM** → **Roles** → **Create role**
2. Trusted entity: **AWS Service** → **bedrock.amazonaws.com**
3. Attach policies from `scripts/policies/`

### Step 5: Setup OpenSearch (for Knowledge Base Vector Storage)

**Option A: OpenSearch Serverless (No provisioning required)**

```bash
# Create serverless collection
aws opensearchserverless create-collection \
  --name careguide-kb-collection \
  --type SEARCH \
  --region us-east-1
```

**Option B: Self-Managed OpenSearch Domain**

```bash
# Requires more configuration
# See AWS_SETUP_GUIDE.md for detailed instructions
```

### Step 6: Create Bedrock Knowledge Base

The Knowledge Base stores medicine information for RAG (Retrieval-Augmented Generation).

```bash
# Update script with your account ID first
nano scripts/setup_bedrock_agent.py

# Find and replace:
# YOUR_ACCOUNT_ID → your actual account ID (from Step 2)
# careguide-kb-collection ARN → your OpenSearch collection ARN

# Create KB and Agent
python scripts/setup_bedrock_agent.py
```

**Save the returned**:
- `BEDROCK_KB_ID` - Knowledge Base ID
- `BEDROCK_AGENT_ID` - Agent ID

### Step 7: Populate Knowledge Base with Medicine Data

```bash
# Ingest sample medicine data
cd scripts
python ingest_knowledge_base.py
```

This ingests:
- RxNorm medicine names and classifications
- Dosages and administration guidelines
- Side effects and contraindications
- Drug interactions and warnings

### Step 8: Configure Backend Environment

Create `.env` file in `backend/` directory:

```bash
cd backend

# Create .env with your values
cat > .env << EOF
# AWS Configuration
AWS_REGION=us-east-1
AWS_ACCOUNT_ID=$ACCOUNT_ID

# Bedrock Configuration
BEDROCK_AGENT_ID=<paste-from-step-6>
BEDROCK_KB_ID=<paste-from-step-6>

# S3 Buckets
S3_BUCKET_PRESCRIPTIONS=careguide-prescriptions-$ACCOUNT_ID
S3_BUCKET_DOCUMENTS=careguide-kb-bucket-$ACCOUNT_ID
S3_BUCKET_RESULTS=careguide-results-$ACCOUNT_ID

# Lambda
LAMBDA_FUNCTION_NAME=careguide-prescription-processor-dev

# DynamoDB
DYNAMODB_TABLE=prescription-results-dev
EOF

# Verify
cat .env
```

### Step 9: Setup DynamoDB (Results Storage)

```bash
# The Lambda deployment template includes this
# Or create manually:

aws dynamodb create-table \
  --table-name prescription-results-dev \
  --attribute-definitions \
    AttributeName=prescriptionId,AttributeType=S \
    AttributeName=timestamp,AttributeType=N \
  --key-schema \
    AttributeName=prescriptionId,KeyType=HASH \
    AttributeName=timestamp,KeyType=RANGE \
  --billing-mode PAY_PER_REQUEST \
  --region us-east-1
```

### Step 10: Deploy Lambda Function

```bash
cd backend

# Create deployment package
mkdir -p lambda-deployment
pip install -r requirements.txt -t lambda-deployment/
cp aws_lambda_handler.py lambda-deployment/

# Create zip
(cd lambda-deployment && zip -r ../lambda_function.zip . && cd ..)

# Deploy
aws lambda create-function \
  --function-name careguide-prescription-processor-dev \
  --runtime python3.11 \
  --role arn:aws:iam::$ACCOUNT_ID:role/CareGuideAgentLambdaRole \
  --handler aws_lambda_handler.lambda_handler \
  --zip-file fileb://lambda_function.zip \
  --timeout 120 \
  --memory-size 512 \
  --environment Variables='
  { 
    AWS_REGION=us-east-1,
    BEDROCK_AGENT_ID=<your-agent-id>,
    BEDROCK_KB_ID=<your-kb-id>,
    OUTPUT_BUCKET=careguide-results-'$ACCOUNT_ID',
    RESULTS_TABLE=prescription-results-dev
  }' \
  --region us-east-1
```

**Verify**:
```bash
aws lambda get-function --function-name careguide-prescription-processor-dev --region us-east-1
```

### Step 11: Configure S3 Event Trigger

Link S3 bucket to Lambda:

```bash
# Give S3 permission to invoke Lambda
aws lambda add-permission \
  --function-name careguide-prescription-processor-dev \
  --statement-id AllowS3Invoke \
  --action lambda:InvokeFunction \
  --principal s3.amazonaws.com \
  --source-arn arn:aws:s3:::careguide-prescriptions-$ACCOUNT_ID \
  --region us-east-1

# Configure bucket notification
cat > notification.json << EOF
{
  "LambdaFunctionConfigurations": [
    {
      "LambdaFunctionArn": "arn:aws:lambda:us-east-1:$ACCOUNT_ID:function:careguide-prescription-processor-dev",
      "Events": ["s3:ObjectCreated:*"],
      "Filter": {
        "Key": {
          "FilterRules": [
            {"Name": "suffix", "Value": ".jpg"},
            {"Name": "suffix", "Value": ".png"}
          ]
        }
      }
    }
  ]
}
EOF

aws s3api put-bucket-notification-configuration \
  --bucket careguide-prescriptions-$ACCOUNT_ID \
  --notification-configuration file://notification.json \
  --region us-east-1
```

---

## Configuration & Testing

### Test 1: Backend API Local

```bash
# Start backend
cd backend
python -m uvicorn app.main:app --reload

# In another terminal, test local provider
curl -X POST http://localhost:8000/upload-prescription \
  -F "file=@../test-prescription.jpg" \
  -F "provider=local" \
  -F "language=en"
```

**Expected response**: JSON with extracted medicines

### Test 2: Bedrock Agent Direct

```bash
# Test agent invocation
aws bedrock-agent-runtime invoke-agent \
  --agent-id $BEDROCK_AGENT_ID \
  --agent-alias-id AIDACKQG5WD3S \
  --session-id test-1 \
  --input-text "What are the side effects of Aspirin?" \
  --region us-east-1
```

### Test 3: Lambda Function

```bash
# Create test event
cat > test-event.json << EOF
{
  "Records": [{
    "s3": {
      "bucket": {"name": "careguide-prescriptions-$ACCOUNT_ID"},
      "object": {"key": "test-prescription.jpg"}
    }
  }]
}
EOF

# Invoke Lambda
aws lambda invoke \
  --function-name careguide-prescription-processor-dev \
  --payload file://test-event.json \
  response.json \
  --region us-east-1

# Check response
cat response.json | jq .
```

### Test 4: End-to-End Flow

```bash
# Upload prescription (triggers Lambda automatically)
aws s3 cp test-prescription.jpg s3://careguide-prescriptions-$ACCOUNT_ID/

# Wait 5 seconds for processing
sleep 5

# Check results
aws s3 ls s3://careguide-results-$ACCOUNT_ID/results/

# View result
aws s3 cp s3://careguide-results-$ACCOUNT_ID/results/test-prescription.json . && jq . test-prescription.json
```

### View Logs

```bash
# Real-time Lambda logs
aws logs tail /aws/lambda/careguide-prescription-processor-dev --follow

# Recent errors
aws logs filter-log-events \
  --log-group-name /aws/lambda/careguide-prescription-processor-dev \
  --filter-pattern ERROR
```

---

## Production Deployment

### Update Lambda with New Code

```bash
# After making changes
cd backend
pip install -r requirements.txt -t lambda-deployment/
cp aws_lambda_handler.py lambda-deployment/
(cd lambda-deployment && zip -r ../lambda_function.zip . && cd ..)

# Deploy update
aws lambda update-function-code \
  --function-name careguide-prescription-processor-dev \
  --zip-file fileb://lambda_function.zip \
  --region us-east-1
```

### Deploy Using SAM (AWS Serverless Application Model)

```bash
# Install SAM CLI
pip install aws-sam-cli

# Deploy stack
sam deploy \
  --template-file backend/template.yaml \
  --stack-name careguide-prod \
  --parameter-overrides \
      EnvironmentName=prod \
      BedrockAgentId=$BEDROCK_AGENT_ID \
  --capabilities CAPABILITY_NAMED_IAM
```

### Enable CloudWatch Monitoring

```bash
# Create dashboard
aws cloudwatch put-dashboard \
  --dashboard-name CareGuideAI \
  --dashboard-body file://cloudwatch-dashboard.json

# Set up alarms
aws cloudwatch put-metric-alarm \
  --alarm-name careguide-lambda-errors \
  --alarm-description "Alert on Lambda errors" \
  --metric-name Errors \
  --namespace AWS/Lambda \
  --statistic Sum \
  --period 300 \
  --threshold 5 \
  --comparison-operator GreaterThanThreshold
```

### Enable Encryption

```bash
# S3 bucket encryption
aws s3api put-bucket-encryption \
  --bucket careguide-prescriptions-$ACCOUNT_ID \
  --server-side-encryption-configuration '{"Rules":[{"ApplyServerSideEncryptionByDefault":{"SSEAlgorithm":"AES256"}}]}'

# DynamoDB encryption
aws dynamodb update-table \
  --table-name prescription-results-prod \
  --sse-specification Enabled=true,SSEType=KMS
```

---

## Troubleshooting

### Issue: "No module named 'boto3'"
**Solution**: Install dependencies
```bash
pip install boto3
```

### Issue: "Access Denied" when calling Bedrock
**Solution**: Check IAM role
```bash
# Verify role has bedrock:InvokeModel permission
aws iam get-role-policy \
  --role-name CareGuideAgentLambdaRole \
  --policy-name LambdaPolicy
```

### Issue: Lambda timeout (>120 seconds)
**Solution**: Increase timeout
```bash
aws lambda update-function-configuration \
  --function-name careguide-prescription-processor-dev \
  --timeout 180 \
  --region us-east-1
```

### Issue: Results not in S3
**Solution**: Check Lambda logs
```bash
aws logs tail /aws/lambda/careguide-prescription-processor-dev --follow
```

### Issue: High AWS costs
**Solution**: Review and optimize
```bash
# Check Bedrock usage
aws cloudwatch get-metric-statistics \
  --namespace AWS/Bedrock \
  --metric-name TokenCount \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-12-31T23:59:59Z \
  --period 86400 \
  --statistics Sum
```

---

## Quick Reference Commands

```bash
# Get account ID
aws sts get-caller-identity --query Account --output text

# List S3 buckets
aws s3 ls | grep careguide

# View Bedrock agents
aws bedrock-agent list-agents --region us-east-1

# Tail Lambda logs
aws logs tail /aws/lambda/careguide-prescription-processor-dev --follow

# Invoke Lambda
aws lambda invoke --function-name careguide-prescription-processor-dev --payload '{}' response.json

# Check costs
aws ce get-cost-and-usage --time-period Start=2024-01-01,End=2024-12-31 --granularity DAILY --metrics UnblendedCost --group-by Type=DIMENSION,Key=SERVICE

# Clean up resources
aws s3 rm s3://careguide-prescriptions-$ACCOUNT_ID --recursive
aws dynamodb delete-table --table-name prescription-results-dev
aws lambda delete-function --function-name careguide-prescription-processor-dev
```

---

## Next Steps

1. ✅ Complete all setup steps above
2. ✅ Run comprehensive tests (see `AWS_TESTING_GUIDE.md`)
3. ✅ Deploy Django/FastAPI backend with Load Balancer
4. ✅ Deploy Next.js frontend to Vercel
5. ✅ Set up CI/CD pipeline with GitHub Actions
6. ✅ Monitor costs and performance

## Support & Documentation

- **AWS Bedrock**: https://docs.aws.amazon.com/bedrock/
- **AWS Lambda**: https://docs.aws.amazon.com/lambda/
- **Boto3 Documentation**: https://boto3.amazonaws.com/v1/documentation/api/latest/index.html
- **CloudWatch Logs**: https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/

---

**Last Updated**: 2024
**CareGuide AI Version**: 1.0
