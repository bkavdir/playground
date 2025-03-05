from dataclasses import dataclass, field
from typing import List, Dict, Optional
from datetime import datetime
from enum import Enum

class LawCategory(Enum):
    EMPLOYMENT = "EMPLOYMENT"
    HEALTH_SAFETY = "HEALTH_SAFETY"
    DISCRIMINATION = "DISCRIMINATION"
    TERMINATION = "TERMINATION"
    WORKING_TIME = "WORKING_TIME"
    PARENTAL = "PARENTAL"

@dataclass
class LegalReference:
    act: str
    section: str
    description: str
    url: Optional[str] = None
    effective_date: datetime = field(default_factory=datetime.now)
    last_amended: Optional[datetime] = None

@dataclass
class LegalRequirement:
    description: str
    references: List[LegalReference] = field(default_factory=list)
    is_mandatory: bool = True
    applicable_from: datetime = field(default_factory=datetime.now)
    penalties: Optional[str] = None
    category: LawCategory = LawCategory.EMPLOYMENT
    compliance_checklist: List[str] = field(default_factory=list)

class IrishEmploymentLaw:
    def __init__(self):
        self._initialize_acts()
        self._initialize_requirements()

    def _initialize_acts(self):
        self.acts: Dict[str, str] = {
            "UNFAIR_DISMISSALS": "Unfair Dismissals Acts 1977-2015",
            "EMPLOYMENT_EQUALITY": "Employment Equality Acts 1998-2015",
            "ORGANISATION_OF_TIME": "Organisation of Working Time Act 1997",
            "TERMS_OF_EMPLOYMENT": "Terms of Employment (Information) Acts 1994-2014",
            "MINIMUM_WAGE": "National Minimum Wage Act 2000",
            "PARENTAL_LEAVE": "Parental Leave Acts 1998-2019",
            "PROTECTION_OF_EMPLOYMENT": "Protection of Employment Acts 1977-2007",
            "PAYMENT_OF_WAGES": "Payment of Wages Act 1991"
        }

    def _initialize_requirements(self):
        self.requirements: Dict[str, List[LegalRequirement]] = {
            "employment_contract": [
                LegalRequirement(
                    description="Written statement of terms of employment",
                    references=[
                        LegalReference(
                            act=self.acts["TERMS_OF_EMPLOYMENT"],
                            section="Section 3",
                            description="Obligation to provide written statement",
                            url="http://www.irishstatutebook.ie/eli/1994/act/5/section/3",
                            effective_date=datetime(1994, 5, 16)
                        )
                    ],
                    is_mandatory=True,
                    applicable_from=datetime(1994, 5, 16),
                    penalties="Up to 4 weeks' remuneration",
                    category=LawCategory.EMPLOYMENT,
                    compliance_checklist=[
                        "Document must be provided within 2 months",
                        "Must include all statutory terms",
                        "Must be signed by employer"
                    ]
                )
            ],
            "termination": [
                LegalRequirement(
                    description="Minimum notice periods",
                    references=[
                        LegalReference(
                            act="Minimum Notice and Terms of Employment Act 1973",
                            section="Section 4",
                            description="Minimum notice requirements",
                            url="http://www.irishstatutebook.ie/eli/1973/act/4/section/4",
                            effective_date=datetime(1973, 1, 1)
                        )
                    ],
                    is_mandatory=True,
                    applicable_from=datetime(1973, 1, 1),
                    penalties="Up to 2 years' remuneration",
                    category=LawCategory.TERMINATION,
                    compliance_checklist=[
                        "Check length of service",
                        "Verify notice period calculation",
                        "Ensure proper notice delivery"
                    ]
                )
            ]
        }

    def get_requirements_for_document(self, doc_type: str) -> List[LegalRequirement]:
        return self.requirements.get(doc_type, [])

    def validate_notice_period(self, years_of_service: float) -> Dict[str, str]:
        notice_periods = {
            "less_than_2": "1 week",
            "2_to_5": "2 weeks",
            "5_to_10": "4 weeks",
            "10_to_15": "6 weeks",
            "more_than_15": "8 weeks"
        }

        if years_of_service < 2:
            return {"required_notice": notice_periods["less_than_2"]}
        elif years_of_service < 5:
            return {"required_notice": notice_periods["2_to_5"]}
        elif years_of_service < 10:
            return {"required_notice": notice_periods["5_to_10"]}
        elif years_of_service < 15:
            return {"required_notice": notice_periods["10_to_15"]}
        else:
            return {"required_notice": notice_periods["more_than_15"]}

    def check_compliance(self, doc_type: str, content: str) -> Dict:
        requirements = self.get_requirements_for_document(doc_type)
        compliance_results = {
            "compliant": True,
            "missing_requirements": [],
            "recommendations": [],
            "legal_references": [],
            "risk_areas": [],
            "compliance_score": 100.0
        }
        
        for requirement in requirements:
            requirement_met = False
            for checklist_item in requirement.compliance_checklist:
                if not self._check_requirement(content, checklist_item):
                    compliance_results["missing_requirements"].append({
                        "requirement": requirement.description,
                        "checklist_item": checklist_item,
                        "reference": requirement.references[0].act if requirement.references else None
                    })
                    requirement_met = False
                    break
                requirement_met = True

            if not requirement_met:
                compliance_results["compliant"] = False
                compliance_results["compliance_score"] -= (100.0 / len(requirements))

            compliance_results["legal_references"].extend([
                {
                    "act": ref.act,
                    "section": ref.section,
                    "description": ref.description,
                    "url": ref.url
                } for ref in requirement.references
            ])

        compliance_results["compliance_score"] = max(0.0, compliance_results["compliance_score"])
        return compliance_results

    def _check_requirement(self, content: str, requirement: str) -> bool:
        # Basic implementation - can be enhanced with more sophisticated checking
        return requirement.lower() in content.lower()

    def get_relevant_acts(self, doc_type: str) -> List[str]:
        requirements = self.get_requirements_for_document(doc_type)
        acts = set()
        for requirement in requirements:
            for reference in requirement.references:
                acts.add(reference.act)
        return list(acts)