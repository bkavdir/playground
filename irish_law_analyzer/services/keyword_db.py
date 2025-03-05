from typing import Optional
from core.models import KeywordInfo
from core.enums import RiskLevel

class KeywordDatabase:
    def __init__(self):
        self.keywords = {
            # High Risk Keywords
            'termination': KeywordInfo(
                risk=RiskLevel.HIGH,
                category='Employment Termination',
                description='Indicates potential employment termination issues'
            ),
            'dismissal': KeywordInfo(
                risk=RiskLevel.HIGH,
                category='Employment Termination',
                description='Related to employee dismissal'
            ),
            'redundancy': KeywordInfo(
                risk=RiskLevel.HIGH,
                category='Employment Termination',
                description='Related to redundancy situations'
            ),
            'discrimination': KeywordInfo(
                risk=RiskLevel.HIGH,
                category='Discrimination',
                description='Potential discrimination issues'
            ),
            # Medium Risk Keywords
            'salary': KeywordInfo(
                risk=RiskLevel.MEDIUM,
                category='Compensation',
                description='Salary-related terms'
            ),
            'overtime': KeywordInfo(
                risk=RiskLevel.MEDIUM,
                category='Working Hours',
                description='Overtime arrangements'
            ),
            # Low Risk Keywords
            'annual leave': KeywordInfo(
                risk=RiskLevel.LOW,
                category='Leave',
                description='Annual leave arrangements'
            ),
            'working hours': KeywordInfo(
                risk=RiskLevel.LOW,
                category='Working Time',
                description='Working hours arrangements'
            ),
        }

    def get_keyword_info(self, keyword: str) -> Optional[KeywordInfo]:
        return self.keywords.get(keyword.lower())