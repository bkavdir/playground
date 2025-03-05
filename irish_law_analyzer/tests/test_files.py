from pathlib import Path

def test_sample_files_exist():
    """Test if sample files exist"""
    test_files_dir = Path(__file__).parent / "test_files"
    
    assert (test_files_dir / "sample_contract.pdf").exists(), "Sample contract PDF not found"
    assert (test_files_dir / "sample_letter.pdf").exists(), "Sample letter PDF not found"

def test_sample_files_readable():
    """Test if sample files are readable"""
    test_files_dir = Path(__file__).parent / "test_files"
    
    with open(test_files_dir / "sample_contract.pdf", "rb") as f:
        assert len(f.read()) > 0, "Sample contract PDF is empty"
    
    with open(test_files_dir / "sample_letter.pdf", "rb") as f:
        assert len(f.read()) > 0, "Sample letter PDF is empty"