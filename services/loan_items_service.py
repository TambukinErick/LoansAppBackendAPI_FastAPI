from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..repository.loan_items_repository import LoanItemRepository
from ..schema.loan_items_schema import *

class LoanItemService:

    def __init__(self, session: Session):
        self.repository = LoanItemRepository(session)

    def create(self, data: CreateLoanItem) -> LoanItem:
        if self.repository.item_exists(data.itemCat):
            raise HTTPException(status_code=400, detail="Item Already Exists")
        loan_item = self.repository.create(data)
        return loan_item
    
    def get_all(self, skip: int = 0, limit: int = 0) -> List[LoanItem]:
        return self.repository.get_all(skip, limit)
    
    def get_by_itemCat(self, itemCat: str) -> LoanItem:
        if not self.repository.item_exists(itemCat):
            raise HTTPException(status_code=404, detail="Item Not Found")
        return self.repository.get_by_itemCat(itemCat)
    
    def get_loaned_out(self, skip: int = 0, limit: int = 0) -> List[LoanItem]:
        return self.repository.get_borrowed(skip, limit)
    
    def update(self, itemCat: str, data: UpdateLoanItem):
        if not self.repository.item_exists(itemCat):
            raise HTTPException(status_code=404, detail="Item Not Found")
        loan_item = self.repository.get_by_itemCat(itemCat)
        updated_loan_item = self.repository.update(loan_item, data)
        return updated_loan_item

    