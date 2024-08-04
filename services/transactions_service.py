from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..repository import transactions_repository, clients_repository, loan_items_repository
from ..schema.transactions_schema import *
from ..schema.loan_items_schema import LoanItemStatus
from ..schema.clients_schema import SetClientPenalty


class TransactionService:
    def __init__(self, session: Session):
        self.client_repo = clients_repository.ClientRepository(session)
        self.loan_item_repo = loan_items_repository.LoanItemRepository(session)
        self.transaction_repo = transactions_repository.TransactionRepository(session)
    
    def get_transaction(self, clientId: int, itemCat: str):
        if not self.transaction_repo.transaction_exists(itemCat, clientId):
            raise HTTPException(status_code=404, detail="Transaction Does Not Exist")
        return self.transaction_repo.get_recent_transaction(itemCat, clientId)

    def get_all_by_clientId(self, clientId: int, skip: int = 0, limit: int = 100):
        return self.transaction_repo.get_all_by_clientId(clientId, skip, limit)
    
    def get_all_by_itemCat(self, itemCat: str, skip: int = 0, limit: int = 100):
        return self.transaction_repo.get_all_by_itemCat(itemCat, skip, limit)

    def create(self, data: CreateTransaction) -> Transaction:
        client, loan_item = self.__get_create_transaction_dependencies(data.itemCat, data.clientId)
        transaction = self.transaction_repo.create(data)
        self.client_repo.toggle_client_borrowing(client)
        self.loan_item_repo.toggle_item_status(loan_item, LoanItemStatus.LOANEDOUT)
        return transaction
    

    def return_transaction(self, data: ReturnTransaction):
        client, loan_item = self.__get_return_transaction_dependencies(data.itemCat, data.clientId)
        transaction = self.transaction_repo.get_recent_transaction(data.itemCat, data.clientId)

        returned_transaction = self.transaction_repo.return_transaction(transaction, data)

        self.client_repo.toggle_client_borrowing(client)
        self.loan_item_repo.toggle_item_status(loan_item, LoanItemStatus.INSTORAGE)
        penalty_calculator = PenaltyCalculator(data.itemCat, data.overdueDays, 
                                               data.overdueHours, data.overDueMinutes, 
                                               client.warningCount)
        # penalty: SetClientPenalty = penalty_calculator.calculatePenalty()
        self.client_repo.set_client_penalties(client, penalty_calculator.calculatePenalty())
        return returned_transaction
    

    def report_loss_or_damage(self, data: ReportTransaction):
        client, loan_item, transaction = self.__get_report_transaction_dependencies(data.itemCat, data.clientId)
        self.transaction_repo.report_transaction(transaction, data.transactionStatus)
        self.client_repo.set_client_penalties(client, SetClientPenalty(fineAmount=data.fineAmount))
        self.loan_item_repo.report_loss_or_damage_item(loan_item, data.transactionStatus)

    





    def __get_create_transaction_dependencies(self, itemCat: str, clientId: int):
        if not self.client_repo.client_exists(clientId):
            raise HTTPException(status_code=404, detail="Client Does Not Exist")
        if not self.loan_item_repo.item_exists(itemCat):
            raise HTTPException(status_code=409, detail="Item Does Not Exist")
        if self.transaction_repo.transaction_ongoing(clientId, itemCat):
            raise HTTPException(status_code=409, detail="Ongoing Transaction")

        client = self.client_repo.get_by_id(clientId)
        if client.borrowing:
            raise HTTPException(status_code=409, detail="Client currently borrowing another item")
        if client.blackListed or client.tempBlackList:
            raise HTTPException(status_code=409, detail="Client currently penalized")
        
        loan_item = self.loan_item_repo.get_by_itemCat(itemCat)
        if loan_item.status == "LOANEDOUT":
            raise HTTPException(status_code=409, detail="Item Currently Loaned Out")
        if loan_item.status == "DAMAGED" or loan_item.status == "LOST":
            raise HTTPException(status_code=409, detail="Item Damaged or Lost")
        
        return client, loan_item
        
    def __get_return_transaction_dependencies(self, itemCat: str, clientId: int):
        if not self.client_repo.client_exists(clientId):
            raise HTTPException(status_code=404, detail="Client Does Not Exist")
        if not self.loan_item_repo.item_exists(itemCat):
            raise HTTPException(status_code=409, detail="Item Does Not Exist")
        if not self.transaction_repo.transaction_ongoing(clientId, itemCat):
            raise HTTPException(status_code=409, detail="Ongoing Transaction")
        
        client = self.client_repo.get_by_id(clientId)

        if not client.borrowing:
            raise HTTPException(status_code=409, detail="Client currently has no ongoing transaction")
        loan_item = self.loan_item_repo.get_by_itemCat(itemCat)
        if loan_item.status == "INSTORAGE" or loan_item.status == "DAMAGED" or loan_item.status == "LOST":
            raise HTTPException(status_code=409, detail="Item Currently Unavailable to Be In a Transaction")
        
        return client, loan_item
    
    def __get_report_transaction_dependencies(self, itemCat: str, clientId: int):
        if not self.client_repo.client_exists(clientId):
            raise HTTPException(status_code=404, detail="Client Does Not Exist")
        if not self.loan_item_repo.item_exists(itemCat):
            raise HTTPException(status_code=409, detail="Item Does Not Exist")
        if not self.transaction_repo.transaction_exists(clientId, itemCat):
            raise HTTPException(status_code=409, detail="No Ongoing Transaction")
        
        client = self.client_repo.get_by_id(clientId)
        loan_item = self.loan_item_repo.get_by_itemCat(itemCat)
        transaction = self.transaction_repo.get_recent_transaction(itemCat, clientId)

        return client, loan_item, transaction


