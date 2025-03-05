from typing import Dict, Tuple, List
from core.document_types import DocumentType
import re
from collections import Counter

class DocumentClassifier:
    def __init__(self):
        self._initialize_patterns()

    def _initialize_patterns(self):
        self.patterns = {
            DocumentType.EMPLOYMENT_CONTRACT: {
                'keywords': [
                    'employment contract',
                    'contract of employment',
                    'terms and conditions',
                    'job description',
                    'position',
                    'salary',
                    'working hours'
                ],
                'weight': 1.5
            },
            DocumentType.TERMINATION_LETTER: {
                'keywords': [
                    'termination',
                    'dismissal',
                    'notice period',
                    'redundancy',
                    'end of employment'
                ],
                'weight': 1.3
            },
            DocumentType.DISCIPLINARY_NOTICE: {
                'keywords': [
                    'disciplinary',
                    'warning',
                    'misconduct',
                    'improvement required',
                    'performance issues'
                ],
                'weight': 1.2
            },
            DocumentType.WORKPLACE_POLICY: {
                'keywords': [
                    'policy',
                    'procedure',
                    'guidelines',
                    'handbook',
                    'rules'
                ],
                'weight': 1.0
            }
        }

    def classify_document(self, text: str) -> DocumentType:
        text = self._preprocess_text(text)
        
        # Calculate scores for each document type
        scores = self._calculate_scores(text)
        
        # Get the document type with highest score
        if scores:
            max_score_type = max(scores.items(), key=lambda x: x[1])[0]
            return max_score_type
        
        return DocumentType.UNKNOWN

    def _preprocess_text(self, text: str) -> str:
        """Preprocess text for classification"""
        # Convert to lowercase
        text = text.lower()
        
        # Remove extra whitespace
        text = ' '.join(text.split())
        
        # Remove special characters
        text = re.sub(r'[^\w\s]', '', text)
        
        return text

    def _calculate_scores(self, text: str) -> Dict[DocumentType, float]:
        scores = {}
        
        for doc_type, pattern_info in self.patterns.items():
            score = 0
            weight = pattern_info['weight']
            
            # Count keyword occurrences
            for keyword in pattern_info['keywords']:
                count = text.count(keyword)
                score += count * weight
            
            if score > 0:
                scores[doc_type] = score
        
        return scores

    def get_confidence_scores(self, text: str) -> Dict[DocumentType, float]:
        """Get confidence scores for all document types"""
        scores = self._calculate_scores(text)
        
        # Normalize scores
        total_score = sum(scores.values())
        if total_score > 0:
            return {
                doc_type: score / total_score
                for doc_type, score in scores.items()
            }
        
        return {DocumentType.UNKNOWN: 1.0}

    def analyze_structure(self, text: str) -> Dict:
        """Analyze document structure"""
        sections = text.split('\n\n')
        
        return {
            'section_count': len(sections),
            'average_section_length': sum(len(s) for s in sections) / len(sections) if sections else 0,
            'has_header': bool(re.match(r'^[A-Z\s]+$', sections[0].strip())) if sections else False,
            'has_signature_section': bool(re.search(r'sign|signature|dated', text.lower()))
        }