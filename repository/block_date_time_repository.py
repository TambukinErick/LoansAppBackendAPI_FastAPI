from sqlalchemy.orm import Session
from ..models.models import BlockOutDate, BlockOutTime
from ..schema import block_out_schema
from typing import List, Optional, Type
import datetime

class BlockOutRepository:
    def __init__(self, session: Session):
        self.session = session

    def create_block_out_date(self, data: block_out_schema.BlockOutDate) -> BlockOutDate:
        block_out_date = BlockOutDate(**data.model_dump(exclude_none=True))
        self.session.add(block_out_date)
        self.session.commit()
        self.session.refresh(block_out_date)
        return block_out_schema.BlockOutDate(**block_out_date.__dict__)
    
    def create_block_out_time(self, data: block_out_schema.BlockOutTime) -> BlockOutTime:
        block_out_time = BlockOutTime(**data.model_dump(exclude_none=True))
        self.session.add(block_out_time)
        self.session.commit()
        self.session.refresh(block_out_time)
        return block_out_schema.BlockOutTime(**block_out_time.__dict__)
    
    def get_all_block_out_dates(self, skip: int, limit: int) -> List[Optional[block_out_schema.BlockOutDate]]:
        blocked_dates = self.session.query(BlockOutDate).offset(skip).limit(limit).all()
        return [block_out_schema.BlockOutDate(**blocked_date.__dict__) for blocked_date in blocked_dates]
    
    def get_all_block_out_times(self, skip: int, limit: int) -> List[Optional[block_out_schema.BlockOutTime]]:
        blocked_times = self.session.query(BlockOutTime).offset(skip).limit(limit).all()
        return [block_out_schema.BlockOutTime(**blocked_time.__dict__) for blocked_time in blocked_times]
    
    def get_blocked_dates_from_starting_point(self, date: datetime.date) -> List[Optional[block_out_schema.BlockOutDate]]:
        blocked_dates = self.session.query(BlockOutDate).filter(BlockOutDate.dateBlocked >= date).limit(30).all()
        return [block_out_schema.BlockOutDate(**blocked_date.__dict__) for blocked_date in blocked_dates]
    
    def get_blocked_times_from_starting_date(self, date: datetime.datetime) ->  List[Optional[block_out_schema.BlockOutTime]]:
        blocked_times = self.session.query(BlockOutTime).filter(BlockOutTime.dateBlocked >= date).limit(30).all()
        return [block_out_schema.BlockOutTime(**blocked_time.__dict__) for blocked_time in blocked_times]
    
    def block_out_date_exists(self, date: datetime.date) -> bool:
        blocked_date = self.session.query(BlockOutDate).filter(BlockOutDate.dateBlocked == date).first()
        return bool(blocked_date)
    
    def block_out_time_exists(self, date: datetime.date) -> bool:
        blocked_time = self.session.query(BlockOutTime).filter(BlockOutTime.dateBlocked == date).first()
        return bool(blocked_time)