class PenaltyCalculator:
    def __init__(self, itemCat: int, overdueDays: int, overdueHours: int,overdueMinutes: int, warningCount: int = 0):
        self.itemCat = itemCat
        self.overdueDays = overdueDays
        self.overdueHours = overdueHours
        self.overdueMinutes = overdueMinutes
        self.warningCount = warningCount

    def calculatePenalty(self) -> SetClientPenalty:
        if self.checkItemType() == "A":
            return self.applyTypeAPenalty()
        return self.applyTypeBPenalty()

    def checkItemType(self):
        if (self.itemCat.startswith('B') or 
            self.itemCat.startswith('C') or 
            self.itemCat.startswith('D') or 
            self.itemCat.startswith('TR') or 
            self.itemCat.startswith('U')):
            return 'A'
        return 'B'

    def applyTypeAPenalty(self):
        if self.warningCount > 3:
            return SetClientPenalty(blackListed=True, holdOrder=True, excuseLetter=True, 
                                    fineAmount=1000, warningCount=self.warningCount)
        elif 1 <= self.overdueDays <= 3:
            return SetClientPenalty(warningCount=(self.warningCount + 1))
        elif 4 <= self.overdueDays <= 10:
            return SetClientPenalty(tempBlackList=True, excuseLetter=True)
        elif self.overdueDays > 10:
            return SetClientPenalty(tempBlackList=True, holdOrder=True, fineAmount=500, excuseLetter=True)
        else:
            return SetClientPenalty()
    def applyTypeBPenalty(self) -> SetClientPenalty:
        if self.warningCount == 3:
            return SetClientPenalty(blackListed=True,
                                    holdOrder=True, excuseLetter=True, 
                                    fineAmount=1000, warningCount=self.warningCount)
        elif 3 <= self.overdueHours <= 5:
            return SetClientPenalty(warningCount=(self.warningCount + 1))
        elif 6 <= self.overdueHours <= 10:
            return SetClientPenalty(tempBlackList=True, excuseLetter=True)
        elif self.overdueHours > 10:
            return SetClientPenalty(tempBlackList=True, holdOrder=True, fineAmount=500, excuseLetter=True)
        else:
            return SetClientPenalty()









