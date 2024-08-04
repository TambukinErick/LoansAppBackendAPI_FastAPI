from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
import datetime 

class LoanItemStatus(str, Enum):
    INSTORAGE = 'INSTORAGE'
    LOANEDOUT = 'LOANEDOUT'
    DAMAGED = 'DAMAGED'
    LOST = 'LOST'

class LoanItem(BaseModel):
    itemCat: str
    status: LoanItemStatus
    description: Optional[str]
    dateReg: datetime.datetime

    class Config:
        orm_mode = True

class CreateLoanItem(BaseModel):
    itemCat: str
    status: LoanItemStatus = LoanItemStatus.INSTORAGE
    description: Optional[str]
    dateReg: datetime.datetime

    class Config:
        orm_mode = True

class UpdateLoanItem(BaseModel):
    status: LoanItemStatus
    description: Optional[str]