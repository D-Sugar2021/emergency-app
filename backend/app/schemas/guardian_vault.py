from typing import List, Optional

from pydantic import BaseModel


class EmergencyContact(BaseModel):
    name: str
    phone: str
    relationship: str


class GuardianVaultData(BaseModel):
    emergency_contacts: List[EmergencyContact] = []
    allergies: Optional[str] = None
    medical_conditions: Optional[str] = None


class GuardianVault(GuardianVaultData):
    pass


class GuardianVaultCreate(GuardianVaultData):
    pass
