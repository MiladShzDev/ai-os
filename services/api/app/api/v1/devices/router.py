from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from ....deps import get_db
from .schemas import DeviceResponse

router = APIRouter(prefix="/devices", tags=["devices"])


@router.get("/{node_id}", response_model=DeviceResponse)
def get_device(node_id: str, db: Session = Depends(get_db)) -> DeviceResponse:
    raise NotImplementedError
