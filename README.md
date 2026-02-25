# CareGuide AI - Prescription OCR & Medicine Detection

CareGuide AI is an intelligent system that extracts text from prescription images and automatically identifies medicines using OCR and NLP technologies.

## Features

- **OCR (Optical Character Recognition)**: Extracts text from prescription images using Tesseract
- **Medicine Detection**: Identifies medicine names from extracted text using pattern matching and spacy NER
- **Image Preprocessing**: Advanced image enhancement for better OCR accuracy
- **FastAPI Backend**: RESTful API for prescription processing
- **Modern Frontend**: Next.js-based user interface

## Project Structure

```
CareGuide_AI/
├── backend/                    # Python FastAPI backend
│   ├── app/
│   │   ├── main.py            # FastAPI application
│   │   ├── models.py          # Database models
│   │   ├── database.py        # Database configuration
│   │   ├── routers/           # API routes
│   │   │   └── prescription.py
│   │   └── services/          # Business logic
│   │       ├── ocr_service.py     # Tesseract OCR integration
│   │       └── nlp_service.py     # Medicine detection
│   └── requirements.txt        # Python dependencies
│
└── careguide-frontend/        # Next.js frontend
    ├── app/
    ├── components/
    └── public/
```

## Installation

### Backend Setup

1. **Install Tesseract OCR**:
   - Download from: https://github.com/UB-Mannheim/tesseract/wiki
   - Default install path: `C:\Program Files\Tessract_OCR\`

2. **Install Python Dependencies**:
   ```bash
   cd backend
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   ```

3. **Install OpenCV** (for advanced image processing):
   ```bash
   pip install opencv-python
   ```

### Frontend Setup

```bash
cd careguide-frontend
npm install
npm run dev
```

## Running the Application

### Start Backend Server

```bash
cd backend
python -m uvicorn app.main:app --reload --host 127.0.0.1 --port 8000
```

Access the API documentation at: http://127.0.0.1:8000/docs

### Start Frontend

```bash
cd careguide-frontend
npm run dev
```

## API Endpoints

### Upload Prescription
- **Endpoint**: `POST /upload-prescription`
- **Content-Type**: `multipart/form-data`
- **Parameter**: `file` (image file)
- **Response**:
  ```json
  {
    "extracted_text": "...",
    "medicines_detected": ["aspirin", "paracetamol", ...]
  }
  ```

## Technologies Used

### Backend
- **FastAPI**: Modern Python web framework
- **Tesseract OCR**: Optical character recognition
- **Spacy**: NLP for entity recognition
- **SQLAlchemy**: ORM for database operations
- **OpenCV**: Advanced image processing

### Frontend
- **Next.js**: React framework
- **TypeScript**: Type-safe JavaScript
- **Tailwind CSS**: Utility-first CSS framework

## Configuration

### Tesseract Path
If Tesseract is installed in a custom location, set the environment variable:
```bash
$env:TESSERACT_PATH = "C:\Program Files\Tessract_OCR\tesseract.exe"
```

## Future Enhancements

- [ ] Cloud storage integration for prescriptions
- [ ] Document management system
- [ ] User authentication and profiles
- [ ] Prescription history tracking
- [ ] Export reports (PDF, CSV)
- [ ] Mobile app support

## License

MIT License - feel free to use this project for personal or educational purposes.

## Author

**Sohail** (@sohail9972)

## Support

For issues, questions, or suggestions, please open an issue on GitHub.
