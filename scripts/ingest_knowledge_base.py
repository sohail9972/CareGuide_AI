#!/usr/bin/env python3
"""
Script to ingest RxNorm and OpenFDA data into Bedrock Knowledge Base.
Processes medicine data and creates chunked documents for RAG.
"""

import json
import csv
import boto3
import requests
from typing import List, Dict, Any
from datetime import datetime

bedrock_agents = boto3.client('bedrock-agents', region_name='us-east-1')
s3 = boto3.client('s3')


def fetch_rxnorm_sample() -> List[Dict[str, Any]]:
    """
    Fetch sample RxNorm data. In production, download the full RxNorm database.
    URL: https://www.nlm.nih.gov/research/umls/rxnorm/docs/rxnormfiles.html
    """
    # Sample medicine data structure
    sample_medicines = [
        {
            "drugName": "Aspirin",
            "rxcui": "5209",
            "strength": "500 mg",
            "form": "Tablet",
            "indications": "Pain relief, fever reduction, antiplatelet effects",
            "doseAndAdministration": "Usually 500-1000 mg every 4-6 hours",
            "contraindications": "Hypersensitivity to salicylates, active bleeding",
            "sideEffects": "GI upset, heartburn, rash, tinnitus",
            "warnings": "Risk of GI bleeding, especially with long-term use",
            "interactions": "Warfarin, NSAIDs, methotrexate"
        },
        {
            "drugName": "Paracetamol",
            "rxcui": "7371",
            "strength": "500 mg",
            "form": "Tablet",
            "indications": "Pain relief, fever reduction",
            "doseAndAdministration": "500-1000 mg every 4-6 hours, max 4 g/day",
            "contraindications": "Hypersensitivity, severe hepatic disease",
            "sideEffects": "Rash, jaundice, hepatotoxicity (rare)",
            "warnings": "Risk of hepatotoxicity especially with alcohol",
            "interactions": "Warfarin, hepatotoxic drugs"
        },
        {
            "drugName": "Metformin",
            "rxcui": "6809",
            "strength": "500 mg",
            "form": "Tablet",
            "indications": "Type 2 diabetes management",
            "doseAndAdministration": "Starting 500 mg once or twice daily, titrate to 1000-2000 mg/day",
            "contraindications": "eGFR <30 mL/min, acute illness, contrast procedures",
            "sideEffects": "GI upset, diarrhea, metallic taste, lactic acidosis (rare)",
            "warnings": "Lactic acidosis risk, especially in renal impairment",
            "interactions": "Alcohol, contrast dyes, ranolazine"
        },
        {
            "drugName": "Lisinopril",
            "rxcui": "21600",
            "strength": "10 mg",
            "form": "Tablet",
            "indications": "Hypertension, heart failure, post-MI",
            "doseAndAdministration": "Starting 10 mg once daily, usual 10-40 mg/day",
            "contraindications": "ACE inhibitor cough history, pregnancy, angioedema",
            "sideEffects": "Dry cough, dizziness, hyperkalemia, angioedema",
            "warnings": "Monitor renal function and potassium levels",
            "interactions": "NSAIDs, potassium supplements, ARBs"
        }
    ]
    return sample_medicines


def create_document_chunks(medicines: List[Dict[str, Any]]) -> List[str]:
    """Convert medicine data into text chunks for embedding."""
    documents = []
    for med in medicines:
        doc = f"""
Medicine: {med['drugName']}
RxCUI: {med['rxcui']}
Strength: {med['strength']}
Form: {med['form']}

Indications:
{med['indications']}

Dosage and Administration:
{med['doseAndAdministration']}

Contraindications:
{med['contraindications']}

Side Effects:
{med['sideEffects']}

Warnings:
{med['warnings']}

Drug Interactions:
{med['interactions']}
"""
        documents.append(doc.strip())
    return documents


def upload_documents_to_kb(kb_id: str, documents: List[str]) -> None:
    """Upload documents to the Knowledge Base."""
    try:
        # Create a JSON file with the documents
        payload = {
            "documents": [
                {
                    "title": f"Medicine_{i}",
                    "content": doc,
                    "metadata": {
                        "source": "RxNorm+OpenFDA",
                        "ingestionDate": datetime.now().isoformat()
                    }
                }
                for i, doc in enumerate(documents)
            ]
        }
        
        # Save to a temporary file and upload to S3
        temp_file = "/tmp/kb_documents.json"
        with open(temp_file, 'w') as f:
            json.dump(payload, f, indent=2)
        
        # Upload to S3 for Knowledge Base ingestion
        s3_key = f"bedrock-kb/documents_{datetime.now().timestamp()}.json"
        s3.upload_file(temp_file, "careguide-kb-bucket", s3_key)
        print(f"✅ Documents uploaded to S3: {s3_key}")
        
        # Trigger KB ingestion
        print(f"📥 Ingesting documents into KB: {kb_id}")
        # Note: actual ingestion depends on KB type and configuration
        print("⚠️  Manual ingestion may be required via AWS Console")
        
    except Exception as e:
        print(f"❌ Error uploading documents: {e}")
        raise


def fetch_openfda_adverse_events(medicine_name: str) -> Dict[str, Any]:
    """Fetch adverse event data from OpenFDA API."""
    try:
        url = f"https://api.fda.gov/drug/event.json?search=patient.drug.openfda.generic_name:{medicine_name}&limit=10"
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            return response.json()
        else:
            print(f"⚠️  Could not fetch OpenFDA data for {medicine_name}")
            return {}
    except Exception as e:
        print(f"❌ Error fetching OpenFDA data: {e}")
        return {}


def enrich_medicine_data(medicines: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """Enrich medicine data with OpenFDA adverse event information."""
    print("🔍 Enriching with OpenFDA adverse events...")
    for med in medicines:
        openfda_data = fetch_openfda_adverse_events(med['drugName'].lower())
        if openfda_data.get('results'):
            adverse_count = len(openfda_data['results'])
            med['adverseEventCount'] = adverse_count
            print(f"  - {med['drugName']}: {adverse_count} adverse events found")
    return medicines


if __name__ == "__main__":
    print("🚀 Starting Knowledge Base Ingestion...\n")
    
    KB_ID = "PLACEHOLDER_KB_ID"  # Replace with actual KB ID from setup_bedrock_agent.py
    
    # Step 1: Fetch medicine data
    print("📥 Fetching RxNorm sample data...")
    medicines = fetch_rxnorm_sample()
    print(f"✅ Loaded {len(medicines)} medicines\n")
    
    # Step 2: Optionally enrich with OpenFDA
    # Uncomment to enrich (requires internet access)
    # print("🌐 Enriching with OpenFDA data...")
    # medicines = enrich_medicine_data(medicines)
    # print()
    
    # Step 3: Create document chunks
    print("📄 Creating document chunks...")
    documents = create_document_chunks(medicines)
    print(f"✅ Created {len(documents)} document chunks\n")
    
    # Step 4: Upload to KB
    print("📤 Uploading to Knowledge Base...")
    # upload_documents_to_kb(KB_ID, documents)
    print("⚠️  Update KB_ID and uncomment to ingest into actual KB\n")
    
    print("✅ Knowledge Base ingestion preparation complete!")
    print("\n📖 To complete ingestion:")
    print("1. Set up your AWS OpenSearch cluster")
    print("2. Create a Bedrock Knowledge Base pointing to OpenSearch")
    print("3. Update KB_ID in this script")
    print("4. Run to ingest documents")
