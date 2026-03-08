# AWS Bedrock Testing Guide

This guide walks you through testing each component of the CareGuide AI AWS infrastructure.

## Prerequisites

- AWS CLI configured with proper credentials
- Python 3.11+ with boto3
- Sample prescription images (.jpg/.png)
- All infrastructure resources created (see `AWS_SETUP_GUIDE.md`)

## Test 1: S3 Bucket Access

### 1.1 Test Prescription Bucket Access
```bash
# List prescriptions bucket
aws s3 ls s3://careguide-prescriptions --region us-east-1

# Upload a test image
aws s3 cp test-prescription.jpg s3://careguide-prescriptions/

# Verify upload
aws s3 ls s3://careguide-prescriptions/

# Download and verify
aws s3 cp s3://careguide-prescriptions/test-prescription.jpg . --region us-east-1
```

### 1.2 Test Results Bucket Access
```bash
# List results bucket
aws s3 ls s3://careguide-results --region us-east-1

# Create a test file
echo '{"test": "data"}' > test-result.json

# Upload test result
aws s3 cp test-result.json s3://careguide-results/

# Verify
aws s3 ls s3://careguide-results/
```

## Test 2: Bedrock Agent Access

### 2.1 Check Agent Status
```bash
# List all agents
aws bedrock-agent list-agents --region us-east-1

# Get specific agent details
aws bedrock-agent get-agent \
  --agent-id YOUR_AGENT_ID \
  --region us-east-1

# Get agent alias
aws bedrock-agent get-agent-alias \
  --agent-id YOUR_AGENT_ID \
  --agent-alias-id AIDACKQG5WD3S \
  --region us-east-1
```

### 2.2 Test Bedrock Model Access
```bash
# Check available models
aws bedrock list-foundation-models --region us-east-1 | jq '.modelSummaries | .[] | select(.modelId | contains("claude"))'

# Test Claude Sonnet invocation
aws bedrock-runtime invoke-model \
  --model-id anthropic.claude-3-5-sonnet-20241022-v2:0 \
  --body '{"messages":[{"role":"user","content":"What is Aspirin?"}],"max_tokens":100}' \
  --region us-east-1 | jq .
```

### 2.3 Test Agent Invocation
```bash
# Invoke agent for a test query
aws bedrock-agent-runtime invoke-agent \
  --agent-id YOUR_AGENT_ID \
  --agent-alias-id AIDACKQG5WD3S \
  --session-id test-session-1 \
  --input-text "Extract medicines from a prescription showing Aspirin 500mg twice daily" \
  --region us-east-1 | jq .

# For more complex responses, pipe through Python
aws bedrock-agent-runtime invoke-agent \
  --agent-id YOUR_AGENT_ID \
  --agent-alias-id AIDACKQG5WD3S \
  --session-id test-session-2 \
  --input-text "What are side effects of Lisinopril?" \
  --region us-east-1 | python -c "
import json, sys
data = json.load(sys.stdin)
for event in data.get('completion', []):
    if 'chunk' in event:
        chunk_bytes = event['chunk'].get('bytes', b'')
        if isinstance(chunk_bytes, bytes):
            print(chunk_bytes.decode('utf-8'), end='')
"
```

## Test 3: Knowledge Base

### 3.1 Check KB Status
```bash
# List knowledge bases
aws bedrock-agent list-knowledge-bases --region us-east-1

# Get KB details
aws bedrock-agent get-knowledge-base \
  --knowledge-base-id YOUR_KB_ID \
  --region us-east-1

# List data sources
aws bedrock-agent list-data-sources \
  --knowledge-base-id YOUR_KB_ID \
  --region us-east-1

# Get data source details
aws bedrock-agent get-data-source \
  --knowledge-base-id YOUR_KB_ID \
  --data-source-id YOUR_DATA_SOURCE_ID \
  --region us-east-1
```

### 3.2 Upload Documents to KB
```bash
# Create test documents
python scripts/ingest_knowledge_base.py

# Check S3 upload
aws s3 ls s3://careguide-kb-bucket/bedrock-kb/ --region us-east-1
```

