# 🏥 CareGuide AI - AWS Bedrock Infrastructure Setup

Complete guide to deploy the CareGuide AI prescription digitization system on AWS with Bedrock.

## ⚡ Quick Start

**New to AWS?** Start here: [AWS_QUICKSTART.md](AWS_QUICKSTART.md)

**Experienced with AWS?** Run the interactive wizard:
```bash
cd scripts
python aws_setup_wizard.py
```

---

## 📖 Documentation

Choose your path:

### For Different User Types

| User Type | Start Here | Time |
|-----------|-----------|------|
| 🚀 **AWS Experts** | [AWS_QUICKSTART.md](AWS_QUICKSTART.md) | 5 min |
| 📚 **First-Time Users** | [AWS_SETUP_GUIDE.md](AWS_SETUP_GUIDE.md) | 30 min |
| 🧪 **Quality Assurance** | [AWS_TESTING_GUIDE.md](AWS_TESTING_GUIDE.md) | 1 hour |
| 🔧 **DevOps Engineers** | [AWS_INFRASTRUCTURE.md](AWS_INFRASTRUCTURE.md) | 2 hours |
| 📦 **Need Overview?** | [AWS_COMPLETE_PACKAGE.md](AWS_COMPLETE_PACKAGE.md) | 15 min |

---

## 🎯 What This Does

CareGuide AI analyzes prescription images and:
- ✅ **Extracts medicines** using AWS Bedrock Claude 3.5 Sonnet (vision)
- ✅ **Looks up medicine info** using Knowledge Base (RAG)
- ✅ **Provides guidance** in multiple languages
- ✅ **Identifies warnings** and drug interactions
- ✅ **Scales automatically** with Lambda & S3

### Architecture
```
Prescription Image → S3 → Lambda → Bedrock Agent → Results → S3 + DynamoDB
```

---

## 🚀 Fastest Setup (5 Minutes)

```bash
# 1. Prerequisites
aws configure
pip install boto3

# 2. Get account ID
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)

# 3. Enable Bedrock models
# Go to AWS Console → Bedrock → Model Access
# Request: Claude 3.5 Sonnet + Titan Embeddings

# 4. Run setup wizard
cd scripts
python aws_setup_wizard.py
# Wizard will create:
# - S3 buckets
# - IAM roles
# - Bedrock Agent & Knowledge Base
# - Lambda function
# - DynamoDB table
# - .env file

# 5. Test it
cd ../backend
python -m uvicorn app.main:app --reload
# curl -X POST http://localhost:8000/upload-prescription \
#   -F "file=@test.jpg" -F "provider=aws" -F "language=en"
```

---

## 📋 Full Setup Checklist

### Day 1: Foundation (30 minutes)
- [ ] Enable Bedrock models in AWS Console
- [ ] Get AWS account ID: `aws sts get-caller-identity`
- [ ] Run: `python scripts/aws_setup_wizard.py`
- [ ] Verify S3 buckets created: `aws s3 ls | grep careguide`

### Day 2: Testing (1 hour)
- [ ] Test local provider: `provider=local`
- [ ] Test AWS provider: `provider=aws`
- [ ] Upload prescription to trigger Lambda
- [ ] Check results in S3
- [ ] View Lambda logs

### Day 3: Production (1 hour)
- [ ] Review AWS_INFRASTRUCTURE.md
- [ ] Update `.env` with production values
- [ ] Deploy using CloudFormation
- [ ] Set up CloudWatch alarms
- [ ] Configure cost monitoring

---

## 🎬 Usage Examples

### Test Locally (No AWS needed)
```bash
curl -X POST http://localhost:8000/upload-prescription \
  -F "file=@prescription.jpg" \
  -F "provider=local" \
  -F "language=en"
```

### Test with AWS Bedrock
```bash
curl -X POST http://localhost:8000/upload-prescription \
  -F "file=@prescription.jpg" \
  -F "provider=aws" \
  -F "language=hi"  # Hindi guidance
```

### Trigger Lambda Directly
```bash
aws s3 cp prescription.jpg s3://careguide-prescriptions-$ACCOUNT_ID/
# Lambda automatically processes and saves results to:
# s3://careguide-results-$ACCOUNT_ID/results/
```

---

## 🏗️ What Gets Created

### AWS Resources
- **S3 Buckets** (3): Prescriptions, Knowledge Base, Results
- **Lambda Function**: Serverless prescription processor
- **DynamoDB Table**: Result storage and indexing
- **Bedrock Agent**: Multi-tool prescription analyzer
- **Knowledge Base**: Medicine data (RxNorm+OpenFDA)
- **IAM Roles**: Permissions for all services
- **CloudWatch Logs**: Monitoring and debugging

### Files Generated
- `.env` - Configuration with your AWS IDs
- `lambda_function.zip` - Deployable Lambda package
- `notification.json` - S3 event configuration
- CloudWatch Dashboard - Performance monitoring

---

## 📊 Architecture Details

