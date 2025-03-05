import logging
from pathlib import Path
from datetime import datetime
import json
from typing import Any, Dict

class CustomLogger:
    def __init__(self, name: str = "irish_law_analyzer"):
        self.logger = logging.getLogger(name)
        self.setup_logger()

    def setup_logger(self):
        """Setup logger configuration"""
        # Create logs directory if it doesn't exist
        log_dir = Path(__file__).resolve().parent.parent / "logs"
        log_dir.mkdir(exist_ok=True)

        # Create handlers
        log_file = log_dir / f"{datetime.now().strftime('%Y%m%d')}.log"
        file_handler = logging.FileHandler(log_file)
        console_handler = logging.StreamHandler()

        # Create formatters and add it to handlers
        log_format = "%(asctime)s [%(levelname)s] %(message)s"
        file_handler.setFormatter(logging.Formatter(log_format))
        console_handler.setFormatter(logging.Formatter(log_format))

        # Add handlers to the logger
        self.logger.addHandler(file_handler)
        self.logger.addHandler(console_handler)
        self.logger.setLevel(logging.INFO)

    def log_analysis(self, document_id: str, analysis_result: Dict[str, Any]):
        """Log analysis results"""
        try:
            log_entry = {
                "document_id": document_id,
                "timestamp": datetime.now().isoformat(),
                "risk_score": analysis_result.get("risk_score"),
                "risk_level": analysis_result.get("overall_risk_level"),
                "findings_count": len(analysis_result.get("findings", [])),
            }
            self.logger.info(f"Analysis completed: {json.dumps(log_entry)}")
        except Exception as e:
            self.logger.error(f"Error logging analysis: {str(e)}")

    def log_error(self, error_type: str, error_message: str, extra_data: Dict = None):
        """Log error information"""
        try:
            log_entry = {
                "error_type": error_type,
                "error_message": error_message,
                "timestamp": datetime.now().isoformat()
            }
            if extra_data:
                log_entry["extra_data"] = extra_data
            self.logger.error(f"Error occurred: {json.dumps(log_entry)}")
        except Exception as e:
            self.logger.error(f"Error logging error: {str(e)}")

logger = CustomLogger()