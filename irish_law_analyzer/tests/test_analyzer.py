import pytest
from services.analyzer.document_analyzer import DocumentAnalyzer
from services.analyzer.text_analyzer import TextAnalyzer
from core.models import AnalysisResult
from core.document_types import DocumentType
from core.enums import RiskLevel

class TestDocumentAnalyzer:
    def setup_method(self):
        self.analyzer = DocumentAnalyzer()

    async def test_analyze_document(self, sample_text):
        result = await self.analyzer.analyze_document(sample_text, "test_doc")
        
        assert isinstance(result, AnalysisResult)
        assert result.document_type in DocumentType
        assert isinstance(result.risk_score, float)
        assert result.risk_score >= 0 and result.risk_score <= 10
        assert result.overall_risk_level in RiskLevel
        assert isinstance(result.findings, list)
        assert isinstance(result.recommendations, list)

    async def test_analyze_empty_document(self):
        result = await self.analyzer.analyze_document("", "test_doc")
        assert result.risk_score == 1.0
        assert result.overall_risk_level == RiskLevel.LOW
        assert len(result.findings) == 0

class TestTextAnalyzer:
    def setup_method(self):
        self.analyzer = TextAnalyzer()

    def test_analyze_text(self, sample_text):
        result = self.analyzer.analyze(sample_text, DocumentType.EMPLOYMENT_CONTRACT)
        
        assert isinstance(result, AnalysisResult)
        assert len(result.findings) > 0
        assert "salary" in [f.keyword.lower() for f in result.findings]
        assert "working hours" in [f.keyword.lower() for f in result.findings]

    def test_context_extraction(self):
        text = "This is a test sentence with salary information."
        result = self.analyzer.analyze(text, DocumentType.EMPLOYMENT_CONTRACT)
        
        salary_findings = [f for f in result.findings if f.keyword.lower() == "salary"]
        if salary_findings:
            assert "test sentence with salary information" in salary_findings[0].context