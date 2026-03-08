"""
AWS Lambda handler for serverless prescription processing.
Triggered by S3 events when prescription images are uploaded.
Invokes Bedrock Agent for medicine extraction and guidance generation.
"""

import json
import boto3
import os
from datetime import datetime
from typing import Dict, Any

s3_client = boto3.client('s3')
bedrock_agent_runtime = boto3.client('bedrock-agent-runtime')
dynamodb = boto3.resource('dynamodb')

# Environment variables
BEDROCK_AGENT_ID = os.getenv('BEDROCK_AGENT_ID', 'PLACEHOLDER')
BEDROCK_AGENT_ALIAS_ID = os.getenv('BEDROCK_AGENT_ALIAS_ID', 'AIDACKQG5WD3S')
OUTPUT_BUCKET = os.getenv('OUTPUT_BUCKET', 'careguide-results')
RESULTS_TABLE = os.getenv('RESULTS_TABLE', 'prescription-results')
AWS_REGION = os.getenv('AWS_REGION', 'us-east-1')


def get_s3_object(bucket: str, key: str) -> bytes:
    """Download object from S3."""
    try:
        response = s3_client.get_object(Bucket=bucket, Key=key)
        return response['Body'].read()
    except Exception as e:
        print(f"❌ Error downloading from S3: {str(e)}")
        raise


def invoke_bedrock_agent(prompt: str, session_id: str) -> Dict[str, Any]:
    """
    Invoke Bedrock Agent for prescription analysis.
    
    Args:
        prompt: User prompt with medicine extraction request
        session_id: Session ID for agent invocation
        
    Returns:
        Agent response with extracted medicines and guidance
    """
    try:
        response = bedrock_agent_runtime.invoke_agent(
            agentId=BEDROCK_AGENT_ID,
            agentAliasId=BEDROCK_AGENT_ALIAS_ID,
            sessionId=session_id,
            inputText=prompt
        )
        
        # Collect full response from event stream
        result_text = ""
        for event in response.get('completion', []):
            if 'chunk' in event:
                chunk_data = event['chunk'].get('bytes', b'')
                if isinstance(chunk_data, bytes):
                    result_text += chunk_data.decode('utf-8')
                else:
                    result_text += str(chunk_data)
        
        return {
            'success': True,
            'response': result_text,
            'sessionId': session_id
        }
    except Exception as e:
        print(f"❌ Bedrock Agent error: {str(e)}")
        return {
            'success': False,
            'error': str(e),
            'sessionId': session_id
        }


def save_results_to_s3(results: Dict[str, Any], s3_key: str) -> str:
    """Save analysis results to S3."""
    try:
        s3_client.put_object(
            Bucket=OUTPUT_BUCKET,
            Key=s3_key,
            Body=json.dumps(results, indent=2),
            ContentType='application/json'
        )
        return f"s3://{OUTPUT_BUCKET}/{s3_key}"
    except Exception as e:
        print(f"❌ Error saving to S3: {str(e)}")
        return None


def save_results_to_dynamodb(results: Dict[str, Any]) -> bool:
    """Save results to DynamoDB for quick lookup."""
    try:
        table = dynamodb.Table(RESULTS_TABLE)
        table.put_item(Item={
            'prescriptionId': results.get('prescriptionId'),
            'timestamp': int(datetime.now().timestamp()),
            'analysis': results,
            'status': 'completed'
        })
        return True
    except Exception as e:
        print(f"⚠️  Warning: Could not save to DynamoDB: {str(e)}")
        return False


def lambda_handler(event: Dict[str, Any], context: Any) -> Dict[str, Any]:
    """
    Lambda handler for S3-triggered prescription processing.
    
    Args:
        event: S3 ObjectCreated event
        context: Lambda context
        
    Returns:
        Response with analysis results
    """
    print(f"📥 Event received: {json.dumps(event)}")
    
    try:
        # Extract S3 details from event
        if 'Records' not in event or len(event['Records']) == 0:
            return {
                'statusCode': 400,
                'body': json.dumps({'error': 'No Records in event'})
            }
        
        record = event['Records'][0]
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']
        
        print(f"🔍 Processing: s3://{bucket}/{key}")
        
        # Download image from S3
        image_data = get_s3_object(bucket, key)
        print(f"✅ Downloaded {len(image_data)} bytes from S3")
        
        # Prepare analysis prompt for Bedrock Agent
        session_id = f"{key.split('/')[-1]}-{int(datetime.now().timestamp())}"
        prompt = (
            f"Analyze the prescription image at s3://{bucket}/{key}. "
            "Extract all medicines, dosages, frequencies, and special instructions. "
            "Also provide safety warnings and potential drug interactions. "
            'Format as JSON with fields: medicines (list), warnings (list), interactions (list).'
        )
        
        # Invoke Bedrock Agent
        print("🤖 Invoking Bedrock Agent...")
        agent_response = invoke_bedrock_agent(prompt, session_id)
        
        if not agent_response['success']:
            print(f"❌ Agent failed: {agent_response.get('error')}")
            return {
                'statusCode': 500,
                'body': json.dumps({
                    'error': 'Bedrock Agent failed',
                    'details': agent_response.get('error')
                })
            }
        
        # Parse agent response
        try:
            analysis = json.loads(agent_response.get('response', '{}'))
        except json.JSONDecodeError:
            # If response is not JSON, wrap it
            analysis = {
                'medicines': [],
                'warnings': [],
                'interactions': [],
                'raw_response': agent_response.get('response')
            }
        
        # Prepare results
        prescription_id = key.replace('/', '-').replace('.jpg', '').replace('.png', '')
        results = {
            'prescriptionId': prescription_id,
            'sourceImage': f"s3://{bucket}/{key}",
            'timestamp': datetime.now().isoformat(),
            'analysis': analysis,
            'sessionId': session_id,
            'language': 'en'
        }
        
        # Save results
        output_key = f"results/{prescription_id}.json"
        s3_path = save_results_to_s3(results, output_key)
        print(f"💾 Results saved to: {s3_path}")
        
        # Optional: Save to DynamoDB
        if RESULTS_TABLE:
            save_results_to_dynamodb(results)
        
        print("✅ Prescription processing completed successfully")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Prescription analysis completed',
                'prescriptionId': prescription_id,
                'resultsLocation': s3_path,
                'analysis': analysis
            })
        }
        
    except Exception as e:
        print(f"❌ Unexpected error: {str(e)}")
        import traceback
        traceback.print_exc()
        return {
            'statusCode': 500,
            'body': json.dumps({
                'error': 'Internal server error',
                'details': str(e)
            })
        }
