from fastapi import FastAPI, File, UploadFile, HTTPException, Request
from fastapi.responses import HTMLResponse
from fastapi.staticfiles import StaticFiles
from fastapi.templating import Jinja2Templates
from typing import Optional
import uvicorn
import time

from .config import settings
from services.processor.pdf_processor import PDFProcessor
from services.processor.image_processor import ImageProcessor
from services.analyzer.document_analyzer import DocumentAnalyzer
from core.models import ProcessingStatus

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
    try:
        # Validate file
        await validate_file(file)
        
        # Read file content
        start_time = time.time()
        file_bytes = await file.read()
        
        # Process file based on type
        if file.filename.endswith('.pdf'):
            processor_result = pdf_processor.process_document(file_bytes, file.filename)
        else:
            processor_result = image_processor.process_document(file_bytes, file.filename)
            
        if not processor_result.success:
            raise HTTPException(
                status_code=422,
                detail=f"File processing failed: {processor_result.error}"
            )
        
        # Analyze document
        analysis_result = await document_analyzer.analyze_document(
            processor_result.extracted_text,
            document_id=file.filename
        )
        
        # Prepare response
        processing_time = time.time() - start_time
        
        return {
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
            "metadata": analysis_result.metadata,
            "status": analysis_result.status.value
        }
        
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"An error occurred during processing: {str(e)}"
        )

async def validate_file(file: UploadFile) -> None:
    """Validate uploaded file"""
    # Check file size
    file_size = 0
    chunk_size = 1024  # 1KB
    while chunk := await file.read(chunk_size):
        file_size += len(chunk)
        if file_size > settings.MAX_FILE_SIZE:
            raise HTTPException(
                status_code=413,
                detail="File too large"
            )
    
    # Reset file position after reading
    await file.seek(0)
    
    # Check file extension
    ext = file.filename.split('.')[-1].lower()
    if ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=415,
            detail=f"File type not allowed. Allowed types: {settings.ALLOWED_EXTENSIONS}"
        )

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "app_name": settings.APP_NAME,
        "version": settings.APP_VERSION
    }

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )