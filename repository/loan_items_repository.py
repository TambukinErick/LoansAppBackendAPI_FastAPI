from sqlalchemy.orm import Session
from ..models.models import LoanItem
from ..schema import loan_items_schema
from typing import List, Optional, Type

class LoanItemRepository():
        def __init__(self, session: Session):
            self.session = session
        
        def create(self, data: loan_items_schema.CreateLoanItem) -> loan_items_schema.LoanItem:
              loan_item = LoanItem(**data.model_dump(exclude_none=True))
              self.session.add(loan_item)
              self.session.commit()
              self.session.refresh(loan_item)
              return loan_items_schema.LoanItem(**loan_item.__dict__)
        
        def get_all(self, skip, limit) -> List[Optional[loan_items_schema.LoanItem]]:
            loan_items = self.session.query(LoanItem).offset(skip).limit(limit).all()
            return [loan_items_schema.LoanItem(**LoanItem.__dict__) for LoanItem in loan_items]

        def get_by_itemCat(self, itemCat: str) -> Type[LoanItem]:
            return self.session.query(LoanItem).filter_by(itemCat=itemCat).first()
        
        def get_borrowed(self, skip, limit) -> List[Optional[loan_items_schema.LoanItem]]:
            loan_items = self.session.query(LoanItem).filter_by(status = "LOANEDOUT").offset(skip).limit(limit).all()
            return [loan_items_schema.LoanItem(**LoanItem.__dict__) for LoanItem in loan_items]
        
        def item_exists(self, itemCat: str) -> bool:
            loan_item = self.session.query(LoanItem).filter_by(itemCat = itemCat).first()
            return bool(loan_item)
        
        def item_borrowed(self, itemCat: str) -> bool:
            loan_item = self.session.query(LoanItem).filter_by(itemCat = itemCat).first()
            if loan_item.status == "LOANEDOUT":
                return True
            else:
                return False
        def item_lost_or_damaged(self, itemCat: str) -> bool:
            loan_item = self.session.query(LoanItem).filter_by(itemCat = itemCat).first()
            if loan_item.status == "LOST" or loan_item.status == "DAMAGED":
                return True
            return False
        
        def update(self, loanitem: Type[LoanItem], data: loan_items_schema.UpdateLoanItem) -> loan_items_schema.LoanItem:
            for key, value in data.model_dump(exclude_none=True).items():
                setattr(loanitem, key, value)
            self.session.commit()
            self.session.refresh(loanitem)
            return loan_items_schema.LoanItem(**loanitem.__dict__)
        
        def toggle_item_status(self, loanItem: LoanItem, data: loan_items_schema.LoanItemStatus):
            loanItem.status = data
            self.session.commit()
            self.session.refresh(loanItem)

        def report_loss_or_damage_item(self, loanItem: Type[LoanItem], status):
            loanItem.status = status
            self.session.commit()
            self.session.refresh(loanItem)