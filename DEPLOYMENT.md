# Deployment Guide

There are multiple ways to run CareGuide AI without local installation:

## Option 1: GitHub Codespaces (Easiest - Free for GitHub Pro users)

**Steps:**
1. Go to your repository: https://github.com/sohail9972/CareGuide_AI
2. Click **Code** → **Codespaces** → **Create codespace on main**
3. Wait for the environment to set up (2-3 minutes)
4. In the terminal, the setup will automatically install all dependencies

**Run the application:**
```bash
# Terminal 1: Backend
cd backend
python -m uvicorn app.main:app --reload

# Terminal 2: Frontend
cd careguide-frontend
npm run dev
```

Both services will be available at the ports shown in VS Code.

---

## Option 2: Docker (For any machine)

**Requirements:** Docker and Docker Compose installed

**Steps:**

1. **Clone the repository:**
   ```bash
   git clone https://github.com/sohail9972/CareGuide_AI.git
   cd CareGuide_AI
   ```
   
   # install backend dependencies (includes EasyOCR model)
   cd backend
   pip install -r requirements.txt
   python -m spacy download en_core_web_sm
   pip install opencv-python

   # environment variable to control OCR engine:
   #   OCR_ENGINE=pytesseract | easyocr | auto (default)
   # easyocr tends to be more accurate on handwritten/messy text.

   # Note: EasyOCR will be used automatically if installed; it often produces higher-quality text on handwritten/prescription images.


2. **Run with Docker Compose:**
   ```bash
   docker-compose up
   ```

3. **Access the application:**
   - Frontend: http://localhost:3000
   - Backend API: http://localhost:8000
   - API Documentation: http://localhost:8000/docs

---

## Option 3: Deploy Frontend to Vercel (Free)

**Steps:**

1. Go to https://vercel.com/new
2. Connect your GitHub account
3. Select the **CareGuide_AI** repository
4. Configure settings:
   - Framework: Next.js
   - Root Directory: `careguide-frontend`
5. Add environment variable:
   ```
   NEXT_PUBLIC_API_URL=your-backend-url
   ```
6. Click **Deploy**

Your frontend will be live immediately!

---

## Option 4: Deploy Backend to Railway.app (Free tier available)

**Steps:**

1. Go to https://railway.app
2. Click **New Project** → **Deploy from GitHub**
3. Select your repository
4. Add a service:
   - Service: Python
   - Root Directory: `backend`
5. Add environment variable:
   ```
   TESSERACT_PATH=/usr/bin/tesseract
   ```
6. Deploy

**Note:** Railway provides free tier with limited resources. For production, upgrade to paid plan.

**Alternative:** Use Render.com with similar steps.

---

## Option 5: Deploy Backend to Heroku (Free tier deprecated)

Use Railway or Render instead for free hosting.

---

## Complete Cloud Deployment (Recommended)

**Frontend:** Vercel (Free)
**Backend:** Railway.app (Free tier) or Render
**Database:** PostgreSQL on Railway or AWS RDS

---

## Environment Variables Needed

### Backend (.env)
```
DATABASE_URL=your_database_url
TESSERACT_PATH=/usr/bin/tesseract
PYTHONUNBUFFERED=1
```

### Frontend (.env.local)
```
NEXT_PUBLIC_API_URL=https://your-backend-url.com
```

---

## Quick Start Commands

### Local Development
```bash
# Backend
cd backend
pip install -r requirements.txt
python -m spacy download en_core_web_sm
python -m uvicorn app.main:app --reload

# Frontend
cd careguide-frontend
npm install
npm run dev
```

### Docker
```bash
docker-compose up
```

### GitHub Codespaces
1. Click "Code" → "Codespaces"
2. Run the commands in the terminal

---

## Troubleshooting

**Tesseract not found:**
- For Docker: Already installed
- For Codespaces: Automatically installed
- For local: Install from https://github.com/UB-Mannheim/tesseract/wiki

**Spacy model missing:**
```bash
python -m spacy download en_core_web_sm
```

**Port already in use:**
```bash
docker-compose down  # Stop containers
docker-compose up    # Start fresh
```

---

## AWS Integration (optional)

To run the new AWS‑native pipeline, perform the following additional steps:

1. **Create and configure Bedrock resources**
   * Build a Bedrock Agent that accepts an S3 URI, runs the multimodal vision model (`anthropic.claude-3.5-sonnet`), performs RAG lookups against a Knowledge Base, and translates the results. Store the agent ID in an environment variable `BEDROCK_AGENT_ID`.
   * Populate a Knowledge Base with medicine information (download RxNorm/OpenFDA datasets and ingest via the Bedrock console or API).

2. **Provision AWS infrastructure**
   * Create an Amazon S3 bucket for prescription images (`S3_BUCKET`).
   * Deploy a Lambda function (see `specs/design.md`) that triggers on object creation and invokes the Bedrock agent using the AWS SDK.
   * Ensure your Lambda role has `bedrock:InvokeModel`, `s3:GetObject`, `s3:PutObject`, and optional DynamoDB or SQS permissions if you store results.

3. **Set environment variables** for the backend service, either in `.env` or the deployment platform:
   ```bash
   AWS_REGION=us-east-1
   S3_BUCKET=your-bucket-name
   BEDROCK_MODEL=anthropic.claude-3.5-sonnet
   BEDROCK_AGENT_ID=your-agent-id
   ```

4. **Use the AWS provider** in your API calls:
   ```bash
   curl -F "file=@prescription.jpg" "http://localhost:8000/upload-prescription?provider=aws&language=hi"
   ```

5. **Monitor & logs**: View Lambda logs in CloudWatch and Bedrock call details in AWS Console.

## Getting Help

- Check the main [README.md](README.md)
- Review the [GitHub Issues](https://github.com/sohail9972/CareGuide_AI/issues)
- Check API docs at: http://localhost:8000/docs
