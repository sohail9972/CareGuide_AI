# Requirements for CareGuide AI Migration to AWS Generative AI Stack

## Project Goal
Digitize handwritten medical prescriptions and provide accurate, **multilingual recovery guidance** for patients in the "AI for Bharat" initiative.

## Functional Requirements
1. **Image ingestion**: Users upload prescription images via the frontend. The backend stores them in Amazon S3 and triggers processing.
2. **Vision analysis**: Use an Amazon Bedrock multimodal foundation model (Claude 3.5 Sonnet) to read handwriting and output a structured JSON object containing medicines, dosages, frequencies, and durations.
3. **Knowledge augmentation (RAG)**: Connect the extracted medicine names to a Bedrock Knowledge Base populated from authoritative datasets such as RxNorm or OpenFDA. Provide verified descriptions, side‑effects, and recovery steps.
4. **Multilingual guidance**: Generate patient instructions in the language selected by the user (Hindi, English, etc.) using Bedrock natural‑language capabilities.
5. **Orchestration agent**: Create a Bedrock Agent that chains the vision call, RAG lookup, and translation into a single workflow.
6. **API endpoints**: The FastAPI backend must expose a `/upload-prescription` route that accepts images, triggers the AWS pipeline, and returns the final guidance payload.
7. **Edge events**: Implement an S3 upload trigger using AWS Lambda to start processing automatically.
8. **Logging & audit**: Record each step and any model outputs for compliance and debugging.

## Non‑Functional Requirements
* **Latency**: Prediction pipeline should complete within 5 seconds for a single prescription.
* **Scalability**: Architecture must scale automatically via AWS serverless features.
* **Security**: Images stored encrypted (S3 SSE), API secured with Cognito or API key.
* **Cost‑efficient**: Use free-tier and low‑cost Bedrock models where possible.

## Kiro‑generated Tasks
- **Task: Replace OCR/NLP pipeline** – Remove local `ocr_service.py` / `nlp_service.py`. Implement an AWS agentic workflow that sends images to Bedrock's Claude 3.5 Sonnet for vision and uses Bedrock Agents for orchestration.
- **Task: Build knowledge base** – Create and populate a Bedrock Knowledge Base from RxNorm/OpenFDA CSVs; write a small script to automate ingestion.
- **Task: Multilingual translation** – Configure the agent to call Bedrock's text‑generation endpoint to translate guidance into requested languages.
- **Task: S3 Lambda trigger** – Define a Lambda function (Python) that fires on object creation and invokes the backend or directly calls Bedrock.
- **Task: API orchestration** – Expand FastAPI to call a new `aws_service.py` that wraps Boto3 calls to Bedrock and S3.

These tasks will guide the Spec‑Driven Development (SDD) workflow.
