import os
import json
import boto3
from typing import Dict

# Environment configuration
AWS_REGION = os.getenv("AWS_REGION", "us-east-1")
S3_BUCKET = os.getenv("S3_BUCKET", "careguide-prescriptions")
BEDROCK_MODEL = os.getenv("BEDROCK_MODEL", "anthropic.claude-3.5-sonnet")

# Lazy-load clients
_s3 = None
_bedrock = None

def _get_s3_client():
    global _s3
    if _s3 is None:
        try:
            _s3 = boto3.client("s3", region_name=AWS_REGION)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize S3 client: {str(e)}. Ensure AWS credentials are configured.")
    return _s3

def _get_bedrock_client():
    global _bedrock
    if _bedrock is None:
        try:
            _bedrock = boto3.client("bedrock", region_name=AWS_REGION)
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Bedrock client: {str(e)}. Ensure AWS credentials are configured.")
    return _bedrock


def upload_to_s3(file_path: str, key: str) -> str:
    """Upload a local file to S3 and return the object URL."""
    s3 = _get_s3_client()
    s3.upload_file(file_path, S3_BUCKET, key)
    url = f"s3://{S3_BUCKET}/{key}"
    return url


def invoke_vision_agent(s3_url: str, language: str = "en") -> Dict:
    """Send the image location to Bedrock agent and receive structured output.

    The agent is responsible for performing the multimodal vision analysis,
    RAG lookup, and translation. The prompt should be defined when the agent
    is created in the Bedrock console.
    """
    prompt = {
        "type": "text",            
        "text": (
            f"Process the prescription image at {s3_url}. "
            "Return JSON with fields medicines, dosages, duration, and provide "
            f"instructions in {language}."
        )
    }

    response = _get_bedrock_client().invoke_model(
        modelId=BEDROCK_MODEL,
        content=[
            {"type": "s3Object", "s3Url": s3_url},
            prompt
        ],
    )

    # the model output typically lives in the 'output' or 'body' field
    raw = response.get("output") or response.get("body")
    if isinstance(raw, bytes):
        raw = raw.decode("utf-8")
    try:
        return json.loads(raw)
    except Exception:
        # if the model returned text with JSON embedded, try to parse
        text = raw.strip()
        # simple heuristic
        start = text.find("{")
        end = text.rfind("}")
        if start != -1 and end != -1:
            return json.loads(text[start : end + 1])
        raise


def analyze_prescription(image_path: str, language: str = "en") -> Dict:
    """High‑level helper that uploads the image then invokes the agent."""
    key = os.path.basename(image_path)
    s3_url = upload_to_s3(image_path, key)
    return invoke_vision_agent(s3_url, language)
