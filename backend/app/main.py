from fastapi import FastAPI
from .routers import prescription
from .database import engine, Base

app = FastAPI(title="CareGuide AI Backend")

Base.metadata.create_all(bind=engine)

app.include_router(prescription.router)