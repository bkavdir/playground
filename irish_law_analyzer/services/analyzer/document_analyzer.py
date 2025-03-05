from typing import Dict, List, Optional
from datetime import datetime
import time
from core.models import AnalysisResult, Finding, AnalysisConfig
from core.enums import RiskLevel, ProcessingStatus
from core.document_types import DocumentType, DocumentRequirements
from core.irish_law_rules import IrishEmploymentLaw
from ..classifier.document_classifier import DocumentClassifier
from .text_analyzer import TextAnalyzer
from app.config import settings

class DocumentAnalyzer:
    def __init__(self):
        self.text_analyzer = TextAnalyzer()
        self.document_classifier = DocumentClassifier()
        self.document_requirements = DocumentRequirements()
        self.irish_law = IrishEmploymentLaw()
        self.config = AnalysisConfig(
        risk_threshold_high=settings.RISK_THRESHOLD_HIGH,
        risk_threshold_medium=settings.RISK_THRESHOLD_MEDIUM,
        context_window_size=settings.CONTEXT_WINDOW_SIZE
)

    async def analyze_document(self, text: str, document_id: str) -> AnalysisResult:
        start_time = time.time()

        try:
            # Initialize result
            result = AnalysisResult(
                document_id=document_id,
                document_type=DocumentType.UNKNOWN,
                status=ProcessingStatus.PROCESSING
            )

            # Classify document
            doc_type = self.document_classifier.classify_document(text)
            result.document_type = doc_type

            # Perform text analysis
            text_analysis = self.text_analyzer.analyze(text, doc_type)
            result.findings.extend(text_analysis.findings)
            result.categories.update(text_analysis.categories)

            # Check document requirements
            requirements_validation = self.document_requirements.validate_document(doc_type, text)
            
            # Check legal compliance
            compliance_results = self.irish_law.check_compliance(doc_type.value.lower(), text)

            # Calculate risk score
            risk_score = self._calculate_risk_score(
                text_analysis.findings,
                requirements_validation,
                compliance_results
            )
            result.risk_score = risk_score

            # Set overall risk level
            result.overall_risk_level = self._determine_risk_level(risk_score)

            # Generate recommendations
            if self.config.include_recommendations:
                result.recommendations = self._generate_recommendations(
                    doc_type,
                    requirements_validation,
                    compliance_results
                )

            # Update metadata
            result.metadata.update({
                "processing_time": time.time() - start_time,
                "requirements_validation": requirements_validation,
                "compliance_results": compliance_results,
                "word_count": len(text.split()),
                "processed_at": datetime.now().isoformat()
            })

            result.status = ProcessingStatus.COMPLETED
            return result

        except Exception as e:
            result.status = ProcessingStatus.FAILED
            result.metadata["error"] = str(e)
            return result

    def _calculate_risk_score(
        self,
        findings: List[Finding],
        requirements_validation: Dict,
        compliance_results: Dict
    ) -> float:
        base_score = 0.0
        
        # Score from findings
        for finding in findings:
            risk_multiplier = {
                RiskLevel.HIGH.value: 3.0,
                RiskLevel.MEDIUM.value: 2.0,
                RiskLevel.LOW.value: 1.0
            }.get(finding.risk_level, 1.0)
            
            base_score += finding.occurrences * risk_multiplier

        # Score from requirements validation
        if not requirements_validation["is_valid"]:
            base_score += len(requirements_validation["missing_required_clauses"]) * 2.0
            base_score += len(requirements_validation["missing_recommended_clauses"]) * 1.0

        # Score from compliance
        if not compliance_results["compliant"]:
            base_score += len(compliance_results["missing_requirements"]) * 2.5

        # Normalize score to 1-10 range
        normalized_score = min(10.0, (base_score / 10.0) + 1.0)
        return round(normalized_score, 1)

    def _determine_risk_level(self, risk_score: float) -> RiskLevel:
        if risk_score > self.config.risk_threshold_high:
            return RiskLevel.HIGH
        elif risk_score > self.config.risk_threshold_medium:
            return RiskLevel.MEDIUM
        return RiskLevel.LOW

    def _generate_recommendations(
        self,
        doc_type: DocumentType,
        requirements_validation: Dict,
        compliance_results: Dict
    ) -> List[str]:
        recommendations = []

        # Add recommendations based on missing requirements
        for clause in requirements_validation.get("missing_required_clauses", []):
            recommendations.append(f"Add required clause: {clause}")

        for clause in requirements_validation.get("missing_recommended_clauses", []):
            recommendations.append(f"Consider adding recommended clause: {clause}")

        # Add recommendations based on compliance issues
        for requirement in compliance_results.get("missing_requirements", []):
            recommendations.append(
                f"Address compliance issue: {requirement['requirement']} "
                f"(Ref: {requirement['reference']})"
            )

        return recommendations

    def update_config(self, new_config: AnalysisConfig):
        """Update analyzer configuration"""
        self.config = new_config