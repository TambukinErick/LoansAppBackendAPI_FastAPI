from pydantic import BaseModel, Field
from typing import Optional
from enum import Enum
import datetime 

class TransactionStatus(str, Enum):
    ONGOING = "ONGOING"
    COMPLETED = "COMPLETED"
    DAMAGED = "DAMAGED"
    LOST = "LOST"




class Transaction(BaseModel):
    transactionId: int
    itemCat: str
    clientId: int
    loaningMemberName: str
    remarks: Optional[str] = Field(default=None)
    dateLoaned: datetime.datetime
    dueDate: datetime.datetime
    transactionStatus: TransactionStatus
    dateReturned: Optional[datetime.datetime]
    overdueDays: int = Field(default=0)
    overdueHours: int = Field(default=0)
    overdueMinutes: int = Field(default=0)
    recievingMemberName: Optional[str]
    returnRemarks: Optional[str] = Field(default=None)

class CreateTransaction(BaseModel):
    itemCat: str
    clientId: int
    loaningMemberName: str
    remarks: Optional[str] = Field(default=None)
    dateLoaned: datetime.datetime
    dueDate: datetime.datetime
    transactionStatus: TransactionStatus = TransactionStatus.ONGOING

class ReturnTransaction(BaseModel):
    itemCat: str
    clientId: int
    transactionStatus: TransactionStatus = TransactionStatus.COMPLETED
    dateReturned: datetime.datetime
    overdueDays: int = Field(default=0)
    overdueHours: int = Field(default=0)
    overDueMinutes: int = Field(default=0)
    recievingMemberName:  str
    returnRemarks:  Optional[str] = Field(default=None)

class ReportTransaction(BaseModel):
    itemCat: str
    clientId: int
    transactionStatus: TransactionStatus
    fineAmount: int = Field(default=0)





