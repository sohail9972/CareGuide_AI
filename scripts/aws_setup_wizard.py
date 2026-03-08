#!/usr/bin/env python3
"""
Interactive AWS setup wizard for CareGuide AI.
Guides users through the entire Bedrock infrastructure setup process.
"""

import os
import sys
import json
import subprocess
from pathlib import Path


class Colors:
    HEADER = '\033[95m'
    BLUE = '\033[94m'
    CYAN = '\033[96m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    ENDC = '\033[0m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'


def print_header(text):
    print(f"\n{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{text:^60}{Colors.ENDC}")
    print(f"{Colors.HEADER}{Colors.BOLD}{'='*60}{Colors.ENDC}\n")


def print_section(text):
    print(f"\n{Colors.CYAN}{Colors.BOLD}>>> {text}{Colors.ENDC}")


def print_success(text):
    print(f"{Colors.GREEN}✅  {text}{Colors.ENDC}")


def print_warning(text):
    print(f"{Colors.YELLOW}⚠️  {text}{Colors.ENDC}")


def print_error(text):
    print(f"{Colors.RED}❌  {text}{Colors.ENDC}")


def run_command(cmd, description=""):
    """Run a shell command and return success status."""
    try:
        if description:
            print(f"  Running: {description}")
        result = subprocess.run(cmd, shell=True, capture_output=True, text=True)
        if result.returncode == 0:
            return True, result.stdout
        else:
            return False, result.stderr
    except Exception as e:
        return False, str(e)


def get_aws_account_id():
    """Get AWS account ID from AWS CLI."""
    print_section("Getting AWS Account ID")
    success, output = run_command(
        "aws sts get-caller-identity --query Account --output text",
        "aws sts get-caller-identity"
    )
    
    if success:
        account_id = output.strip()
        print_success(f"AWS Account ID: {account_id}")
        return account_id
    else:
        print_error("Could not get AWS Account ID. Ensure AWS CLI is configured.")
        print_error(output)
        return None


def check_prerequisites():
    """Check if all prerequisites are installed."""
    print_header(" CHECKING PREREQUISITES")
    
    prerequisites = {
        'aws --version': 'AWS CLI',
        'python --version': 'Python 3.11+',
        'boto3': 'boto3 Python package'
    }
    
    all_good = True
    for cmd, name in prerequisites.items():
        if cmd == 'boto3':
            try:
                import boto3
                print_success(f"{name}: {boto3.__version__}")
            except ImportError:
                print_error(f"{name}: NOT INSTALLED")
                print_warning(f"Run: pip install boto3")
                all_good = False
        else:
            success, output = run_command(cmd)
            if success:
                version = output.strip().split('\n')[0]
                print_success(f"{name}: {version}")
            else:
                print_error(f"{name}: NOT FOUND")
                all_good = False
    
    return all_good


def setup_s3_buckets(account_id):
    """Create S3 buckets."""
    print_header(" CREATING S3 BUCKETS")
    
    buckets = [
        ('careguide-prescriptions', 'For prescription images'),
        ('careguide-kb-bucket', 'For knowledge base documents'),
        ('careguide-results', 'For analysis results')
    ]
    
    for bucket_name, description in buckets:
        full_bucket = f"{bucket_name}-{account_id}"
        print_section(f"Creating: {full_bucket}")
        print(f"  Purpose: {description}")
        
        success, output = run_command(
            f"aws s3 mb s3://{full_bucket} --region us-east-1",
            f"Creating S3 bucket {full_bucket}"
        )
        
        if success:
            print_success(f"Bucket created: {full_bucket}")
        else:
            if "already exists" in output:
                print_warning(f"Bucket already exists: {full_bucket}")
            else:
                print_error(f"Failed to create bucket: {full_bucket}")
                return False
    
    return True


def enable_bedrock_models():
    """Prompt user to enable Bedrock models."""
    print_header(" ENABLING BEDROCK MODELS")
    
    print("Bedrock models must be enabled in your AWS account.")
    print("Please follow these steps:")
    print()
    print("  1. Go to AWS Console → Bedrock → Model Catalog")
    print("  2. Click 'Manage Access' → 'Request Model Access'")
    print("  3. Select and enable:")
    print("     - Claude 3.5 Sonnet")
    print("     - Titan Embeddings G1")
    print()
    
    input_val = input(f"{Colors.BOLD}Have you enabled Bedrock models? (yes/no): {Colors.ENDC}").strip().lower()
    return input_val == 'yes'


def create_iam_roles():
    """Create IAM roles for Bedrock and Lambda."""
    print_header(" CREATING IAM ROLES")
    
    print_section("Option 1: Automatic Role Creation (Recommended)")
    print("Run: python scripts/create_iam_roles.py")
    print()
    
    response = input(f"{Colors.BOLD}Create IAM roles now? (yes/no): {Colors.ENDC}").strip().lower()
    
    if response == 'yes':
        success, output = run_command(
            "python scripts/create_iam_roles.py",
            "Creating IAM roles"
        )
        
        if success:
            print_success("IAM roles created successfully")
            print(output)
            return True
        else:
            print_error("Failed to create IAM roles")
            print(output)
            return False
    else:
        print_warning("Skipping automatic role creation")
        print("You can create roles manually in the AWS Console later")
        return True


def setup_opensearch():
    """Setup OpenSearch for Knowledge Base."""
    print_header(" SETTING UP OPENSEARCH")
    
    print("OpenSearch is required for Knowledge Base vector storage.")
    print()
    print("Option 1: AWS OpenSearch Serverless (Recommended - no provisioning)")
    print("Option 2: Self-managed OpenSearch (requires configuration)")
    print()
    
    response = input(f"{Colors.BOLD}Use OpenSearch Serverless? (yes/no): {Colors.ENDC}").strip().lower()
    
    if response == 'yes':
        print_section("Creating OpenSearch Serverless Collection")
        success, output = run_command(
            "aws opensearchserverless create-collection --name careguide-kb-collection --type SEARCH --region us-east-1",
            "Creating OpenSearch Serverless collection"
        )
        
        if success:
            print_success("OpenSearch collection created")
            collection_info = json.loads(output)
            return collection_info.get('createCollectionDetail', {}).get('arn')
        else:
            if "already exists" in output:
                print_warning("Collection already exists")
                return None
            else:
                print_error("Failed to create OpenSearch collection")
                return None
    else:
        print_warning("Manual OpenSearch setup required")
        return None


def create_knowledge_base():
    """Create Bedrock Knowledge Base."""
    print_header(" CREATING KNOWLEDGE BASE")
    
    print("Creating Knowledge Base for medicine data...")
    
    print_section("Running: scripts/setup_bedrock_agent.py")
    print("This will create:")
    print("  - Bedrock Knowledge Base")
    print("  - Bedrock Agent with vision and RAG capabilities")
    print()
    
    response = input(f"{Colors.BOLD}Create Knowledge Base and Agent? (yes/no): {Colors.ENDC}").strip().lower()
    
    if response == 'yes':
        print_warning("⚠️  Update YOUR_ACCOUNT_ID in scripts/setup_bedrock_agent.py first!")
        response2 = input(f"{Colors.BOLD}Have you updated the script? (yes/no): {Colors.ENDC}").strip().lower()
        
        if response2 == 'yes':
            success, output = run_command(
                "python scripts/setup_bedrock_agent.py",
                "Creating Bedrock Agent and KB"
            )
            
            if success:
                print_success("Bedrock infrastructure created")
                print(output)
                
                # Extract IDs from output
                kb_id = input(f"{Colors.BOLD}Enter Knowledge Base ID: {Colors.ENDC}").strip()
                agent_id = input(f"{Colors.BOLD}Enter Agent ID: {Colors.ENDC}").strip()
                
                return kb_id, agent_id
        else:
            print_warning("Please update the script and try again")
    
    return None, None


def ingest_knowledge_base(kb_id):
    """Populate Knowledge Base with medicine data."""
    print_header(" INGESTING KNOWLEDGE BASE")
    
    if not kb_id:
        print_warning("Skipping KB ingestion (no KB ID provided)")
        return False
    
    print_section("Ingesting Sample Medicine Data")
    
    success, output = run_command(
        f"python scripts/ingest_knowledge_base.py",
        "Ingesting medicine data"
    )
    
    if success:
        print_success("Knowledge Base ingestion complete")
        print(output)
        return True
    else:
        print_error("Failed to ingest Knowledge Base")
        print(output)
        return False


def setup_environment():
    """Create .env file for backend."""
    print_header(" SETTING UP ENVIRONMENT")
    
    account_id = input(f"{Colors.BOLD}Enter AWS Account ID: {Colors.ENDC}").strip()
    kb_id = input(f"{Colors.BOLD}Enter Knowledge Base ID: {Colors.ENDC}").strip()
    agent_id = input(f"{Colors.BOLD}Enter Agent ID: {Colors.ENDC}").strip()
    
    env_content = f"""# AWS Configuration
AWS_REGION=us-east-1
AWS_ACCOUNT_ID={account_id}

# Bedrock Configuration
BEDROCK_AGENT_ID={agent_id}
BEDROCK_KB_ID={kb_id}

# S3 Buckets
S3_BUCKET_PRESCRIPTIONS=careguide-prescriptions-{account_id}
S3_BUCKET_DOCUMENTS=careguide-kb-bucket-{account_id}
S3_BUCKET_RESULTS=careguide-results-{account_id}

# Lambda
LAMBDA_FUNCTION_NAME=careguide-prescription-processor-dev

# DynamoDB
DYNAMODB_TABLE=prescription-results-dev
"""
    
    env_file = Path('backend/.env')
    env_file.write_text(env_content)
    print_success(f"Environment file created: {env_file}")
    return True


def test_setup():
    """Test the AWS setup."""
    print_header(" TESTING SETUP")
    
    print_section("Running basic connectivity tests")
    
    # Test 1: S3 Access
    print_section("Test 1: S3 Bucket Access")
    success, output = run_command(
        "aws s3 ls --region us-east-1 | head -5",
        "Listing S3 buckets"
    )
    if success:
        print_success("✓ S3 accessible")
    else:
        print_error("✗ S3 access failed")
    
    # Test 2: Bedrock Models
    print_section("Test 2: Bedrock Model Availability")
    success, output = run_command(
        "aws bedrock list-foundation-models --region us-east-1 | grep claude",
        "Checking Claude models"
    )
    if success:
        print_success("✓ Bedrock models available")
    else:
        print_warning("⚠️  Bedrock models not available (may need request approval)")
    
    # Test 3: Lambda Function
    print_section("Test 3: Lambda Function")
    success, output = run_command(
        "aws lambda list-functions --region us-east-1 | grep careguide",
        "Checking Lambda functions"
    )
    if success:
        print_success("✓ Lambda function found")
    else:
        print_warning("⚠️  Lambda function not deployed yet")


def show_next_steps(kb_id, agent_id, account_id):
    """Show next steps for the user."""
    print_header(" NEXT STEPS")
    
    print(f"✅ Basic infrastructure setup complete!\n")
    
    print(f"Your Configuration:")
    print(f"  Account ID: {account_id}")
    print(f"  KB ID: {kb_id}")
    print(f"  Agent ID: {agent_id}")
    print()
    
    print("Next Steps:")
    print()
    print("1. Deploy Lambda Function")
    print("   $ cd backend")
    print("   $ pip install -r requirements.txt -t lambda-deployment/")
    print("   $ cp aws_lambda_handler.py lambda-deployment/")
    print("   $ cd lambda-deployment && zip -r ../lambda_function.zip . && cd ..")
    print()
    print("2. Test the Backend API")
    print("   $ python -m uvicorn app.main:app --reload")
    print("   $ # In another terminal:")
    print("   $ curl -X POST http://localhost:8000/upload-prescription \\")
    print("       -F 'file=@test-image.jpg' \\")
    print("       -F 'provider=aws' \\")
    print("       -F 'language=en'")
    print()
    print("3. Test S3 → Lambda → Analysis Flow")
    print(f"   $ aws s3 cp test.jpg s3://careguide-prescriptions-{account_id}/")
    print("   $ # Check CloudWatch logs")
    print(f"   $ aws logs tail /aws/lambda/careguide-prescription-processor-dev --follow")
    print()
    print("4. Review Documentation")
    print("   - AWS_SETUP_GUIDE.md - Detailed setup instructions")
    print("   - AWS_TESTING_GUIDE.md - Comprehensive testing guide")
    print("   - AWS_DEPLOYMENT.md - Production deployment guide")
    print()


def main():
    """Run the interactive setup wizard."""
    print_header(" CAREGUIDE AI - AWS SETUP WIZARD")
    
    print("This wizard will guide you through setting up AWS Bedrock infrastructure")
    print("for the CareGuide AI prescription processing system.")
    print()
    
    # Step 1: Check prerequisites
    if not check_prerequisites():
        print_error("\n❌ Some prerequisites are missing. Please install them and try again.")
        sys.exit(1)
    
    # Step 2: Get AWS account ID
    account_id = get_aws_account_id()
    if not account_id:
        sys.exit(1)
    
    # Step 3: Setup S3 Buckets
    if not setup_s3_buckets(account_id):
        print_warning("S3 setup incomplete. Continuing anyway...")
    
    # Step 4: Enable Bedrock models
    if not enable_bedrock_models():
        print_warning("Bedrock models not enabled. Please enable in AWS Console and continue.")
    
    # Step 5: Create IAM roles
    if not create_iam_roles():
        print_warning("IAM role setup failed. Please try manual setup.")
    
    # Step 6: Setup OpenSearch
    setup_opensearch()
    
    # Step 7: Create Knowledge Base and Agent
    kb_id, agent_id = create_knowledge_base()
    
    # Step 8: Ingest Knowledge Base
    if kb_id:
        ingest_knowledge_base(kb_id)
    
    # Step 9: Setup Environment
    if kb_id and agent_id:
        setup_environment()
    
    # Step 10: Test setup
    test_setup()
    
    # Step 11: Show next steps
    if kb_id and agent_id:
        show_next_steps(kb_id, agent_id, account_id)
    else:
        print_warning("⚠️  Setup incomplete. Please review the AWS_SETUP_GUIDE.md for manual configuration.")
    
    print_header(" SETUP WIZARD COMPLETE")
    print("For detailed information, see:")
    print("  - AWS_SETUP_GUIDE.md")
    print("  - AWS_TESTING_GUIDE.md")
    print()


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print(f"\n{Colors.YELLOW}Setup wizard cancelled by user{Colors.ENDC}")
        sys.exit(0)
    except Exception as e:
        print(f"\n{Colors.RED}Unexpected error: {e}{Colors.ENDC}")
        sys.exit(1)