```
┌─────────────────────────────────────────────────────┐
│                   User Uploads Image                 │
└────────────────────┬────────────────────────────────┘
                     ↓
        ┌────────────────────────────┐
        │    FastAPI Backend         │
        │  /upload-prescription      │
        └────────────┬───────────────┘
                     ↓
        ┌─────────────────────────────┐
        │  Route by Provider Type     │
        └──────┬──────────────┬───────┘
               ↓              ↓
        ┌─────────────┐  ┌───────────────────┐
        │  Local      │  │  AWS Bedrock      │
        ├─────────────┤  ├───────────────────┤
        │ Tesseract   │  │ Upload Image → S3 │
        │   OCR       │  │       ↓           │
        │     ↓       │  │ Claude 3.5 Sonnet │
        │  spaCy NER  │  │  (Vision Model)   │
        │     ↓       │  │       ↓           │
        │  Pattern    │  │ Bedrock KB (RAG)  │
        │  Matching   │  │       ↓           │
        └──────┬──────┘  │ Generate Guidance │
               │         │ (Multilingual)    │
               │         └─────────┬─────────┘
               │                   │
               └─────────┬─────────┘
                         ↓
        ┌─────────────────────────────┐
        │   Analysis Results          │
        │  - Medicines               │
        │  - Dosages                 │
        │  - Warnings                │
        │  - Interactions            │
        │  - Guidance (in language)  │
        └─────────────┬───────────────┘
                      ↓
        ┌──────────────────────────────┐
        │  Save Results               │
        ├──────────────────────────────┤
        │ S3 (JSON file storage)       │
        │ DynamoDB (quick lookup)      │
        └──────────────────────────────┘
```

---

## 🧪 How to Test

### Test 1: S3 Access
```bash
aws s3 ls s3://careguide-prescriptions-$ACCOUNT_ID/
```

### Test 2: Lambda Function
```bash
aws lambda list-functions --region us-east-1 | grep careguide
```

### Test 3: Full Workflow
```bash
# Upload triggers Lambda
aws s3 cp test.jpg s3://careguide-prescriptions-$ACCOUNT_ID/
sleep 5

# Check results
aws s3 ls s3://careguide-results-$ACCOUNT_ID/results/
```

### Test 4: View Logs
```bash
aws logs tail /aws/lambda/careguide-prescription-processor-dev --follow
```

---

## 💰 Costs

| Item | Quantity | Price | Total |
|------|----------|-------|-------|
| Bedrock API calls | 100/mo | $0.003 per call | $0.30 |
| S3 storage | 1 GB | $0.023 | $0.02 |
| Lambda | 100/mo | $0.20/million | $0.00 |
| DynamoDB | 100 writes | Free tier | $0.00 |
| **Total for 100 requests/month** | | | **~$1-5** |

Production (10,000/month): ~$200-500/month

---

## 🔐 Security Notes

Before going production:

1. **Enable S3 Encryption**: SSE-S3 or KMS
2. **Enable DynamoDB Encryption**: At-rest encryption
3. **Use IAM Roles**: Never hardcode AWS keys
4. **Enable CloudTrail**: Audit all AWS API calls
5. **Set Budget Alerts**: Monitor spending

---

## 📚 Documentation Files

| File | Purpose |
|------|---------|
| [AWS_QUICKSTART.md](AWS_QUICKSTART.md) | 5-minute setup for AWS pros |
| [AWS_SETUP_GUIDE.md](AWS_SETUP_GUIDE.md) | Step-by-step detailed guide |
| [AWS_TESTING_GUIDE.md](AWS_TESTING_GUIDE.md) | Comprehensive test procedures |
| [AWS_INFRASTRUCTURE.md](AWS_INFRASTRUCTURE.md) | Production deployment guide |
| [AWS_COMPLETE_PACKAGE.md](AWS_COMPLETE_PACKAGE.md) | Package overview & features |

---

## 🛠️ Scripts Available

| Script | Purpose | Time |
|--------|---------|------|
| `aws_setup_wizard.py` | Interactive setup (recommended) | 5 min |
| `setup_bedrock_agent.py` | Create Bedrock Agent & KB | 2 min |
| `ingest_knowledge_base.py` | Populate KB with medicine data | 1 min |
| `create_iam_roles.py` | Create IAM roles automatically | 1 min |

---

## ❓ Troubleshooting

### "No module named boto3"
```bash
pip install boto3
```

### "Access denied" on Bedrock
```bash
# Check IAM permissions
aws iam get-role-policy --role-name CareGuideAgentLambdaRole --policy-name LambdaPolicy
```

### Lambda timeout
```bash
# Increase to 180 seconds
aws lambda update-function-configuration \
  --function-name careguide-prescription-processor-dev \
  --timeout 180
```

### Results not appearing in S3
```bash
# Check Lambda logs
aws logs tail /aws/lambda/careguide-prescription-processor-dev --follow
```

---

## 🎓 Learning Path

1. **Understand the Architecture** (5 min)
   - Read this README

2. **Quick Setup** (5 min)
   - Run `aws_setup_wizard.py`

3. **Test Everything** (30 min)
   - Follow AWS_TESTING_GUIDE.md