### 3.3 Test KB Document Availability
```bash
# List documents indexed in KB
# (Method depends on KB backing storage - OpenSearch or Kendra)

# If using OpenSearch Serverless:
aws opensearchserverless batch-get-collection \
  --names careguide-kb-collection \
  --region us-east-1
```

## Test 4: DynamoDB Table

### 4.1 Create Test Item
```bash
# Put an item in DynamoDB
aws dynamodb put-item \
  --table-name prescription-results-dev \
  --item '{
    "prescriptionId": {"S": "test-001"},
    "timestamp": {"N": "1234567890"},
    "analysis": {
      "M": {
        "medicines": {"L": [{"S": "Aspirin"}]},
        "warnings": {"L": []}
      }
    },
    "status": {"S": "completed"}
  }' \
  --region us-east-1
```

### 4.2 Query Items
```bash
# Get specific item
aws dynamodb get-item \
  --table-name prescription-results-dev \
  --key '{"prescriptionId":{"S":"test-001"},"timestamp":{"N":"1234567890"}}' \
  --region us-east-1

# Query by partition key
aws dynamodb query \
  --table-name prescription-results-dev \
  --key-condition-expression "prescriptionId = :id" \
  --expression-attribute-values '{":id":{"S":"test-001"}}' \
  --region us-east-1

# Scan all items
aws dynamodb scan --table-name prescription-results-dev --region us-east-1 | jq .
```

## Test 5: Lambda Function

### 5.1 Test Lambda Directly
```bash
# Create test event
cat > test-event.json << 'EOF'
{
  "Records": [{
    "s3": {
      "bucket": {"name": "careguide-prescriptions"},
      "object": {"key": "test-prescription.jpg"}
    }
  }]
}
EOF

# Invoke Lambda function
aws lambda invoke \
  --function-name careguide-prescription-processor-dev \
  --payload file://test-event.json \
  response.json \
  --region us-east-1

# Check response
cat response.json | jq .
```

### 5.2 Tail Lambda Logs
```bash
# Real-time log tailing
aws logs tail /aws/lambda/careguide-prescription-processor-dev --follow --region us-east-1

# Get recent logs
aws logs tail /aws/lambda/careguide-prescription-processor-dev --max-items 20 --region us-east-1
```

### 5.3 Check Lambda Metrics
```bash
# Get Lambda invocation count
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Invocations \
  --dimensions Name=FunctionName,Value=careguide-prescription-processor-dev \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-12-31T23:59:59Z \
  --period 3600 \
  --statistics Sum \
  --region us-east-1

# Get Lambda errors
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name Errors \
  --dimensions Name=FunctionName,Value=careguide-prescription-processor-dev \
  --start-time 2024-01-01T00:00:00Z \
  --end-time 2024-12-31T23:59:59Z \
  --period 3600 \
  --statistics Sum \
  --region us-east-east
```

## Test 6: End-to-End Flow

### 6.1 Upload Prescription and Trigger Lambda
```bash
# Upload image to prescriptions bucket (should trigger Lambda)
aws s3 cp prescription.jpg s3://careguide-prescriptions/ --region us-east-1

# Wait a few seconds for processing
sleep 5

# Check results bucket
aws s3 ls s3://careguide-results/results/ --region us-east-1

# Download and view result
aws s3 cp s3://careguide-results/results/prescription-001.json . --region us-east-1
cat prescription-001.json | jq .

# Check DynamoDB for record
aws dynamodb query \
  --table-name prescription-results-dev \
  --key-condition-expression "prescriptionId = :id" \
  --expression-attribute-values '{":id":{"S":"prescription-001"}}' \
  --region us-east-1 | jq .
```

### 6.2 Backend API Test
```bash
# Start backend in one terminal
cd backend
python -m uvicorn app.main:app --reload

# In another terminal, test AWS provider
curl -X POST http://localhost:8000/upload-prescription \
  -F "file=@prescription.jpg" \
  -F "provider=aws" \
  -F "language=en" | jq .

# With verbose output
curl -v -X POST http://localhost:8000/upload-prescription \
  -F "file=@prescription.jpg" \
  -F "provider=aws" \
  -F "language=en"
```

