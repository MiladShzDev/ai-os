from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ....deps import get_db
from ....models.device import Device
from .schemas import DeviceCreate, DeviceResponse, DeviceUpdate

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

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Device already exists")

    db.refresh(device)

    return device


@router.get("/{node_id}", response_model=DeviceResponse)
def get_device(node_id: str, db: Session = Depends(get_db)) -> Device:
    device = db.get(Device, node_id)

    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")

    return device


@router.get("", response_model=list[DeviceResponse])
def list_devices(
    limit: int = Query(default=50, ge=1, le=100),
    offset: int = Query(default=0, ge=0),
    db: Session = Depends(get_db),
) -> list[Device]:
    return (
        db.query(Device)
        .order_by(Device.node_id)
        .offset(offset)
        .limit(limit)
        .all()
    )


@router.delete("/{node_id}", status_code=204)
def delete_device(node_id: str, db: Session = Depends(get_db)) -> None:
    device = db.get(Device, node_id)

    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")

    db.delete(device)
    db.commit()


@router.patch("/{node_id}", response_model=DeviceResponse)
def update_device(
    node_id: str,
    payload: DeviceUpdate,
    db: Session = Depends(get_db),
) -> Device:
    device = db.get(Device, node_id)

    if device is None:
        raise HTTPException(status_code=404, detail="Device not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(device, field, value)

    db.commit()
    db.refresh(device)

    return device