4. **Learn AWS Services** (1 hour)
   - Study Bedrock, Lambda, S3 basics

5. **Production Deployment** (2 hours)
   - Follow AWS_INFRASTRUCTURE.md

6. **Optimize & Monitor** (ongoing)
   - Use CloudWatch dashboard
   - Monitor costs
   - Improve accuracy

---

## 📞 Need Help?

### For Setup Issues
1. Check **AWS_SETUP_GUIDE.md** Troubleshooting section
2. Review error messages in CloudWatch logs
3. Verify AWS credentials with: `aws sts get-caller-identity`

### For Testing Issues
1. Check **AWS_TESTING_GUIDE.md**
2. Verify Lambda function: `aws lambda get-function`
3. Check S3 buckets: `aws s3 ls`

### For AWS Help
- [AWS Bedrock Documentation](https://docs.aws.amazon.com/bedrock/)
- [AWS Lambda FAQs](https://aws.amazon.com/lambda/faqs/)
- [AWS Support](https://console.aws.amazon.com/support/)

---

## ✨ Features

**Local Analysis** (works without AWS):
- ✅ Tesseract OCR text extraction
- ✅ spaCy NER for medicine detection
- ✅ Pattern matching for dosages
- ✅ Basic medicine identification

**AWS Bedrock Analysis** (scalable, accurate):
- ✅ Claude 3.5 Sonnet vision analysis
- ✅ RAG knowledge base lookup
- ✅ Multilingual guidance generation
- ✅ Drug interaction warnings
- ✅ Automatic scaling with Lambda

**Data Management**:
- ✅ S3 image storage (with versioning)
- ✅ DynamoDB result indexing
- ✅ CloudWatch monitoring
- ✅ Cost tracking

---

## 🚀 Next Steps

**Ready to get started?**

1. **Choose your path**:
   - AWS Expert? → [AWS_QUICKSTART.md](AWS_QUICKSTART.md)
   - First time? → [AWS_SETUP_GUIDE.md](AWS_SETUP_GUIDE.md)

2. **Run setup**:
   ```bash
   python scripts/aws_setup_wizard.py
   ```

3. **Test**:
   ```bash
   curl -X POST http://localhost:8000/upload-prescription \
     -F "file=@test.jpg" -F "provider=aws" -F "language=en"
   ```

4. **Deploy**:
   ```bash
   python -m uvicorn app.main:app --prod
   ```

---

## 📝 Requirements

### Before Starting
- ✅ AWS account (with billing enabled)
- ✅ Bedrock access enabled
- ✅ AWS CLI installed (`aws --version`)
- ✅ Python 3.11+ (`python --version`)
- ✅ boto3 installed (`pip install boto3`)

### Check Prerequisites
```bash
# Verify everything
aws sts get-caller-identity  # ✓ AWS CLI works
python --version              # ✓ Python 3.11+
pip list | grep boto3         # ✓ boto3 installed
```

---

## 📊 Project Stats

- 📄 **4 comprehensive guides**: 50+ pages of documentation
- 🛠️ **4 automation scripts**: Ready to run
- 🏗️ **Full CloudFormation template**: Production-ready
- 📦 **Complete AWS integration**: Bedrock + Lambda + S3 + DynamoDB
- ✅ **Tested & verified**: Working examples included

---

## 🎉 Success Metrics

After setup, you should be able to:
- ✅ Upload prescription images via API
- ✅ Get medicine analysis in real-time
- ✅ Access results from S3 and DynamoDB
- ✅ View CloudWatch metrics and logs
- ✅ Scale to thousands of prescriptions/month

---

## 📄 License & Attribution

**Project**: CareGuide AI - Prescription Digitization System  
**Stack**: AWS Bedrock, Lambda, S3, DynamoDB, FastAPI  
**Status**: Production Ready  

---

## 🙏 Credits

Built for **AI for Bharat** initiative with:
- AWS Cloud Services
- Claude 3.5 Sonnet (Anthropic)
- RxNorm & OpenFDA datasets
- FastAPI framework
- Python 3.11+

---

**Last Updated**: 2024  
**Version**: 1.0  
**Status**: ✅ Ready for Deployment

---

## 🎯 Quick Links

| What You Need | Where to Find It |
|---------------|------------------|
| **5-min setup** | [AWS_QUICKSTART.md](AWS_QUICKSTART.md) |
| **Detailed guide** | [AWS_SETUP_GUIDE.md](AWS_SETUP_GUIDE.md) |
| **Testing guide** | [AWS_TESTING_GUIDE.md](AWS_TESTING_GUIDE.md) |
| **Production deploy** | [AWS_INFRASTRUCTURE.md](AWS_INFRASTRUCTURE.md) |
| **Package overview** | [AWS_COMPLETE_PACKAGE.md](AWS_COMPLETE_PACKAGE.md) |
| **Setup wizard** | `python scripts/aws_setup_wizard.py` |

---

**🚀 Ready? Start here:**
```bash
cd scripts && python aws_setup_wizard.py
```
