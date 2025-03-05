from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    # Application Settings
    APP_NAME: str = "Irish Law Analyzer"
    APP_VERSION: str = "1.0.0"
    DEBUG: bool = True
    
    # File Processing Settings
    MAX_FILE_SIZE: int = 10 * 1024 * 1024  # 10MB
    ALLOWED_EXTENSIONS: set = {"pdf", "jpg", "jpeg", "png"}
    UPLOAD_FOLDER: str = "uploads"
    
    # OCR Settings
    OCR_LANGUAGE: str = "eng"
    OCR_DPI: int = 300
    
    # Analysis Settings
    RISK_THRESHOLD_HIGH: float = 7.0
    RISK_THRESHOLD_MEDIUM: float = 4.0
    CONTEXT_WINDOW_SIZE: int = 50
    
    # Path Settings
    BASE_DIR: Path = Path(__file__).resolve().parent.parent
    TEMPLATES_DIR: Path = BASE_DIR / "templates"
    STATIC_DIR: Path = BASE_DIR / "static"
    
    class Config:
        env_file = ".env"

settings = Settings()