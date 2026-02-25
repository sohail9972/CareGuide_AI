from fastapi import APIRouter, UploadFile, File, HTTPException
import shutil
import os
import tempfile
from ..services.ocr_service import extract_text_from_image
from ..services.nlp_service import extract_medicines

router = APIRouter()

@router.post("/upload-prescription")
async def upload_prescription(file: UploadFile = File(...)):
    """
    Upload a prescription image and extract text and medicines.
    
    Args:
        file: Image file to process
        
    Returns:
        Dictionary with extracted_text and medicines_detected
        
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
        
        # Extract text from image using OCR
        extracted_text = extract_text_from_image(temp_path)
        
        if not extracted_text or not extracted_text.strip():
            raise HTTPException(status_code=400, detail="Could not extract text from image")
        
        # Extract medicines from extracted text
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