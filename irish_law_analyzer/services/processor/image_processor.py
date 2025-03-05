from typing import List
import pytesseract
from PIL import Image
import io
from .base import BaseDocumentProcessor
from core.models import ProcessingResult, DocumentMetadata
from app.config import settings

class ImageProcessor(BaseDocumentProcessor):
    def __init__(self):
        super().__init__()
        self.supported_mime_types = {
            'image/jpeg', 
            'image/png', 
            'image/tiff', 
            'image/bmp'
        }
        self.ocr_language = settings.OCR_LANGUAGE
        self.min_quality = 300  # Minimum DPI

    def extract_text(self, file_bytes: bytes, filename: str) -> ProcessingResult:
        try:
            # Open image
            image = Image.open(io.BytesIO(file_bytes))
            
            # Preprocess image if needed
            processed_image = self._preprocess_image(image)
            
            # Extract text using OCR
            text = pytesseract.image_to_string(
                processed_image,
                lang=self.ocr_language,
                config='--psm 1 --oem 3'
            )

            # Get metadata
            metadata = self._get_image_metadata(image, filename)

            return ProcessingResult(
                success=True,
                message="Image processed successfully",
                extracted_text=text,
                metadata=metadata
            )

        except Exception as e:
            return ProcessingResult(
                success=False,
                message="Image processing failed",
                error=str(e)
            )

    def _preprocess_image(self, image: Image.Image) -> Image.Image:
        """Preprocess image for better OCR results"""
        # Convert to RGB if needed
        if image.mode not in ('L', 'RGB'):
            image = image.convert('RGB')

        # Check and adjust resolution
        if hasattr(image, 'info') and 'dpi' in image.info:
            if min(image.info['dpi']) < self.min_quality:
                # Resize to improve quality
                scale = self.min_quality / min(image.info['dpi'])
                new_size = tuple(int(dim * scale) for dim in image.size)
                image = image.resize(new_size, Image.LANCZOS)

        return image

    def _get_image_metadata(self, image: Image.Image, filename: str) -> DocumentMetadata:
        return DocumentMetadata(
            file_name=filename,
            file_size=image.size[0] * image.size[1] * len(image.getbands()),
            mime_type=Image.MIME[image.format],
            page_count=1,
            word_count=None  # Will be updated after OCR
        )

    def set_ocr_language(self, language: str):
        """Set OCR language"""
        self.ocr_language = language

    def set_minimum_quality(self, dpi: int):
        """Set minimum DPI requirement"""
        self.min_quality = dpi