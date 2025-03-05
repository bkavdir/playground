import pytest
from services.processor.pdf_processor import PDFProcessor
from services.processor.image_processor import ImageProcessor
from core.models import ProcessingResult

class TestPDFProcessor:
    def setup_method(self):
        self.processor = PDFProcessor()

    def test_initialization(self):
        assert self.processor.supported_mime_types == {'application/pdf'}
        assert self.processor.dpi == 300
        assert self.processor.ocr_language == 'eng'

    def test_process_valid_pdf(self, test_pdf):
        with open(test_pdf, 'rb') as f:
            result = self.processor.process_document(f.read(), "test.pdf")
        
        assert isinstance(result, ProcessingResult)
        assert result.success
        assert result.extracted_text
        assert not result.error

    def test_process_invalid_file(self):
        result = self.processor.process_document(b"invalid data", "test.pdf")
        assert not result.success
        assert result.error

class TestImageProcessor:
    def setup_method(self):
        self.processor = ImageProcessor()

    def test_initialization(self):
        assert 'image/jpeg' in self.processor.supported_mime_types
        assert 'image/png' in self.processor.supported_mime_types
        assert self.processor.ocr_language == 'eng'

    def test_process_valid_image(self, test_image):
        with open(test_image, 'rb') as f:
            result = self.processor.process_document(f.read(), "test.jpg")
        
        assert isinstance(result, ProcessingResult)
        assert result.success
        assert result.extracted_text
        assert not result.error

    def test_process_invalid_image(self):
        result = self.processor.process_document(b"invalid data", "test.jpg")
        assert not result.success
        assert result.error