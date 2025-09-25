from sqlalchemy import Column, Integer, String, DateTime, Text
from sqlalchemy.sql import func
from .database import Base

class Document(Base):
    __tablename__ = "documents"
    
    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String(255), nullable=False)
    original_filename = Column(String(255), nullable=False)
    file_type = Column(String(10), nullable=False)
    file_size = Column(Integer, nullable=False)
    upload_date = Column(DateTime, server_default=func.now())
    processed_date = Column(DateTime)
    content_preview = Column(Text)
    chunk_count = Column(Integer, default=0)
    processing_status = Column(String(20), default="pending")  # pending, processing, completed, error
    error_message = Column(Text)