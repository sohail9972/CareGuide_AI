# CareGuide AI - AWS Quick Start Guide

## 🚀 5-Minute Setup

For experienced AWS users who want to get started immediately.

### Prerequisites
- AWS account with Bedrock access
- AWS CLI configured (`aws configure`)
- Python 3.11+
- boto3 installed (`pip install boto3`)

### Step 1: Get Your AWS Account ID
```bash
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
echo $ACCOUNT_ID
```

### Step 2: Run the Interactive Setup Wizard
```bash
cd scripts
python aws_setup_wizard.py
```

The wizard will:
- ✅ Create S3 buckets
- ✅ Create IAM roles
- ✅ Create Bedrock Agent & Knowledge Base
- ✅ Populate knowledge base with medicine data
- ✅ Generate `.env` file for backend

### Step 3: Deploy Lambda Function
```bash
cd backend
pip install -r requirements.txt -t lambda-deployment/
cp aws_lambda_handler.py lambda-deployment/
(cd lambda-deployment && zip -r ../lambda_function.zip .)

aws lambda create-function \
  --function-name careguide-prescription-processor-dev \
  --runtime python3.11 \
  --role arn:aws:iam::$ACCOUNT_ID:role/CareGuideAgentLambdaRole \
  --handler aws_lambda_handler.lambda_handler \
  --zip-file fileb://lambda_function.zip \
  --timeout 120 \
  --memory-size 512 \
  --environment "Variables={AWS_REGION=us-east-1,BEDROCK_AGENT_ID=YOUR_AGENT_ID,BEDROCK_KB_ID=YOUR_KB_ID}" \
  --region us-east-1
```

### Step 4: Test Locally
```bash
# Start backend
python -m uvicorn app.main:app --reload

# In another terminal, test with local provider
curl -X POST http://localhost:8000/upload-prescription \
  -F "file=@test-prescription.jpg" \
  -F "provider=local" \
  -F "language=en"

# Test with AWS provider (when Lambda is deployed)
curl -X POST http://localhost:8000/upload-prescription \
  -F "file=@test-prescription.jpg" \
  -F "provider=aws" \
  -F "language=en"
```

### Step 5: Test End-to-End
```bash
# Upload prescription to S3 (triggers Lambda automatically)
aws s3 cp test-prescription.jpg s3://careguide-prescriptions-$ACCOUNT_ID/

# Check results after a few seconds
aws s3 ls s3://careguide-results-$ACCOUNT_ID/results/

# View result
aws s3 cp s3://careguide-results-$ACCOUNT_ID/results/test-prescription.json . && cat test-prescription.json | jq .
```

## 📊 Architecture Overview

```
Prescription Image
       ↓
┌─────────────────────────────────────┐
│   S3 Bucket (careguide-prescriptions) │
└──────────────┬──────────────────────┘
               │
               ↓ (S3 ObjectCreated Event)
         ┌──────────────┐
         │  Lambda      │
         │  Function    │
         └──────────────┘
               │
        ┌──────┴──────┐
        ↓             ↓
  [Bedrock Agent]  [Knowledge Base]
        │             │
        └──────┬──────┘
               ↓
    ┌──────────────────────┐
    │  Claude 3.5 Sonnet   │
    │  (Vision + RAG)      │
    └──────────────────────┘
               ↓
    ┌──────────────────────┐
    │  Analysis Results    │
    │  (medicines, dosages,│
    │   interactions)      │
    └──────────────────────┘
               ↓
┌─────────────────────────────────────┐
│   S3 Bucket (careguide-results)      │
│   DynamoDB (prescription-results)    │
└─────────────────────────────────────┘
```

## 🧪 Common Test Commands

### Test S3 Access
```bash
aws s3 ls s3://careguide-prescriptions-$ACCOUNT_ID/
```

### Test Lambda Invocation
```bash
aws lambda invoke \
  --function-name careguide-prescription-processor-dev \
  --payload '{"Records":[{"s3":{"bucket":{"name":"careguide-prescriptions-'$ACCOUNT_ID'"},"object":{"key":"test.jpg"}}}]}' \
  response.json && cat response.json | jq .
```

