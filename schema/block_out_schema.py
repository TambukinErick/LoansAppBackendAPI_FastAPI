from pydantic import BaseModel, Field, field_validator
from typing import Optional
import datetime

class BlockOutDate(BaseModel):
    dateBlocked: datetime.date
    remarks: Optional[str] = Field(None, max_length=255)

class BlockOutTime(BaseModel):
    dateBlocked: datetime.date
    startTime: datetime.datetime
    endTime: datetime.datetime
    remarks: Optional[str] = Field(None, max_length=255)
