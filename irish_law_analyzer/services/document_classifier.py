from enum import Enum
import magic  # pip install python-magic
import re

class DocumentType(Enum):
    EMPLOYMENT_CONTRACT = "EMPLOYMENT_CONTRACT"
    DISCIPLINARY_NOTICE = "DISCIPLINARY_NOTICE"
    TERMINATION_LETTER = "TERMINATION_LETTER"
    GENERAL_POLICY = "GENERAL_POLICY"
    UNKNOWN = "UNKNOWN"

class DocumentClassifier:
    def __init__(self):
        self.document_patterns = {
            DocumentType.EMPLOYMENT_CONTRACT: [
                r'employment\s+contract',
                r'contract\s+of\s+employment',
                r'terms\s+and\s+conditions\s+of\s+employment'
            ],
            DocumentType.DISCIPLINARY_NOTICE: [
                r'disciplinary\s+notice',
                r'warning\s+letter',
                r'misconduct'
            ],
            DocumentType.TERMINATION_LETTER: [
                r'termination\s+of\s+employment',
                r'notice\s+of\s+dismissal',
                r'redundancy\s+notice'
            ],
            DocumentType.GENERAL_POLICY: [
                r'company\s+policy',
                r'workplace\s+policy',
                r'handbook'
            ]
        }

    def classify_document(self, text: str) -> DocumentType:
        text = text.lower()
        
        for doc_type, patterns in self.document_patterns.items():
            for pattern in patterns:
                if re.search(pattern, text):
                    return doc_type
        
        return DocumentType.UNKNOWN

    def get_mime_type(self, file_bytes: bytes) -> str:
        return magic.from_buffer(file_bytes, mime=True)