## Test 7: Performance and Load

### 7.1 Lambda Performance
```bash
# Check Lambda duration
aws logs tail /aws/lambda/careguide-prescription-processor-dev \
  --filter-pattern "Duration" \
  --follow \
  --region us-east-1
```

### 7.2 Concurrent Invocations
```bash
# Test multiple uploads (will queue if Lambda hits concurrency limit)
for i in {1..5}; do
  aws s3 cp prescription.jpg s3://careguide-prescriptions/test-$i.jpg --region us-east-1
done

# Check function configuration
aws lambda get-function-concurrency \
  --function-name careguide-prescription-processor-dev \
  --region us-east-1
```

### 7.3 Cost Monitoring
```bash
# Get Lambda cost metrics
aws ce get-cost-and-usage \
  --time-period Start=2024-01-01,End=2024-12-31 \
  --granularity MONTHLY \
  --metrics "UnblendedCost" \
  --filter file://ce-filter.json \
  --group-by Type=SERVICE

# Create ce-filter.json
cat > ce-filter.json << 'EOF'
{
  "Dimensions": {
    "Key": "SERVICE",
    "Values": ["AWS Lambda"]
  }
}
EOF
```

## Troubleshooting Tests

### Issue: Lambda Cannot Access Bedrock Agent
```bash
# Check Lambda execution role permissions
aws iam get-role-policy \
  --role-name careguide-lambda-role-dev \
  --policy-name BedrockAccess \
  --region us-east-1 | jq .PolicyDocument

# Verify agent exists and is accessible
aws bedrock-agent list-agents --region us-east-1
```

### Issue: CloudWatch Logs Empty
```bash
# Check if log group exists
aws logs describe-log-groups \
  --log-group-name-prefix /aws/lambda \
  --region us-east-1 | jq '.logGroups[] | select(.logGroupName | contains("careguide"))'

# Create log group if missing
aws logs create-log-group \
  --log-group-name /aws/lambda/careguide-prescription-processor-dev \
  --region us-east-1
```

### Issue: Results Not Appearing in S3
```bash
# Check bucket policies
aws s3api get-bucket-policy \
  --bucket careguide-results \
  --region us-east-1 | jq .

# Verify Lambda can write to bucket
aws s3api head-bucket \
  --bucket careguide-results \
  --region us-east-1
```

### Issue: DynamoDB Throttling
```bash
# Check table capacity
aws dynamodb describe-table \
  --table-name prescription-results-dev \
  --region us-east-1 | jq '.Table | {BillingMode, StreamSpecification}'

# For on-demand mode, no throttling expected
# For provisioned mode, increase capacity
aws dynamodb update-table \
  --table-name prescription-results-dev \
  --provisioned-throughput ReadCapacityUnits=100,WriteCapacityUnits=100 \
  --region us-east-1
```

## Quick Test Checklist

- [ ] S3 buckets accessible (`aws s3 ls`)
- [ ] Bedrock models available (`aws bedrock list-foundation-models`)
- [ ] Agent created and healthy (`aws bedrock-agent get-agent`)
- [ ] Knowledge Base functional (`aws bedrock-agent get-knowledge-base`)
- [ ] Lambda function deployed (`aws lambda get-function`)
- [ ] DynamoDB table created (`aws dynamodb describe-table`)
- [ ] S3 event notification configured (`aws s3api get-bucket-notification-configuration`)
- [ ] Lambda can read from input bucket (test with direct invoke)
- [ ] Lambda can write to output bucket (check CloudWatch logs)
- [ ] End-to-end flow works (S3 upload → Lambda → results)

## Next: Production Deployment

Once all tests pass:

1. Set up CI/CD pipeline to auto-deploy Lambda updates
2. Enable X-Ray tracing for performance analysis
3. Set up CloudWatch alarms for errors and latency
4. Create backup strategy for DynamoDB
5. Implement encryption for S3 buckets at rest
6. Set up API Gateway for REST access to results
7. Consider multi-region deployment for HA
