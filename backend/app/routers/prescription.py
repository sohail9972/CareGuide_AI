from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import os
import tempfile
from ..services.ocr_service import extract_text_from_image
from ..services.nlp_service import extract_medicines
from ..services.aws_service import analyze_prescription


router = APIRouter()

@router.post("/upload-prescription")
async def upload_prescription(
    file: UploadFile = File(...),
    provider: str = "local",  # or "aws"
    language: str = "en"
):
    """
    Upload a prescription image and extract text and medicines.

    The `provider` parameter chooses the analysis backend:
    - `local`: use Tesseract + spaCy (current implementation)
    - `aws`: call Bedrock agent pipeline via AWS SDK

    Args:
        file: Image file to process
        provider: analysis provider
        language: target language for guidance when using AWS

    Returns:
        Dictionary with extracted_text or full guidance

    Raises:
        HTTPException: If file processing fails
    """
    # Validate file type
    if not file.content_type.startswith('image/'):
        raise HTTPException(status_code=400, detail="File must be an image")
    
    # Create a temporary file in system temp directory
    temp_file = None
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=os.path.splitext(file.filename)[1]) as temp_file:
            temp_path = temp_file.name
            # Write uploaded file to temp location
            shutil.copyfileobj(file.file, temp_file)
        
        # If the client requests AWS analysis, use that path
        if provider == "aws":
            result = analyze_prescription(temp_path, language)
            return result

        # Otherwise fall back to local OCR/NLP
        extracted_text = extract_text_from_image(temp_path)
        
        if not extracted_text or not extracted_text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from image")
        
        medicines = extract_medicines(extracted_text)
        
        return {
            "extracted_text": extracted_text,
            "medicines_detected": medicines
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing file: {str(e)}")
    
    finally:
        # Clean up temporary file
        if temp_path and os.path.exists(temp_path):
            try:
                os.remove(temp_path)
            except Exception:
                pass  # Ignore cleanup errors