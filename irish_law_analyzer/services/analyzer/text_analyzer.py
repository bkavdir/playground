from typing import Dict, List, Optional
from core.models import Finding, AnalysisResult
from core.document_types import DocumentType
import re

class TextAnalyzer:
    def __init__(self):
        self.context_window = 50
        self.sentence_end_pattern = re.compile(r'[.!?]+')

    def analyze(self, text: str, doc_type: DocumentType) -> AnalysisResult:
        result = AnalysisResult(
            document_id="",  # Will be set by DocumentAnalyzer
            document_type=doc_type
        )

        # Normalize text
        normalized_text = self._normalize_text(text)
        
        # Split into sentences
        sentences = self._split_into_sentences(normalized_text)
        
        # Analyze patterns
        self._analyze_patterns(normalized_text, sentences, result)
        
        # Categorize findings
        self._categorize_findings(result)
        
        return result

    def _normalize_text(self, text: str) -> str:
        """Normalize text for analysis"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Remove special characters (keeping punctuation)
        text = re.sub(r'[^\w\s.!?,;:-]', '', text)
        
        return text

    def _split_into_sentences(self, text: str) -> List[str]:
        """Split text into sentences"""
        sentences = self.sentence_end_pattern.split(text)
        return [s.strip() for s in sentences if s.strip()]

    def _analyze_patterns(self, text: str, sentences: List[str], result: AnalysisResult):
        """Analyze text patterns and update result"""
        # Analyze legal references
        self._find_legal_references(text, result)
        
        # Analyze dates and deadlines
        self._find_dates_and_deadlines(text, result)
        
        # Analyze monetary values
        self._find_monetary_values(text, result)
        
        # Analyze specific clauses
        self._analyze_clauses(sentences, result)

    def _find_legal_references(self, text: str, result: AnalysisResult):
        """Find legal references in text"""
        legal_patterns = [
            r'section\s+\d+',
            r'article\s+\d+',
            r'act\s+of\s+\d{4}',
            r'regulation\s+\d+'
        ]
        
        for pattern in legal_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                result.findings.append(Finding(
                    keyword=match.group(),
                    risk_level="MEDIUM",
                    category="Legal References",
                    occurrences=1,
                    context=self._get_context(text, match.start(), match.end())
                ))

    def _find_dates_and_deadlines(self, text: str, result: AnalysisResult):
        """Find dates and deadlines in text"""
        date_patterns = [
            r'\d{1,2}/\d{1,2}/\d{4}',
            r'\d{1,2}-\d{1,2}-\d{4}',
            r'\d{1,2}\s+(?:january|february|march|april|may|june|july|august|september|october|november|december)\s+\d{4}'
        ]
        
        for pattern in date_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                result.findings.append(Finding(
                    keyword=match.group(),
                    risk_level="LOW",
                    category="Dates and Deadlines",
                    occurrences=1,
                    context=self._get_context(text, match.start(), match.end())
                ))

    def _find_monetary_values(self, text: str, result: AnalysisResult):
        """Find monetary values in text"""
        money_patterns = [
            r'€\s*\d+(?:,\d{3})*(?:\.\d{2})?',
            r'eur\s*\d+(?:,\d{3})*(?:\.\d{2})?',
            r'\d+(?:,\d{3})*(?:\.\d{2})?\s*euros?'
        ]
        
        for pattern in money_patterns:
            matches = re.finditer(pattern, text)
            for match in matches:
                result.findings.append(Finding(
                    keyword=match.group(),
                    risk_level="MEDIUM",
                    category="Monetary Values",
                    occurrences=1,
                    context=self._get_context(text, match.start(), match.end())
                ))

    def _analyze_clauses(self, sentences: List[str], result: AnalysisResult):
        """Analyze specific clauses in the document"""
        clause_indicators = [
            "hereby agrees",
            "shall be",
            "must",
            "will not",
            "is prohibited",
            "is required"
        ]
        
        for i, sentence in enumerate(sentences):
            for indicator in clause_indicators:
                if indicator in sentence:
                    result.findings.append(Finding(
                        keyword=indicator,
                        risk_level="LOW",
                        category="Contractual Clauses",
                        occurrences=1,
                        context=sentence
                    ))

    def _get_context(self, text: str, start: int, end: int) -> str:
        """Get context around a matched pattern"""
        context_start = max(0, start - self.context_window)
        context_end = min(len(text), end + self.context_window)
        return f"...{text[context_start:context_end]}..."

    def _categorize_findings(self, result: AnalysisResult):
        """Categorize findings by type"""
        categories: Dict[str, List[Finding]] = {}
        
        for finding in result.findings:
            if finding.category not in categories:
                categories[finding.category] = []
            categories[finding.category].append(finding)
        
        result.categories = categories