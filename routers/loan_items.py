from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from ..schema.loan_items_schema import *
from ..services.loan_items_service import LoanItemService
from ..database import get_db

router = APIRouter(
    prefix="/loansitems",
    tags=["Loan Items"]
)

@router.post("/", response_model= LoanItem)
def create_loan_item(loanitem: CreateLoanItem, session: Session = Depends(get_db)):
    _service = LoanItemService(session)
    return _service.create(loanitem)


@router.get("/", response_model=list[LoanItem])
def read_loan_items(skip: int = 0, limit: int = 100, session: Session = Depends(get_db)):
    _service = LoanItemService(session)
    return _service.get_all(skip, limit)


@router.get("/{itemCat}", response_model= LoanItem)
def read_loan_item(itemCat: str, session: Session = Depends(get_db)):
    _service = LoanItemService(session)
    return _service.get_by_itemCat(itemCat)


@router.put("/{itemCat}", response_model=LoanItem)
def update_loan_item(itemCat: str, loanitem: UpdateLoanItem, session: Session = Depends(get_db)):
    _service = LoanItemService(session)
    return _service.update(itemCat, loanitem)
