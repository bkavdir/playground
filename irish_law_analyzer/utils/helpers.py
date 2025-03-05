import os
from datetime import datetime
from typing import Dict, Any
import hashlib
from pathlib import Path

def generate_document_id(filename: str, content: bytes) -> str:
    """Generate unique document ID based on content and timestamp"""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    content_hash = hashlib.md5(content).hexdigest()[:10]
    return f"{timestamp}_{content_hash}"

def create_temp_file_path(filename: str, folder: str = "uploads") -> Path:
    """Create temporary file path for uploaded documents"""
    base_dir = Path(__file__).resolve().parent.parent
    uploads_dir = base_dir / folder
    
    # Create directory if it doesn't exist
    uploads_dir.mkdir(exist_ok=True)
    
    # Generate unique filename
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    unique_filename = f"{timestamp}_{filename}"
    
    return uploads_dir / unique_filename

def cleanup_old_files(folder: str = "uploads", max_age_hours: int = 24):
    """Clean up old temporary files"""
    base_dir = Path(__file__).resolve().parent.parent
    folder_path = base_dir / folder
    
    if not folder_path.exists():
        return
    
    current_time = datetime.now()
    for file_path in folder_path.glob('*'):
        if file_path.name == '.gitkeep':
            continue
            
        file_age = current_time - datetime.fromtimestamp(file_path.stat().st_mtime)
        if file_age.total_seconds() > (max_age_hours * 3600):
            try:
                file_path.unlink()
            except Exception as e:
                print(f"Error deleting {file_path}: {e}")

def format_file_size(size_in_bytes: int) -> str:
    """Format file size in human readable format"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_in_bytes < 1024:
            return f"{size_in_bytes:.2f} {unit}"
        size_in_bytes /= 1024
    return f"{size_in_bytes:.2f} TB"

def extract_metadata(file_path: Path) -> Dict[str, Any]:
    """Extract metadata from file"""
    stats = file_path.stat()
    return {
        "filename": file_path.name,
        "size": format_file_size(stats.st_size),
        "created": datetime.fromtimestamp(stats.st_ctime).isoformat(),
        "modified": datetime.fromtimestamp(stats.st_mtime).isoformat(),
        "extension": file_path.suffix.lower()
    }