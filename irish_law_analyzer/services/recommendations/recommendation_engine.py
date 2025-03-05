from typing import List, Dict
from core.document_types import DocumentType
from core.models import Finding
from core.irish_law_rules import IrishEmploymentLaw

class RecommendationEngine:
    def __init__(self):
        self.irish_law = IrishEmploymentLaw()
        self._initialize_recommendation_templates()

    def _initialize_recommendation_templates(self):
        self.templates = {
            DocumentType.EMPLOYMENT_CONTRACT: {
                'missing_clause': "Add missing clause for: {clause}",
                'risk_high': "High risk identified in section: {section}",
                'compliance': "Ensure compliance with {act} regarding {topic}",
                'improvement': "Consider improving clarity of {section}"
            },
            DocumentType.TERMINATION_LETTER: {
                'missing_clause': "Include required information about: {clause}",
                'notice_period': "Verify notice period complies with minimum requirement: {period}",
                'appeal_rights': "Ensure appeal rights are clearly stated",
                'final_payments': "Include details about final payments and timing"
            }
        }

    def generate_recommendations(
        self,
        doc_type: DocumentType,
        findings: List[Finding],
        compliance_results: Dict,
        requirements_validation: Dict
    ) -> List[str]:
        recommendations = []

        # Add type-specific recommendations
        type_recommendations = self._get_type_specific_recommendations(
            doc_type,
            requirements_validation
        )
        recommendations.extend(type_recommendations)

        # Add risk-based recommendations
        risk_recommendations = self._get_risk_based_recommendations(findings)
        recommendations.extend(risk_recommendations)

        # Add compliance recommendations
        compliance_recommendations = self._get_compliance_recommendations(
            doc_type,
            compliance_results
        )
        recommendations.extend(compliance_recommendations)

        # Prioritize and deduplicate recommendations
        return self._prioritize_recommendations(recommendations)

    def _get_type_specific_recommendations(
        self,
        doc_type: DocumentType,
        requirements_validation: Dict
    ) -> List[str]:
        recommendations = []
        templates = self.templates.get(doc_type, {})

        for clause in requirements_validation.get("missing_required_clauses", []):
            if 'missing_clause' in templates:
                recommendations.append(
                    templates['missing_clause'].format(clause=clause)
                )

        return recommendations

    def _get_risk_based_recommendations(self, findings: List[Finding]) -> List[str]:
        recommendations = []
        
        for finding in findings:
            if finding.risk_level == "HIGH":
                recommendations.append(
                    f"Address high-risk issue in '{finding.category}': {finding.keyword}"
                )
            elif finding.risk_level == "MEDIUM":
                recommendations.append(
                    f"Review potential issue in '{finding.category}': {finding.keyword}"
                )

        return recommendations

    def _get_compliance_recommendations(
        self,
        doc_type: DocumentType,
        compliance_results: Dict
    ) -> List[str]:
        recommendations = []

        for requirement in compliance_results.get("missing_requirements", []):
            recommendations.append(
                f"Ensure compliance with {requirement['reference']}: "
                f"{requirement['requirement']}"
            )

        return recommendations

    def _prioritize_recommendations(self, recommendations: List[str]) -> List[str]:
        # Remove duplicates while preserving order
        unique_recommendations = list(dict.fromkeys(recommendations))
        
        # Sort by priority (assuming recommendations starting with certain
        # keywords are more important)
        priority_order = ["Ensure compliance", "Address high-risk", "Include required", "Review potential", "Consider"]
        
        def get_priority(rec):
            for i, priority in enumerate(priority_order):
                if rec.startswith(priority):
                    return i
            return len(priority_order)

        return sorted(unique_recommendations, key=get_priority)