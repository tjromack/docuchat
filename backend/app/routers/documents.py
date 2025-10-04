from fastapi import APIRouter, File, UploadFile, HTTPException, Depends
from sqlalchemy.orm import Session
from ..models.database import get_db
from ..models.document import Document
from ..services.document_processor import DocumentProcessor
import os
import uuid
import traceback
from datetime import datetime

router = APIRouter(prefix="/api/documents", tags=["documents"])

# Initialize document processor
doc_processor = DocumentProcessor()

@router.post("/upload")
async def upload_document(file: UploadFile = File(...), db: Session = Depends(get_db)):
    """Upload and process a document"""
    try:
        print(f"Starting upload for file: {file.filename}")
        
        # Validate file exists
        if not file.filename:
            print("Error: No filename provided")
            raise HTTPException(status_code=400, detail="No file provided")
        
        # Validate file type
        allowed_types = ['.pdf', '.docx', '.txt']
        file_ext = os.path.splitext(file.filename)[1].lower()
        
        if file_ext not in allowed_types:
            print(f"Error: Invalid file type {file_ext}")
            raise HTTPException(
                status_code=400, 
                detail=f"File type {file_ext} not supported. Allowed: {allowed_types}"
            )
        
        print(f"File type {file_ext} is valid")
        
        # Read file content
        try:
            file_content = await file.read()
            file_size = len(file_content)
            print(f"File read successfully, size: {file_size} bytes")
        except Exception as e:
            print(f"Error reading file: {str(e)}")
            raise HTTPException(status_code=400, detail=f"Could not read file: {str(e)}")
        
        # File size check (10MB limit)
        if file_size > 10 * 1024 * 1024:
            print(f"Error: File too large ({file_size} bytes)")
            raise HTTPException(status_code=400, detail="File too large. Maximum size is 10MB.")
        
        # Generate unique filename
        unique_filename = f"{uuid.uuid4()}{file_ext}"
        upload_folder = os.getenv("UPLOAD_FOLDER", "../data/uploads")
        
        print(f"Upload folder: {upload_folder}")
        print(f"Unique filename: {unique_filename}")
        
        # Create upload directory if it doesn't exist
        try:
            os.makedirs(upload_folder, exist_ok=True)
            print(f"Upload directory ensured: {upload_folder}")
        except Exception as e:
            print(f"Error creating upload directory: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Could not create upload directory: {str(e)}")
        
        # Save file to disk
        file_path = os.path.join(upload_folder, unique_filename)
        try:
            with open(file_path, "wb") as f:
                f.write(file_content)
            print(f"File saved to: {file_path}")
        except Exception as e:
            print(f"Error saving file: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Could not save file: {str(e)}")
        
        # Create initial database record
        try:
            document = Document(
                filename=unique_filename,
                original_filename=file.filename,
                file_type=file_ext,
                file_size=file_size,
                processing_status="processing"
            )
            db.add(document)
            db.commit()
            db.refresh(document)
            print(f"Document record created with ID: {document.id}")
        except Exception as e:
            print(f"Database error: {str(e)}")
            raise HTTPException(status_code=500, detail=f"Database error: {str(e)}")
        
        # Process document (extract, chunk, embed, store)
        try:
            print("Starting document processing pipeline...")
            processing_result = doc_processor.process_document(
                file_content=file_content,
                file_type=file_ext,
                document_id=document.id,
                metadata={
                    "filename": file.filename,
                    "file_type": file_ext
                }
            )
            
            if not processing_result["success"]:
                # Update document with error status
                document.processing_status = "error"
                document.error_message = processing_result.get("error", "Processing failed")
                db.commit()
                
                raise HTTPException(
                    status_code=500,
                    detail=f"Document processing failed: {processing_result.get('error')}"
                )
            
            # Update document with success status
            document.processing_status = "completed"
            document.processed_date = datetime.utcnow()
            document.chunk_count = processing_result["chunk_count"]
            
            # Generate preview from first chunk (if available)
            if processing_result["chunk_count"] > 0:
                # We'll keep the preview simple for now
                document.content_preview = f"Document processed into {processing_result['chunk_count']} chunks"
            
            db.commit()
            db.refresh(document)
            
            print(f"Document processing completed. Chunks created: {processing_result['chunk_count']}")
            
        except HTTPException:
            raise
        except Exception as e:
            print(f"Error during processing: {str(e)}")
            print(f"Traceback: {traceback.format_exc()}")
            
            # Update document with error
            document.processing_status = "error"
            document.error_message = str(e)
            db.commit()
            
            raise HTTPException(status_code=500, detail=f"Processing failed: {str(e)}")
        
        # Prepare response
        response_data = {
            "id": document.id,
            "filename": document.original_filename,
            "file_type": file_ext,
            "file_size": file_size,
            "status": "uploaded_successfully",
            "chunk_count": document.chunk_count,
            "processing_status": document.processing_status,
            "upload_date": document.upload_date.isoformat() if document.upload_date else None
        }
        
        print("Upload completed successfully")
        return response_data
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Unexpected error in upload: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Unexpected server error: {str(e)}")

