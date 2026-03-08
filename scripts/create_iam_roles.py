#!/usr/bin/env python3
"""
Create IAM roles required for Bedrock Agent, Knowledge Base, and Lambda.
Generates JSON policies for manual attachment or CloudFormation integration.
"""

import json
import boto3

iam = boto3.client('iam')


# Policy for Bedrock Agent execution
BEDROCK_AGENT_POLICY = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelEndpoint"
            ],
            "Resource": "arn:aws:bedrock:*:*:agent/*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:GetAgentAction",
                "bedrock:Invoke*"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject"
            ],
            "Resource": "arn:aws:s3:::careguide-*/*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "kendra:Query",
                "kendra:GetQuerySuggestions"
            ],
            "Resource": "*"
        }
    ]
}

# Trust policy for Bedrock service
BEDROCK_AGENT_TRUST_POLICY = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "bedrock.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}

# Policy for Knowledge Base
BEDROCK_KB_POLICY = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::careguide-*/*",
                "arn:aws:s3:::careguide-*"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "opensearch:DescribeSecurityConfiguration",
                "opensearch:DescribeNodeTypes",
                "opensearch:DescribeDomain",
                "opensearch:DescribeDomainConfig"
            ],
            "Resource": "*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel"
            ],
            "Resource": "arn:aws:bedrock:*:*:foundation-model/*"
        }
    ]
}

# Policy for Lambda function
LAMBDA_POLICY = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject"
            ],
            "Resource": "arn:aws:s3:::careguide-*/*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeAgent",
                "bedrock:InvokeModel"
            ],
            "Resource": "*"
        }
    ]
}

LAMBDA_TRUST_POLICY = {
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}


def create_iam_role(role_name: str, assume_role_policy: dict, inline_policies: dict) -> str:
    """Create an IAM role with assumed trust policy and inline policies."""
    try:
        # Create role
        response = iam.create_role(
            RoleName=role_name,
            AssumeRolePolicyDocument=json.dumps(assume_role_policy),
            Description=f"Role for {role_name}"
        )
        role_arn = response['Role']['Arn']
        print(f"✅ Created role: {role_name}")
        print(f"   ARN: {role_arn}\n")
        
        # Attach inline policies
        for policy_name, policy_document in inline_policies.items():
            iam.put_role_policy(
                RoleName=role_name,
                PolicyName=policy_name,
                PolicyDocument=json.dumps(policy_document)
            )
            print(f"   ✅ Attached policy: {policy_name}")
        
        return role_arn
    except iam.exceptions.EntityAlreadyExistsException:
        print(f"⚠️  Role {role_name} already exists")
        return iam.get_role(RoleName=role_name)['Role']['Arn']
    except Exception as e:
        print(f"❌ Error creating role {role_name}: {e}")
        raise


def generate_policy_files():
    """Generate policy JSON files for manual review and attachment."""
    policies = {
        "bedrock_agent_policy.json": BEDROCK_AGENT_POLICY,
        "bedrock_kb_policy.json": BEDROCK_KB_POLICY,
        "lambda_policy.json": LAMBDA_POLICY
    }
    
    for filename, policy in policies.items():
        filepath = f"./policies/{filename}"
        with open(filepath, 'w') as f:
            json.dump(policy, f, indent=2)
        print(f"📄 Generated: {filepath}")


if __name__ == "__main__":
    import sys
    
    print("🔐 AWS IAM Role Creation for Bedrock & Lambda\n")
    
    if len(sys.argv) > 1 and sys.argv[1] == "--generate-policies":
        print("📋 Generating policy files for manual review...\n")
        generate_policy_files()
        print("\n✅ Policy files generated. Review and attach manually via AWS Console.")
    else:
        print("⚠️  This script creates IAM roles. Ensure you have appropriate permissions.\n")
        
        # Create roles
        print("Creating IAM roles...\n")
        
        bedrock_agent_role = create_iam_role(
            "BedrockAgentExecutionRole",
            BEDROCK_AGENT_TRUST_POLICY,
            {"BedrockAgentPolicy": BEDROCK_AGENT_POLICY}
        )
        
        bedrock_kb_role = create_iam_role(
            "BedrockKBExecutionRole",
            BEDROCK_AGENT_TRUST_POLICY,
            {"BedrockKBPolicy": BEDROCK_KB_POLICY}
        )
        
        lambda_role = create_iam_role(
            "CareGuideAgentLambdaRole",
            LAMBDA_TRUST_POLICY,
            {"LambdaPolicy": LAMBDA_POLICY}
        )
        
        print("\n✅ IAM roles created successfully!")
        print(f"\n📝 Save these ARNs for configuration:")
        print(f"   Bedrock Agent Role: {bedrock_agent_role}")
        print(f"   Bedrock KB Role: {bedrock_kb_role}")
        print(f"   Lambda Role: {lambda_role}")
