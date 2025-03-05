from dataclasses import dataclass, field
from typing import Dict, List, Optional
from datetime import datetime
from .enums import RiskLevel, ProcessingStatus, DocumentStatus
from .document_types import DocumentType
from dataclasses import dataclass, field

@dataclass
class KeywordInfo:
    risk: RiskLevel
    category: str
    description: str
    weight: float = 1.0
    requires_context: bool = False

@dataclass
class Finding:
    keyword: str
    risk_level: str
    category: str
    occurrences: int
    context: str = ""
    page_number: Optional[int] = None
    confidence: float = 1.0

@dataclass
class AnalysisResult:
    document_id: str
    document_type: DocumentType
    risk_score: float = 0.0
    findings: List[Finding] = field(default_factory=list)
    categories: Dict[str, List[Finding]] = field(default_factory=dict)
    overall_risk_level: RiskLevel = RiskLevel.LOW
    recommendations: List[str] = field(default_factory=list)
    processing_time: float = 0.0
    processed_at: datetime = field(default_factory=datetime.now)
    status: ProcessingStatus = ProcessingStatus.PENDING
    metadata: Dict = field(default_factory=dict)

@dataclass
class DocumentMetadata:
    file_name: str
    file_size: int
    mime_type: str
    page_count: Optional[int] = None
    created_at: datetime = field(default_factory=datetime.now)
    modified_at: datetime = field(default_factory=datetime.now)
    processed_at: Optional[datetime] = None
    processing_duration: Optional[float] = None
    word_count: Optional[int] = None
    language: Optional[str] = None

@dataclass
class ProcessingResult:
    success: bool
    message: str
    extracted_text: str = ""
    error: Optional[str] = None
    metadata: Optional[DocumentMetadata] = None
    processing_time: float = 0.0

@dataclass
class AnalysisConfig:
    risk_threshold_high: float = 7.0
    risk_threshold_medium: float = 4.0
    context_window_size: int = 50
    minimum_confidence: float = 0.6
    include_recommendations: bool = True
    detailed_analysis: bool = False
    max_findings: int = 100