#!/usr/bin/env python3
"""
Script to create a Bedrock Agent for prescription analysis.
This agent chains: Vision (text extraction) → RAG (knowledge lookup) → Translation
"""

import json
import boto3
import time
from typing import Dict, Any

bedrock = boto3.client('bedrock', region_name='us-east-1')
bedrock_agents = boto3.client('bedrock-agents', region_name='us-east-1')


def create_agent_definition() -> Dict[str, Any]:
    """Define the agent specification for prescription analysis."""
    return {
        "name": "PrescriptionAnalyzer",
        "description": "Analyzes prescription images to extract medicines and provide medical guidance",
        "foundationModel": "anthropic.claude-3-5-sonnet-20241022",
        "agentResourceRoleArn": "arn:aws:iam::YOUR_ACCOUNT_ID:role/BedrockAgentRole",
        "toolGroups": [
            {
                "toolGroupName": "VisionTools",
                "description": "Tools for analyzing prescription images",
                "tools": [
                    {
                        "toolName": "AnalyzePrescriptionImage",
                        "description": "Extracts text and medicines from a prescription image",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "imageUrl": {
                                    "type": "string",
                                    "description": "S3 URL of the prescription image"
                                }
                            },
                            "required": ["imageUrl"]
                        }
                    }
                ]
            },
            {
                "toolGroupName": "KnowledgeBaseTools",
                "description": "Tools for retrieving medical knowledge",
                "tools": [
                    {
                        "toolName": "LookupMedicineInfo",
                        "description": "Retrieves detailed info about a medicine from the knowledge base",
                        "inputSchema": {
                            "type": "object",
                            "properties": {
                                "medicineName": {
                                    "type": "string",
                                    "description": "Name of the medicine to look up"
                                }
                            },
                            "required": ["medicineName"]
                        }
                    }
                ]
            }
        ],
        "instructions": """You are a medical prescription analyzer. Your task:
1. Receive a prescription image URL
2. Use AnalyzePrescriptionImage to extract medicines, dosages, and duration
3. For each medicine found, use LookupMedicineInfo to get verified medical data (indications, side effects, precautions)
4. Compile a comprehensive guidance document
5. Return structured JSON with medicines, dosages, verified guidance, and any warnings

Always prioritize accuracy and use verified medical sources. If uncertain, flag as requiring physician review."""
    }


def create_knowledge_base_definition() -> Dict[str, Any]:
    """Define the Knowledge Base for storing medicine information."""
    return {
        "name": "MedicineDatabase",
        "description": "Knowledge base containing medicine information from RxNorm and OpenFDA",
        "type": "VECTOR",  # Vector embeddings for semantic search
        "embeddingModelArn": "arn:aws:bedrock:us-east-1::foundation-model/amazon.titan-embed-text-v1"
    }


def create_agent(agent_def: Dict[str, Any]) -> str:
    """Create a Bedrock Agent using the agent definition."""
    try:
        response = bedrock_agents.create_agent(
            agentName=agent_def["name"],
            agentDescription=agent_def["description"],
            foundationModel=agent_def["foundationModel"],
            agentResourceRoleArn=agent_def["agentResourceRoleArn"],
            instructions=agent_def["instructions"]
        )
        agent_id = response['agent']['agentId']
        print(f"✅ Agent created: {agent_id}")
        return agent_id
    except Exception as e:
        print(f"❌ Error creating agent: {e}")
        raise


def create_knowledge_base(kb_def: Dict[str, Any]) -> str:
    """Create a Bedrock Knowledge Base."""
    try:
        response = bedrock_agents.create_knowledge_base(
            name=kb_def["name"],
            description=kb_def["description"],
            knowledgeBaseConfiguration={
                "type": kb_def["type"],
                "vectorKnowledgeBaseConfiguration": {
                    "embeddingModel": {
                        "provider": "AMAZON",
                        "modelId": kb_def["embeddingModelArn"].split("/")[-1]
                    }
                }
            },
            storageConfiguration={
                "type": "OPENSEARCH",
                "opensearchServerlessConfiguration": {
                    "collectionArn": "arn:aws:aoss:us-east-1:YOUR_ACCOUNT_ID:collection/careguide-kb"
                }
            },
            roleArn="arn:aws:iam::YOUR_ACCOUNT_ID:role/BedrockKBRole"
        )
        kb_id = response['knowledgeBase']['knowledgeBaseId']
        print(f"✅ Knowledge Base created: {kb_id}")
        return kb_id
    except Exception as e:
        print(f"❌ Error creating knowledge base: {e}")
        raise


def associate_agent_with_kb(agent_id: str, kb_id: str) -> None:
    """Associate the Knowledge Base with the Agent for RAG lookups."""
    try:
        bedrock_agents.create_agent_action_group(
            agentId=agent_id,
            agentVersion="DRAFT",
            actionGroupName="KnowledgeBaseLookup",
            description="Retrieve medicine information from the knowledge base",
            actionGroupExecutor={
                "type": "KNOWLEDGE_BASE",
                "knowledgeBaseId": kb_id
            }
        )
        print(f"✅ Agent {agent_id} associated with KB {kb_id}")
    except Exception as e:
        print(f"❌ Error associating KB with agent: {e}")
        raise


def prepare_agent(agent_id: str) -> str:
    """Prepare (compile) the agent for use."""
    try:
        response = bedrock_agents.prepare_agent(
            agentId=agent_id
        )
        agent_version = response['agentVersion']
        print(f"✅ Agent prepared: version {agent_version}")
        return agent_version
    except Exception as e:
        print(f"❌ Error preparing agent: {e}")
        raise


if __name__ == "__main__":
    print("🚀 Starting Bedrock Agent & Knowledge Base Setup...\n")
    
    # Step 1: Create Knowledge Base
    print("📚 Creating Knowledge Base...")
    kb_def = create_knowledge_base_definition()
    # kb_id = create_knowledge_base(kb_def)
    # For now, use a placeholder since KB creation requires OpenSearch setup
    kb_id = "PLACEHOLDER_KB_ID"
    print(f"Knowledge Base ID: {kb_id}\n")
    
    # Step 2: Create Agent
    print("🤖 Creating Agent...")
    agent_def = create_agent_definition()
    # Substitute YOUR_ACCOUNT_ID before running
    agent_id = None  # create_agent(agent_def)
    print(f"⚠️  Agent creation requires valid AWS account ID. Update the script and run manually.\n")
    
    # Step 3: Associate agent with KB
    # if agent_id and kb_id != "PLACEHOLDER_KB_ID":
    #     print("🔗 Associating Agent with Knowledge Base...")
    #     associate_agent_with_kb(agent_id, kb_id)
    
    # Step 4: Prepare agent
    # if agent_id:
    #     print("⚙️  Preparing Agent...")
    #     agent_version = prepare_agent(agent_id)
    
    print("\n✅ To complete setup:")
    print("1. Update YOUR_ACCOUNT_ID in this script")
    print("2. Uncomment the function calls")
    print("3. Run: python scripts/setup_bedrock_agent.py")
    print("\n📖 See BEDROCK_SETUP.md for detailed instructions")
