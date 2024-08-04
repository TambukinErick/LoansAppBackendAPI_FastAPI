from pydantic import BaseModel, Field
from typing import Optional
import datetime 

class Client(BaseModel):
    clientId: int
    lastName: str
    firstName: str
    middleInitial: Optional[str] = None
    suffix: Optional[str] = None
    contactNum: str
    email: str
    yearLevel: int = Field(default=1, ge=1)
    course: str

    hasWednesdayClasses: bool = Field(default=False)
    graduating: bool = Field(default=False)
    registeringMemberName: str
    regDate: datetime.datetime

    borrowing: bool = Field(default=False)
    blackListed: bool = Field(default=False)
    tempBlackList: bool = Field(default=False)
    holdOrder: bool = Field(default=False)
    excuseLetter: bool = Field(default=False)
    fineAmount: int = Field(default=0)

    warningCount: int = Field(default=0, ge=0)
    borrowCount: int = Field(default=0, ge=0)

    class Config:
        orm_mode = True

class CreateClient(BaseModel):
    clientId: int
    lastName: str
    firstName: str
    middleInitial: Optional[str] = None
    suffix: Optional[str] = None
    contactNum: str
    email: str
    yearLevel: int = Field(default=1, ge=1)
    course: str

    hasWednesdayClasses: bool = Field(default=False)
    graduating: bool = Field(default=False)
    registeringMemberName: str
    regDate: datetime.datetime

class UpdateClientDetails(BaseModel):
    lastName: str
    firstName: str
    middleInitial: Optional[str] = None
    suffix: Optional[str] = None
    contactNum: str
    email: str
    yearLevel: int = Field(default=1, ge=1)
    course: str
    hasWednesdayClasses: bool = Field(default=False)
    graduating: bool = Field(default=False)

class SetClientPenalty(BaseModel):
    blackListed: bool = Field(default=False)
    tempBlackList: bool = Field(default=False)
    holdOrder: bool = Field(default=False)
    excuseLetter: bool = Field(default=False)
    fineAmount: int = Field(default=0)
    warningCount: int = Field(default=0, ge=0)