### View Lambda Logs
```bash
aws logs tail /aws/lambda/careguide-prescription-processor-dev --follow
```

### Check DynamoDB Results
```bash
aws dynamodb scan --table-name prescription-results-dev --region us-east-1 | jq .
```

## 🔧 Troubleshooting

### Lambda Cannot Access Bedrock
```bash
# Check role permissions
aws iam get-role-policy --role-name CareGuideAgentLambdaRole --policy-name LambdaPolicy
```

### No Results in S3
```bash
# Check Lambda logs for errors
aws logs tail /aws/lambda/careguide-prescription-processor-dev --follow

# Check Lambda has permission
aws s3api head-bucket --bucket careguide-results-$ACCOUNT_ID
```

### DynamoDB Write Failures
```bash
# Check table exists and is accessible
aws dynamodb describe-table --table-name prescription-results-dev
```

## 📚 Detailed Guides

For more information:
- **Full Setup**: See `AWS_SETUP_GUIDE.md`
- **Testing**: See `AWS_TESTING_GUIDE.md`
- **Local Development**: See `backend/README.md`
- **Frontend Deployment**: See `careguide-frontend/README.md`

## ✅ Checklist

- [ ] AWS CLI configured
- [ ] Bedrock models enabled (Claude 3.5 Sonnet, Titan Embeddings)
- [ ] S3 buckets created
- [ ] IAM roles created
- [ ] Bedrock Agent created
- [ ] Knowledge Base created and populated
- [ ] Lambda function deployed
- [ ] S3 event notification configured
- [ ] `.env` file created in `backend/`
- [ ] Backend API tested locally
- [ ] End-to-end flow tested

## 🌐 Regional Considerations

CareGuide uses **us-east-1** by default. To use a different region:

1. Update `AWS_REGION` environment variable
2. Ensure Bedrock is available in your region
3. Create resources in the same region
4. Update Lambda environment variables

## 💰 Cost Estimation

Monthly costs for low volume (100 prescriptions/month):

- **Bedrock Invocations**: ~$2-5 (depends on agent usage)
- **S3 Storage & Requests**: ~$1-2
- **Lambda**: ~$0.50 (includes free tier)
- **DynamoDB**: Free (on-demand pricing)
- **OpenSearch Serverless**: ~$5-10

**Total: ~$10-20/month for development use**

For production (10,000 prescriptions/month):
- **Bedrock**: ~$200-500
- **S3**: ~$10-20
- **Lambda**: ~$5-10
- **DynamoDB**: ~$10-50
- **OpenSearch**: ~$50-100

**Total: ~$300-700/month**

## 🚢 Production Deployment

For production use:

1. **Use CloudFormation/SAM**: Deploy via `backend/template.yaml`
2. **Enable X-Ray Tracing**: For performance monitoring
3. **Set up API Gateway**: For REST API access to results
4. **Enable S3 Encryption**: Use KMS for sensitive data
5. **Set up Backups**: Configure DynamoDB PITR
6. **Monitor Costs**: Use AWS Cost Explorer
7. **Implement AutoScaling**: For variable load
8. **Set up Alarms**: For errors and latency

## 🤝 Support

Need help?

1. Check AWS Bedrock documentation: https://docs.aws.amazon.com/bedrock/
2. Review CloudWatch logs: `aws logs tail <log-group> --follow`
3. Test with AWS CLI: https://docs.aws.amazon.com/cli/latest/reference/
4. Check backend logs: See `backend/README.md`

## 📝 Environment Variables

Once setup is complete, your `.env` file should contain:

```
AWS_REGION=us-east-1
AWS_ACCOUNT_ID=123456789012
BEDROCK_AGENT_ID=YOUR_AGENT_ID
BEDROCK_KB_ID=YOUR_KB_ID
S3_BUCKET_PRESCRIPTIONS=careguide-prescriptions-123456789012
S3_BUCKET_DOCUMENTS=careguide-kb-bucket-123456789012
S3_BUCKET_RESULTS=careguide-results-123456789012
LAMBDA_FUNCTION_NAME=careguide-prescription-processor-dev
DYNAMODB_TABLE=prescription-results-dev
```

---

**Ready to get started? Run:**
```bash
cd scripts && python aws_setup_wizard.py
```
