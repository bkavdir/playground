from dataclasses import dataclass
from typing import Dict, List
from .enums import RiskLevel

@dataclass
class KeywordInfo:
    risk: RiskLevel
    category: str
    description: str

@dataclass
class Finding:
    keyword: str
    risk_level: str
    category: str
    occurrences: int
    context: str = ""

class AnalysisResult:
    def __init__(self):
        self.risk_score: float = 0
        self.findings: List[Finding] = []
        self.categories: Dict[str, List[Finding]] = {}
        self.overall_risk_level: RiskLevel = RiskLevel.LOW
        self.recommendations: List[str] = []