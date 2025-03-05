import pytest
from fastapi.testclient import TestClient
from pathlib import Path
import os
from app.main import app
from app.config import settings

@pytest.fixture
def client():
    """Test client fixture"""
    return TestClient(app)

@pytest.fixture
def test_pdf():
    """Sample PDF file for testing"""
    current_dir = Path(__file__).parent
    return current_dir / "test_files" / "sample_contract.pdf"

@pytest.fixture
def test_image():
    """Sample image file for testing"""
    current_dir = Path(__file__).parent
    return current_dir / "test_files" / "sample_document.jpg"

@pytest.fixture
def sample_text():
    """Sample text content for testing"""
    return """
    EMPLOYMENT CONTRACT
    
    This employment contract is made between Company Ltd. and John Doe.
    
    1. Position: Software Developer
    2. Salary: €50,000 per annum
    3. Working Hours: 40 hours per week
    4. Annual Leave: 20 days
    5. Notice Period: 1 month
    
    The employee agrees to the terms and conditions stated above.
    """

@pytest.fixture
def mock_processor_result():
    """Mock processor result for testing"""
    from core.models import ProcessingResult, DocumentMetadata
    return ProcessingResult(
        success=True,
        message="Test processing completed",
        extracted_text="Sample text",
        metadata=DocumentMetadata(
            file_name="test.pdf",
            file_size=1000,
            mime_type="application/pdf"
        )
    )