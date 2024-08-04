from fastapi import Depends, APIRouter, HTTPException
import logging
from sqlalchemy.orm import Session
from ..schema.transactions_schema import Transaction, CreateTransaction, ReturnTransaction, ReportTransaction
from ..models import models
from ..database import get_db
from ..services.transactions_service import TransactionService

router = APIRouter(
    prefix="/transactions",
    tags=["Transactions"]
)

logger = logging.getLogger('uvicorn.error')
logger.setLevel(logging.DEBUG)


@router.get("/client_transactions/{clientId}", response_model=list[Transaction])
def read_client_transactions(clientId: int, skip: int = 0, limit: int = 100, session: Session = Depends(get_db)):
    _service = TransactionService(session)
    return _service.get_all_by_clientId(clientId, skip, limit)

@router.get("/item_transactions/{itemCat}", response_model=list[Transaction])
def read_loan_item_transactions(itemCat: str, skip: int = 0, limit: int = 100, session: Session = Depends(get_db)):
    _service = TransactionService(session)
    return _service.get_all_by_itemCat(itemCat, skip, limit)

@router.get("/", response_model=Transaction)
def read_recent_transaction(itemCat: str, clientId: int, session: Session = Depends(get_db)):
    _service = TransactionService(session)
    return _service.get_transaction(clientId, itemCat)


@router.post("/", response_model=Transaction)
def create_transaction(transaction: CreateTransaction, session: Session = Depends(get_db)):
    _service = TransactionService(session)
    return _service.create(transaction)

@router.put("/return_transaction", response_model=Transaction)
def return_transaction(transaction: ReturnTransaction, session: Session = Depends(get_db)):
    _service = TransactionService(session)
    return _service.return_transaction(transaction)

@router.put("/report")
def report_loss_or_damage(transaction: ReportTransaction, session: Session = Depends(get_db)):
    _service = TransactionService(session)
    _service.report_loss_or_damage(transaction)
