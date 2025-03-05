from typing import Tuple
from pathlib import Path
import filetype  # magic yerine filetype kullanacağız
from app.config import settings

def validate_file_type(content: bytes, filename: str) -> Tuple[bool, str]:
    """
    Validate file type using both extension and mime type
    Returns: (is_valid, error_message)
    """
    # Check file extension
    ext = Path(filename).suffix.lower().lstrip('.')
    if ext not in settings.ALLOWED_EXTENSIONS:
        return False, f"File type not allowed. Allowed types: {settings.ALLOWED_EXTENSIONS}"

    # Check mime type using filetype
    kind = filetype.guess(content)
    if kind is None:
        return False, "Could not determine file type"

    allowed_mimes = {
        'application/pdf',
        'image/jpeg',
        'image/png',
        'image/tiff'
    }
    
    if kind.mime not in allowed_mimes:
        return False, f"Invalid file type: {kind.mime}"

    return True, ""

def validate_file_size(content: bytes) -> Tuple[bool, str]:
    """
    Validate file size
    Returns: (is_valid, error_message)
    """
    if len(content) > settings.MAX_FILE_SIZE:
        return False, f"File size exceeds maximum limit of {settings.MAX_FILE_SIZE} bytes"
    return True, ""

def validate_text_content(text: str) -> Tuple[bool, str]:
    """
    Validate extracted text content
    Returns: (is_valid, error_message)
    """
    if not text.strip():
        return False, "No text content could be extracted"
    
    min_length = 10  # Minimum number of characters
    if len(text) < min_length:
        return False, f"Extracted text too short (minimum {min_length} characters)"
    
    return True, ""