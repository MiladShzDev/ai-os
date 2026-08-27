from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ....deps import get_db
from ....models.device import Device
from .schemas import DeviceResponse

router = APIRouter(prefix="/devices", tags=["devices"])


@router.get("/{node_id}", response_model=DeviceResponse)
def get_device(node_id: str, db: Session = Depends(get_db)) -> Device:
    device = db.get(Device, node_id)

    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")

    return device
