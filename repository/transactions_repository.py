from sqlalchemy.orm import Session
from sqlalchemy import and_, desc
from ..models.models import Transaction
from ..schema import transactions_schema
from typing import List, Optional, Type

class TransactionRepository:
    def __init__(self, session: Session):
        self.session  = session

    def create(self, data: transactions_schema.CreateTransaction) -> transactions_schema.Transaction:
        transaction = Transaction(**data.model_dump(exclude_none=True))
        self.session.add(transaction)
        self.session.commit()
        self.session.refresh(transaction)
        return transactions_schema.Transaction(**transaction.__dict__)
    
    def get_all_by_clientId(self, clientId: int, skip: int = 0, limit: int = 100) -> List[Optional[transactions_schema.Transaction]]:
        transactions = self.session.query(Transaction).filter_by(clientId=clientId).offset(skip).limit(limit).all()
        return [transactions_schema.Transaction(**transaction.__dict__) for transaction in transactions]
    
    def get_all_by_itemCat(self, itemCat: str, skip: int = 0, limit: int = 100) -> List[Optional[transactions_schema.Transaction]]:
        transactions = self.session.query(Transaction).filter_by(itemCat = itemCat).offset(skip).limit(limit).all()
        return [transactions_schema.Transaction(**transaction.__dict__) for transaction in transactions]
    
    def transaction_exists(self, itemCat: str, clientId: int) -> bool:
        transaction = self.session.query(Transaction).filter(
            and_(Transaction.clientId == clientId, Transaction.itemCat == itemCat)
            ).order_by(desc(Transaction.transactionId)).first()
        return bool(transaction)

    def get_recent_transaction(self, itemCat: str, clientId: int):
        transaction = self.session.query(Transaction).filter(
            and_(Transaction.clientId == clientId, Transaction.itemCat == itemCat)
            ).order_by(desc(Transaction.transactionId)).first()
        return transaction

    def return_transaction(self, transaction: Type[Transaction], data: transactions_schema.ReturnTransaction) -> transactions_schema.Transaction:
        for key, value in data.model_dump(exclude_none=True).items():
            setattr(transaction, key, value)
        self.session.commit()
        self.session.refresh(transaction)
        return transactions_schema.Transaction(**transaction.__dict__)
    
    def transaction_ongoing(self, clientId: int, itemCat: str) -> bool:
        transaction = self.session.query(Transaction).filter(
            and_(Transaction.clientId == clientId, Transaction.itemCat == itemCat)
            ).order_by(desc(Transaction.transactionId)).first()
        if transaction.transactionStatus == "ONGOING":
            return True
        return False
    def report_transaction(self, transaction: Transaction, penalty: str):
        transaction.transactionStatus = penalty
        self.session.commit()
        self.session.refresh(transaction)
    