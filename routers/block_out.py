from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from ..schema.block_out_schema import BlockOutDate, BlockOutTime
from ..database import get_db
from ..services.block_date_time_service import BlockOutService
import datetime

router = APIRouter(
    prefix="/blockedout",
    tags=["Blocked Dates and Times"]
)

@router.post("/create_date", response_model=BlockOutDate)
async def create_block_out_dates(data: BlockOutDate, session: Session = Depends(get_db)):
    _service = BlockOutService(session)
    return _service.create_block_out_date(data)

@router.post("/create_time", response_model=BlockOutTime)
async def create_block_out_times(data: BlockOutTime, session: Session = Depends(get_db)):
    _service = BlockOutService(session)
    return _service.create_block_out_time(data)

@router.get("/blocked_dates", response_model=list[BlockOutDate])
async def read_blocked_dates(skip: int = 0, limit: int = 100, session: Session = Depends(get_db)):
    _service = BlockOutService(session)
    return _service.get_all_block_out_date(skip, limit)

@router.get("/blocked_times", response_model=list[BlockOutTime])
async def read_blocked_times(skip: int = 0, limit: int = 100, session: Session = Depends(get_db)):
    _service = BlockOutService(session)
    return _service.get_all_block_out_time(skip, limit)

@router.get("/blocked_dates/{date}", response_model=list[BlockOutDate])
async def read_filtered_blocked_dates(date: datetime.date, session: Session = Depends(get_db)):
    _service = BlockOutService(session)
    return _service.filter_block_out_dates_by_start_point(date)

@router.get("/blocked_times/{date}", response_model=list[BlockOutTime])
async def read_filtered_blocked_times(date: datetime.date, session: Session = Depends(get_db)):
    _service = BlockOutService(session)
    return _service.filter_block_out_times_by_start_point(date)