from fastapi import FastAPI, File, UploadFile, Request
from fastapi.responses import HTMLResponse
from fastapi.templating import Jinja2Templates
from services.analyzer import DocumentAnalyzer
from services.processor import PDFProcessor, ImageProcessor

app = FastAPI()
templates = Jinja2Templates(directory="templates")

class DocumentAnalysisService:
    def __init__(self):
        self.analyzer = DocumentAnalyzer()
        self.processors = {
            'pdf': PDFProcessor(),
            'image': ImageProcessor()
        }

    def process_document(self, file_bytes: bytes, file_type: str) -> dict:
        processor = self.processors['pdf'] if file_type == 'pdf' else self.processors['image']
        extracted_text = processor.extract_text(file_bytes)
        analysis_results = self.analyzer.analyze_text(extracted_text)
        
        return {
            "analysis": {
                "risk_score": analysis_results.risk_score,
                "overall_risk_level": analysis_results.overall_risk_level.value,
                "findings": [vars(f) for f in analysis_results.findings],
                "categories": {
                    cat: [vars(f) for f in findings]
                    for cat, findings in analysis_results.categories.items()
                }
            },
            "extracted_text": extracted_text
        }

analysis_service = DocumentAnalysisService()

@app.get("/", response_class=HTMLResponse)
async def upload_form(request: Request):
    return templates.TemplateResponse("upload.html", {"request": request})

@app.post("/upload/")
async def upload_file(file: UploadFile = File(...)):
    file_bytes = await file.read()
    file_type = 'pdf' if file.filename.endswith('.pdf') else 'image'
    
    results = analysis_service.process_document(file_bytes, file_type)
    results["filename"] = file.filename
    
    return results