from typing import List, Optional
import pdfplumber
import pytesseract
from pdf2image import convert_from_bytes
from PIL import Image
import io
import time
from .base import BaseDocumentProcessor
from core.models import ProcessingResult, DocumentMetadata
from app.config import settings

class PDFProcessor(BaseDocumentProcessor):
    def __init__(self):
        super().__init__()
        self.supported_mime_types = {'application/pdf'}
        self.dpi = settings.OCR_DPI           # Değişti
        self.ocr_language = settings.OCR_LANGUAGE  # Değişti
        self.enable_ocr = True

    def extract_text(self, file_bytes: bytes, filename: str) -> ProcessingResult:
        try:
            # First try direct text extraction
            text = self._extract_text_direct(file_bytes)
            
            # If no text found and OCR is enabled, try OCR
            if not text.strip() and self.enable_ocr:
                text = self._extract_text_ocr(file_bytes)

            # Get metadata
            metadata = self._get_pdf_metadata(file_bytes, filename)

            return ProcessingResult(
                success=True,
                message="PDF processed successfully",
                extracted_text=text,
                metadata=metadata
            )

        except Exception as e:
            return ProcessingResult(
                success=False,
                message="PDF processing failed",
                error=str(e)
            )

    def _extract_text_direct(self, file_bytes: bytes) -> str:
        text = ""
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            for page in pdf.pages:
                text += page.extract_text() or ""
        return text

    def _extract_text_ocr(self, file_bytes: bytes) -> str:
        text = ""
        images = convert_from_bytes(file_bytes, dpi=self.dpi)
        
        for image in images:
            text += pytesseract.image_to_string(
                image, 
                lang=self.ocr_language,
                config='--psm 1 --oem 3'
            )
        
        return text

    def _get_pdf_metadata(self, file_bytes: bytes, filename: str) -> DocumentMetadata:
        with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
            metadata = DocumentMetadata(
                file_name=filename,
                file_size=len(file_bytes),
                mime_type='application/pdf',
                page_count=len(pdf.pages),
                word_count=len(self._extract_text_direct(file_bytes).split())
            )
        return metadata

    def set_ocr_language(self, language: str):
        """Set OCR language (e.g., 'eng', 'fra', etc.)"""
        self.ocr_language = language

    def set_dpi(self, dpi: int):
        """Set DPI for image conversion"""
        self.dpi = dpi

    def enable_ocr_processing(self, enable: bool):
        """Enable or disable OCR processing"""
        self.enable_ocr = enable