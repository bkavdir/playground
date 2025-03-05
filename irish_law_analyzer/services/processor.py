from abc import ABC, abstractmethod
import pdfplumber
import pytesseract
from PIL import Image
from pdf2image import convert_from_bytes
import io

class DocumentProcessor(ABC):
    @abstractmethod
    def extract_text(self, file_bytes: bytes) -> str:
        pass

class PDFProcessor(DocumentProcessor):
    def extract_text(self, file_bytes: bytes) -> str:
        text = ""
        try:
            with pdfplumber.open(io.BytesIO(file_bytes)) as pdf:
                for page in pdf.pages:
                    text += page.extract_text() or ""

            if text.strip():
                return text

            images = convert_from_bytes(file_bytes)
            for image in images:
                text += pytesseract.image_to_string(image)

        except Exception as e:
            return f"Processing Error: {str(e)}"
        
        return text.strip()

class ImageProcessor(DocumentProcessor):
    def extract_text(self, file_bytes: bytes) -> str:
        try:
            image = Image.open(io.BytesIO(file_bytes))
            return pytesseract.image_to_string(image)
        except Exception as e:
            return f"Processing Error: {str(e)}"