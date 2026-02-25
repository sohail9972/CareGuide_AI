from sqlalchemy import Column, Integer, String
from .database import Base

class Prescription(Base):
    __tablename__ = "prescriptions"

    id = Column(Integer, primary_key=True, index=True)
    extracted_text = Column(String)