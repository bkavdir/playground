from abc import ABC, abstractmethod
from typing import Optional
from core.models import ProcessingResult, DocumentMetadata
import time

class BaseDocumentProcessor(ABC):
    def __init__(self):
        self.supported_mime_types: set = set()
        self.max_file_size: int = 10 * 1024 * 1024  # 10MB default

    @abstractmethod
    def extract_text(self, file_bytes: bytes, filename: str) -> ProcessingResult:
        pass

    def process_document(self, file_bytes: bytes, filename: str) -> ProcessingResult:
        start_time = time.time()
        
        try:
            # Check file size
            if len(file_bytes) > self.max_file_size:
                return ProcessingResult(
                    success=False,
                    message="File size exceeds maximum limit",
                    error="FILE_TOO_LARGE"
                )

            # Process the document
            result = self.extract_text(file_bytes, filename)
            
            # Add processing time
            result.processing_time = time.time() - start_time
            
            return result

        except Exception as e:
            return ProcessingResult(
                success=False,
                message="Processing failed",
                error=str(e),
                processing_time=time.time() - start_time
            )

    def get_metadata(self, file_bytes: bytes, filename: str) -> Optional[DocumentMetadata]:
        """Extract metadata from document"""
        try:
            return DocumentMetadata(
                file_name=filename,
                file_size=len(file_bytes),
                mime_type=self._get_mime_type(file_bytes)
            )
        except Exception:
            return None

    def _get_mime_type(self, file_bytes: bytes) -> str:
        """Determine MIME type of file"""
        import magic
        return magic.from_buffer(file_bytes, mime=True)

    def is_supported_type(self, mime_type: str) -> bool:
        return mime_type in self.supported_mime_types