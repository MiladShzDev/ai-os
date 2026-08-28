from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ....deps import get_db
from ....models.device import Device
from .schemas import DeviceCreate, DeviceResponse

router = APIRouter(prefix="/devices", tags=["devices"])


@router.post("", response_model=DeviceResponse, status_code=201)
def create_device(
    payload: DeviceCreate,
    db: Session = Depends(get_db),
) -> Device:
    if db.get(Device, payload.node_id) is not None:
        raise HTTPException(status_code=409, detail="Device already exists")

    device = Device(**payload.model_dump())
    db.add(device)
    db.commit()
    db.refresh(device)

    return device


@router.get("/{node_id}", response_model=DeviceResponse)
def get_device(node_id: str, db: Session = Depends(get_db)) -> Device:
    device = db.get(Device, node_id)

    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")

    return device


@router.get("", response_model=list[DeviceResponse])
def list_devices(db: Session = Depends(get_db)) -> list[Device]:
    return db.query(Device).order_by(Device.node_id).all()


@router.post("", response_model=DeviceResponse, status_code=201)
def create_device(
    payload: DeviceCreate,
    db: Session = Depends(get_db),
) -> Device:
    if db.get(Device, payload.node_id) is not None:
        raise HTTPException(status_code=409, detail="Device already exists")

    device = Device(**payload.model_dump())
    db.add(device)
    db.commit()
    db.refresh(device)
    return device
