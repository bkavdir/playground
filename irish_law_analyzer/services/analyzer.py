from core.models import Finding, AnalysisResult
from core.enums import RiskLevel
from .keyword_db import KeywordDatabase

class DocumentAnalyzer:
    def __init__(self):
        self.keyword_db = KeywordDatabase()

    def _get_context(self, text: str, keyword: str, window: int = 50) -> str:
        index = text.lower().find(keyword.lower())
        if index == -1:
            return ""
        start = max(0, index - window)
        end = min(len(text), index + len(keyword) + window)
        return f"...{text[start:end]}..."

    def analyze_text(self, text: str) -> AnalysisResult:
        text = text.lower()
        result = AnalysisResult()
        
        sentences = text.split('.')
        
        for keyword, info in self.keyword_db.keywords.items():
            exact_count = text.count(keyword)
            partial_matches = sum(1 for sentence in sentences if keyword in sentence)
            
            if exact_count > 0 or partial_matches > 0:
                count = max(exact_count, partial_matches)
                
                finding = Finding(
                    keyword=keyword,
                    risk_level=info.risk.value,
                    category=info.category,
                    occurrences=count,
                    context=self._get_context(text, keyword)
                )
                result.findings.append(finding)
                
                if info.category not in result.categories:
                    result.categories[info.category] = []
                result.categories[info.category].append(finding)
        
        total_score = 0
        for finding in result.findings:
            base_score = finding.occurrences * {
                RiskLevel.HIGH.value: 5,
                RiskLevel.MEDIUM.value: 3,
                RiskLevel.LOW.value: 1
            }.get(finding.risk_level, 1)
            
            if len(finding.context) > 100:
                base_score *= 1.2
            
            total_score += base_score
        
        result.risk_score = min(10, (total_score / 8) + 1) if total_score > 0 else 1
        
        result.overall_risk_level = (
            RiskLevel.HIGH if result.risk_score > 7
            else RiskLevel.MEDIUM if result.risk_score > 4
            else RiskLevel.LOW
        )
        
        return result