# Keep your existing list_documents and get_document functions...

@router.get("/")
async def list_documents(db: Session = Depends(get_db)):
    """List all uploaded documents"""
    try:
        print("Fetching all documents...")
        documents = db.query(Document).order_by(Document.upload_date.desc()).all()
        print(f"Found {len(documents)} documents")
        
        result = [
            {
                "id": doc.id,
                "filename": doc.original_filename,
                "file_type": doc.file_type,
                "file_size": doc.file_size,
                "upload_date": doc.upload_date.isoformat() if doc.upload_date else None,
                "status": doc.processing_status,
                "chunk_count": doc.chunk_count,
                "preview": doc.content_preview,
                "error": doc.error_message if doc.processing_status == "error" else None
            }
            for doc in documents
        ]
        
        return result
        
    except Exception as e:
        print(f"Error listing documents: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Could not list documents: {str(e)}")

@router.get("/{document_id}")
async def get_document(document_id: int, db: Session = Depends(get_db)):
    """Get a specific document by ID"""
    try:
        print(f"Fetching document with ID: {document_id}")
        document = db.query(Document).filter(Document.id == document_id).first()
        
        if not document:
            print(f"Document {document_id} not found")
            raise HTTPException(status_code=404, detail="Document not found")
        
        response_data = {
            "id": document.id,
            "filename": document.original_filename,
            "file_type": document.file_type,
            "file_size": document.file_size,
            "upload_date": document.upload_date.isoformat() if document.upload_date else None,
            "processed_date": document.processed_date.isoformat() if document.processed_date else None,
            "status": document.processing_status,
            "chunk_count": document.chunk_count,
            "preview": document.content_preview,
            "error": document.error_message if document.processing_status == "error" else None
        }
        
        print(f"Document {document_id} retrieved successfully")
        return response_data
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error retrieving document {document_id}: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Could not retrieve document: {str(e)}")

@router.delete("/{document_id}")
async def delete_document(document_id: int, db: Session = Depends(get_db)):
    """Delete a document by ID"""
    try:
        print(f"Deleting document with ID: {document_id}")
        document = db.query(Document).filter(Document.id == document_id).first()
        
        if not document:
            print(f"Document {document_id} not found for deletion")
            raise HTTPException(status_code=404, detail="Document not found")
        
        # Delete from vector store
        doc_processor.delete_document(document_id)
        
        # Delete file from disk if it exists
        upload_folder = os.getenv("UPLOAD_FOLDER", "../data/uploads")
        file_path = os.path.join(upload_folder, document.filename)
        
        if os.path.exists(file_path):
            try:
                os.remove(file_path)
                print(f"File deleted from disk: {file_path}")
            except Exception as e:
                print(f"Warning: Could not delete file from disk: {str(e)}")
        
        # Delete from database
        filename = document.original_filename
        db.delete(document)
        db.commit()
        
        print(f"Document '{filename}' deleted successfully")
        return {"message": f"Document '{filename}' deleted successfully"}
        
    except HTTPException:
        raise
    except Exception as e:
        print(f"Error deleting document {document_id}: {str(e)}")
        print(f"Traceback: {traceback.format_exc()}")
        raise HTTPException(status_code=500, detail=f"Could not delete document: {str(e)}")