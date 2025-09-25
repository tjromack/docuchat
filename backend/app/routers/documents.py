from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from sqlalchemy.orm import Session
from ..models.database import get_db
from ..models.document import Document
from ..services.text_extractor import TextExtractor
import os
import uuid
from datetime import datetime

router = APIRouter(prefix="/api/documents", tags=["documents"])

@router.post("/upload")
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    # Validate file
    if not file.filename:
        raise HTTPException(status_code=400, detail="No file provided")
    
    allowed_types = ['.pdf', '.docx', '.txt']
    file_ext = os.path.splitext(file.filename)[1].lower()
    
    if file_ext not in allowed_types:
        raise HTTPException(
            status_code=400, 
            detail=f"File type {file_ext} not supported. Allowed: {allowed_types}"
        )
    
    # File size check (10MB limit)
    file_content = await file.read()
    file_size = len(file_content)
    
    if file_size > 10 * 1024 * 1024:  # 10MB
        raise HTTPException(status_code=400, detail="File too large. Maximum size is 10MB.")
    
    # Generate unique filename
    unique_filename = f"{uuid.uuid4()}{file_ext}"
    upload_folder = os.getenv("UPLOAD_FOLDER", "../data/uploads")
    os.makedirs(upload_folder, exist_ok=True)
    
    # Save file
    file_path = os.path.join(upload_folder, unique_filename)
    with open(file_path, "wb") as f:
        f.write(file_content)
    
    # Extract text
    extraction_result = TextExtractor.extract_text(file_content, file_ext)
    
    if not extraction_result["success"]:
        # Save document with error status
        document = Document(
            filename=unique_filename,
            original_filename=file.filename,
            file_type=file_ext,
            file_size=file_size,
            processing_status="error",
            error_message=extraction_result["error"]
        )
        db.add(document)
        db.commit()
        
        raise HTTPException(
            status_code=500, 
            detail=f"Text extraction failed: {extraction_result['error']}"
        )
    
    # Generate content preview
    content_preview = TextExtractor.get_preview(extraction_result["text"])
    
    # Save to database
    document = Document(
        filename=unique_filename,
        original_filename=file.filename,
        file_type=file_ext,
        file_size=file_size,
        content_preview=content_preview,
        processing_status="completed",
        processed_date=datetime.utcnow()
    )
    
    db.add(document)
    db.commit()
    db.refresh(document)
    
    return {
        "id": document.id,
        "filename": document.original_filename,
        "file_type": file_ext,
        "file_size": file_size,
        "status": "uploaded_successfully",
        "preview": document.content_preview,
        "metadata": extraction_result["metadata"],
        "word_count": extraction_result["metadata"].get("words", "N/A"),
        "upload_date": document.upload_date
    }

@router.get("/")
async def list_documents(db: Session = Depends(get_db)):
    documents = db.query(Document).order_by(Document.upload_date.desc()).all()
    return [
        {
            "id": doc.id,
            "filename": doc.original_filename,
            "file_type": doc.file_type,
            "file_size": doc.file_size,
            "upload_date": doc.upload_date,
            "status": doc.processing_status,
            "preview": doc.content_preview,
            "error": doc.error_message if doc.processing_status == "error" else None
        }
        for doc in documents
    ]

@router.get("/{document_id}")
async def get_document(document_id: int, db: Session = Depends(get_db)):
    document = db.query(Document).filter(Document.id == document_id).first()
    
    if not document:
        raise HTTPException(status_code=404, detail="Document not found")
    
    return {
        "id": document.id,
        "filename": document.original_filename,
        "file_type": document.file_type,
        "file_size": document.file_size,
        "upload_date": document.upload_date,
        "processed_date": document.processed_date,
        "status": document.processing_status,
        "preview": document.content_preview
    }