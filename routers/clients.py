from fastapi import Depends, APIRouter
from sqlalchemy.orm import Session
from ..schema.clients_schema import Client, UpdateClientDetails, CreateClient, SetClientPenalty
from ..database import get_db
from ..services.clients_service import ClientService

router = APIRouter(
    prefix="/clients",
    tags=["Clients"]
)

@router.post("/", response_model=Client)
def create_client(data: CreateClient, session: Session = Depends(get_db)):
    _service = ClientService(session)
    return _service.create(data)

@router.get("/", response_model=list[Client])
def read_clients(skip: int = 0, limit: int = 100, session: Session = Depends(get_db)):
    _service = ClientService(session)
    return _service.get_all(skip, limit)


@router.get("/{clientId)}", response_model=Client)
def read_client(clientId: int, session: Session = Depends(get_db)):
    _service = ClientService(session)
    return _service.get_by_id(clientId)


@router.put("/{clientId}", response_model=Client)
def update_client_cetails(clientId: int, data: UpdateClientDetails, session: Session = Depends(get_db)):
    _service = ClientService(session)
    return _service.update(clientId, data)


