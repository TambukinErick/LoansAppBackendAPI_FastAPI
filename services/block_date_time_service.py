from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..repository.block_date_time_repository import BlockOutRepository
from ..schema.block_out_schema import *

class BlockOutService:
    def __init__(self, session: Session):
        self.repository = BlockOutRepository(session)
    
    def create_block_out_date(self, data: BlockOutDate) -> BlockOutDate:
        if self.repository.block_out_date_exists(data.dateBlocked):
            raise HTTPException(status_code=400, detail="Date Already Blocked")
        block_out_date = self.repository.create_block_out_date(data)
        return block_out_date
    
    def create_block_out_time(self, data: BlockOutTime) -> BlockOutTime:
        if self.repository.block_out_time_exists(data.dateBlocked):
            raise HTTPException(status_code=400, detail="Date Already Blocked")
        block_out_time = self.repository.create_block_out_time(data)
        return block_out_time
    
    def get_all_block_out_date(self, skip: int, limit: int) -> List[Optional[BlockOutDate]]:
        return self.repository.get_all_block_out_dates(skip, limit)
    
    def get_all_block_out_time(self, skip: int, limit: int) -> List[Optional[BlockOutTime]]:
        return self.repository.get_all_block_out_times(skip, limit)
    
    def filter_block_out_dates_by_start_point(self, date: datetime.date) -> List[Optional[BlockOutDate]]:
        return self.repository.get_blocked_dates_from_starting_point(date)
    
    def filter_block_out_times_by_start_point(self, date: datetime.date) -> List[Optional[BlockOutTime]]:
        return self.repository.get_blocked_times_from_starting_date(date)