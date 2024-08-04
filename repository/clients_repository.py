from sqlalchemy.orm import Session
from ..models.models import Client
from ..schema import clients_schema
from typing import List, Optional, Type

class ClientRepository:
    def __init__(self, session: Session):
        self.session = session

    def create(self, data: clients_schema.CreateClient) -> Client:
        client = Client(**data.model_dump(exclude_none=True))
        self.session.add(client)
        self.session.commit()
        self.session.refresh(client)
        return clients_schema.Client(**client.__dict__)
    
    def get_all(self, skip, limit) -> List[Optional[clients_schema.Client]]:
        clients = self.session.query(Client).offset(skip).limit(limit).all()
        return [clients_schema.Client(**client.__dict__) for client in clients]
    
    def get_by_id(self, _id: int) -> Type[Client]:
        return self.session.query(Client).filter_by(clientId = _id).first()
    
    def get_borrowing(self, skip, limit) -> List[Optional[clients_schema.Client]]:
        clients = self.session.query(Client).filter_by(borrowing = True).offset(skip).limit(limit).all()
        return [clients_schema.Client(**client.__dict__) for client in clients]

    
    def client_exists(self, _id: int) -> bool:
        client = self.session.query(Client).filter_by(clientId = _id).first()
        return bool(client)

    def client_borrowing(self, _id: int) -> bool:
        client = self.session.query(Client).filter_by(clientId = _id).first()
        return client.borrowing
    
    def client_penalized(self, _id: int) -> bool:
        client = self.session.query(Client).filter_by(clientId = _id).first()
        if client.blackListed or client.tempBlackList:
            return True
        return False

    def update(self, client: Type[Client], data: clients_schema.UpdateClientDetails) -> clients_schema.Client:
        for key, value in data.model_dump(exclude_none=True).items():
            setattr(client, key, value)
        self.session.commit()
        self.session.refresh(client)
        return clients_schema.Client(**client.__dict__)
    
    def toggle_client_borrowing(self, client: Client):
        if client.borrowing:
            client.borrowing = False
        else:
            client.borrowing = True
            client.borrowCount += 1

        self.session.commit()
        self.session.refresh(client)

    def set_client_penalties(self, client: Client, data: clients_schema.SetClientPenalty):
        for key, value in data.model_dump(exclude_none=True).items():
            setattr(client, key, value)
        self.session.commit()
        self.session.refresh(client)
