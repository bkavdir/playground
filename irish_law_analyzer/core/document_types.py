from enum import Enum
from dataclasses import dataclass
from typing import List, Dict, Optional
from datetime import datetime
from dataclasses import dataclass, field

class DocumentType(Enum):
    EMPLOYMENT_CONTRACT = "EMPLOYMENT_CONTRACT"
    DISCIPLINARY_NOTICE = "DISCIPLINARY_NOTICE"
    TERMINATION_LETTER = "TERMINATION_LETTER"
    GRIEVANCE_LETTER = "GRIEVANCE_LETTER"
    WORKPLACE_POLICY = "WORKPLACE_POLICY"
    HEALTH_SAFETY = "HEALTH_SAFETY"
    UNKNOWN = "UNKNOWN"

@dataclass
class DocumentRequirement:
    required_clauses: List[str]
    recommended_clauses: List[str]
    risk_multiplier: float
    minimum_content_length: int
    maximum_content_length: Optional[int] = None
    required_sections: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    compliance_rules: List[str] = field(default_factory=list)

class DocumentRequirements:
    def __init__(self):
        self.requirements = {
            DocumentType.EMPLOYMENT_CONTRACT: DocumentRequirement(
                required_clauses=[
                    "job title",
                    "salary",
                    "working hours",
                    "annual leave",
                    "notice period",
                    "probation period"
                ],
                recommended_clauses=[
                    "grievance procedure",
                    "disciplinary procedure",
                    "sick leave",
                    "confidentiality"
                ],
                risk_multiplier=1.5,
                minimum_content_length=1000,
                maximum_content_length=10000,
                required_sections=[
                    "terms and conditions",
                    "compensation and benefits",
                    "working hours and leave",
                    "termination"
                ],
                keywords=[
                    "employment",
                    "contract",
                    "agreement",
                    "position",
                    "salary"
                ],
                compliance_rules=[
                    "must_include_minimum_wage",
                    "must_specify_working_hours",
                    "must_include_leave_entitlement"
                ]
            ),
            DocumentType.TERMINATION_LETTER: DocumentRequirement(
                required_clauses=[
                    "termination date",
                    "notice period",
                    "reason for termination",
                    "final payment details"
                ],
                recommended_clauses=[
                    "appeal rights",
                    "return of company property",
                    "reference provision"
                ],
                risk_multiplier=2.0,
                minimum_content_length=300,
                maximum_content_length=2000,
                required_sections=[
                    "notice of termination",
                    "reason for termination",
                    "final arrangements"
                ],
                keywords=[
                    "termination",
                    "dismissal",
                    "notice",
                    "effective date"
                ],
                compliance_rules=[
                    "must_specify_notice_period",
                    "must_include_appeal_rights",
                    "must_state_reason"
                ]
            )
        }

    def get_requirements(self, doc_type: DocumentType) -> DocumentRequirement:
        return self.requirements.get(doc_type, DocumentRequirement(
            required_clauses=[],
            recommended_clauses=[],
            risk_multiplier=1.0,
            minimum_content_length=0,
            maximum_content_length=None,
            required_sections=[],
            keywords=[],
            compliance_rules=[]
        ))

    def validate_document(self, doc_type: DocumentType, content: str) -> Dict:
        requirements = self.get_requirements(doc_type)
        validation_results = {
            "is_valid": True,
            "missing_required_clauses": [],
            "missing_recommended_clauses": [],
            "missing_sections": [],
            "content_length_valid": True,
            "compliance_issues": []
        }
        
        # Validate content length
        content_length = len(content)
        if content_length < requirements.minimum_content_length:
            validation_results["is_valid"] = False
            validation_results["content_length_valid"] = False
        
        if requirements.maximum_content_length and content_length > requirements.maximum_content_length:
            validation_results["content_length_valid"] = False

        # Check required clauses
        for clause in requirements.required_clauses:
            if clause.lower() not in content.lower():
                validation_results["is_valid"] = False
                validation_results["missing_required_clauses"].append(clause)

        # Check recommended clauses
        for clause in requirements.recommended_clauses:
            if clause.lower() not in content.lower():
                validation_results["missing_recommended_clauses"].append(clause)

        # Check required sections
        for section in requirements.required_sections:
            if section.lower() not in content.lower():
                validation_results["missing_sections"].append(section)

        return validation_results