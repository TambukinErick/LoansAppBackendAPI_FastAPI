from typing import List
from fastapi import HTTPException
from sqlalchemy.orm import Session
from ..repository.clients_repository import ClientRepository
from ..schema.clients_schema import Client, UpdateClientDetails, CreateClient,SetClientPenalty

class ClientService:
    """
    Service Class for handling clients
    """

    def __init__(self, session: Session):
        self.repository = ClientRepository(session)
    
    def create(self, data: CreateClient) -> Client:
        if self.repository.client_exists(data.clientId):
            raise HTTPException(status_code=400, detail="Client Already Exists")
        client = self.repository.create(data)
        return client
    
    def get_all(self, skip: int = 0, limit: int = 100) -> List[Client]:
        return self.repository.get_all(skip, limit)
    
    def get_by_id(self, clientId) -> Client:
        if self.repository.client_exists(clientId):
            return self.repository.get_by_id(clientId)
        raise HTTPException(status_code=404, detail="Client Not Found")
    
    def update(self, clientId: int, data: UpdateClientDetails):
        if not self.repository.client_exists(clientId):
            raise HTTPException(status_code=404, detail="Client Not Found")
        client = self.repository.get_by_id(clientId)
        updated_client = self.repository.update(client, data)
        return updated_client
    
    