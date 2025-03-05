from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
import time
import os
from pathlib import Path

from .config import settings
from irish_law_analyzer.services.processor.pdf_processor import PDFProcessor
from irish_law_analyzer.services.processor.image_processor import ImageProcessor
from irish_law_analyzer.services.analyzer.document_analyzer import DocumentAnalyzer
from irish_law_analyzer.core.models import ProcessingStatus

# Utils importları
from irish_law_analyzer.utils.logger import logger
from irish_law_analyzer.utils.helpers import (
    generate_document_id,
    create_temp_file_path,
    cleanup_old_files,
    extract_metadata
)
from irish_law_analyzer.utils.validators import (
    validate_file_type,
    validate_file_size,
    validate_text_content
)

app = FastAPI(
    title=settings.APP_NAME,
    version=settings.APP_VERSION,
    debug=settings.DEBUG
)

# Static files and templates setup
app.mount("/static", StaticFiles(directory=str(settings.STATIC_DIR)), name="static")
templates = Jinja2Templates(directory=str(settings.TEMPLATES_DIR))

# Initialize services
pdf_processor = PDFProcessor()
image_processor = ImageProcessor()
document_analyzer = DocumentAnalyzer()

# Uygulama başlatılırken uploads klasörünü oluştur
UPLOAD_DIR = Path(__file__).parent.parent / "uploads"
UPLOAD_DIR.mkdir(exist_ok=True)

@app.get("/", response_class=HTMLResponse)
async def home(request: Request):
    """Render the home page with upload form"""
    return templates.TemplateResponse(
        "upload.html",
        {"request": request, "app_name": settings.APP_NAME}
    )

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    """Handle file upload and analysis"""
    temp_file_path = None
    try:
        # Read file content
        file_content = await file.read()
        
        # Validate file
        is_valid_type, type_error = validate_file_type(file_content, file.filename)
        if not is_valid_type:
            raise HTTPException(status_code=415, detail=type_error)
            
        is_valid_size, size_error = validate_file_size(file_content)
        if not is_valid_size:
            raise HTTPException(status_code=413, detail=size_error)

        # Generate unique document ID
        document_id = generate_document_id(file.filename, file_content)
        
        # Save file temporarily
        temp_file_name = f"{int(time.time())}_{file.filename}"
        temp_file_path = UPLOAD_DIR / temp_file_name
        
        with open(temp_file_path, "wb") as buffer:
            buffer.write(file_content)
        
        # Log processing start
        logger.logger.info(f"Starting processing for document: {document_id}")
        
        start_time = time.time()

        # Process file based on type
        if file.filename.endswith('.pdf'):
            processor_result = pdf_processor.process_document(file_content, file.filename)
        else:
            processor_result = image_processor.process_document(file_content, file.filename)
            
        if not processor_result.success:
            logger.log_error("ProcessingError", processor_result.error)
            raise HTTPException(
                status_code=422,
                detail=f"File processing failed: {processor_result.error}"
            )

        # Validate extracted text
        is_valid_text, text_error = validate_text_content(processor_result.extracted_text)
        if not is_valid_text:
            logger.log_error("TextExtractionError", text_error)
            raise HTTPException(status_code=422, detail=text_error)

        # Analyze document
        analysis_result = await document_analyzer.analyze_document(
            processor_result.extracted_text,
            document_id=document_id
        )
        
        # Calculate processing time
        processing_time = time.time() - start_time
        
        # Extract metadata
        metadata = {
            "filename": file.filename,
            "size": len(file_content),
            "document_id": document_id,
            "processing_time": processing_time,
            "upload_time": time.strftime("%Y-%m-%d %H:%M:%S"),
            "file_type": "PDF" if file.filename.endswith('.pdf') else "Image"
        }
        
        # Log analysis completion
        logger.log_analysis(document_id, {
            "risk_score": analysis_result.risk_score,
            "overall_risk_level": analysis_result.overall_risk_level.value,
            "findings_count": len(analysis_result.findings),
            "processing_time": processing_time
        })

        response_data = {
            "document_id": document_id,
            "filename": file.filename,
            "analysis": {
                "risk_score": analysis_result.risk_score,
                "overall_risk_level": analysis_result.overall_risk_level.value,
                "findings": [vars(f) for f in analysis_result.findings],
                "categories": {
                    cat: [vars(f) for f in findings]
                    for cat, findings in analysis_result.categories.items()
                },
                "recommendations": analysis_result.recommendations,
                "document_type": analysis_result.document_type.value,
                "processing_time": processing_time
            },
            "metadata": metadata,
            "status": analysis_result.status.value
        }

        return response_data
        
    except HTTPException as he:
        logger.log_error("HTTPException", str(he))
        raise he
    except Exception as e:
        logger.log_error("UnexpectedError", str(e))
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred during processing: {str(e)}"
        )
    finally:
        # Cleanup temporary file
        if temp_file_path and temp_file_path.exists():
            try:
                temp_file_path.unlink()
            except Exception as e:
                logger.log_error("CleanupError", f"Failed to delete temporary file: {str(e)}")

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION,
        "timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
    }

# Cleanup old files on startup
@app.on_event("startup")
async def startup_event():
    """Initialize application"""
    try:
        # Ensure required directories exist
        UPLOAD_DIR.mkdir(exist_ok=True)
        settings.STATIC_DIR.mkdir(exist_ok=True)
        settings.TEMPLATES_DIR.mkdir(exist_ok=True)
        
        # Cleanup old files
        cleanup_old_files()
        
        logger.logger.info("Application started successfully")
    except Exception as e:
        logger.log_error("StartupError", str(e))
        raise

@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    try:
        cleanup_old_files()
        logger.logger.info("Application shutdown successfully")
    except Exception as e:
        logger.log_error("ShutdownError", str(e))