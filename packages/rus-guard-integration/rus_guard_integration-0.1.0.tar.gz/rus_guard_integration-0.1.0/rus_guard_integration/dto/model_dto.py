from datetime import datetime
from typing import List

from pydantic import BaseModel


class RusGuardEmployeeDto:
    class Create(BaseModel):
        rus_guard_group_guid: str
        LastName: str
        FirstName: str | None = None
        SecondName: str | None = None
        Comment: str | None = None
        IsLocked: bool | None = None
        Number: int | None = None
        Authority: str | None = None
        DateOfIssue: datetime | None = None
        PINCode: int | None = None
        PINCodeDescription: str | None = None
        PINCodeUnderPressure: int | None = None
        PINCodeUnderPressureDescription: str | None = None
        PassportIssue: str | None = None
        PassportNumber: str | None = None
        ResidentialAddress: str | None = None
        EmployeePositionID: str | None = None
        IsChangeLocked: bool | None = None
        IsChangePin: bool | None = None

    class Update(BaseModel):
        LastName: str | None
        FirstName: str | None
        SecondName: str | None
        Comment: str | None
        IsLocked: bool | None
        Number: int | None
        Authority: str | None
        DateOfIssue: datetime | None
        PINCode: int | None
        PINCodeDescription: str | None
        PINCodeUnderPressure: int | None
        PINCodeUnderPressureDescription: str | None
        PassportIssue: str | None
        PassportNumber: str | None
        ResidentialAddress: str | None
        EmployeePositionID: str | None
        IsChangeLocked: bool | None
        IsChangePin: bool | None



class AcsAccessLevelDto:
    class Create(BaseModel):
        Name: str | None
        Description: str | None
        tagIDs: list[str] | None = None

    class Update(BaseModel):
        # Id: str
        Name: str | None
        Description: str | None
        tagIDs: list[str] | None = None
