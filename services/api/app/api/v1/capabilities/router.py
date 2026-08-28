from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ....deps import get_db
from ....models.capability import Capability
from .schemas import CapabilityCreate, CapabilityResponse, CapabilityUpdate

router = APIRouter(prefix="/capabilities", tags=["capabilities"])


@router.post("", response_model=CapabilityResponse, status_code=201)
def create_capability(
    payload: CapabilityCreate,
    db: Session = Depends(get_db),
) -> Capability:
    if db.get(Capability, payload.capability_id) is not None:
        raise HTTPException(status_code=409, detail="Capability already exists")

    capability = Capability(**payload.model_dump())
    db.add(capability)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Capability already exists")

    db.refresh(capability)

    return capability


@router.get("/{capability_id}", response_model=CapabilityResponse)
def get_capability(
    capability_id: str,
    db: Session = Depends(get_db),
) -> Capability:
    capability = db.get(Capability, capability_id)

    if capability is None:
        raise HTTPException(status_code=404, detail="Capability not found")

    return capability


@router.patch("/{capability_id}", response_model=CapabilityResponse)
def update_capability(
    capability_id: str,
    payload: CapabilityUpdate,
    db: Session = Depends(get_db),
) -> Capability:
    capability = db.get(Capability, capability_id)

    if capability is None:
        raise HTTPException(status_code=404, detail="Capability not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(capability, field, value)

    db.commit()
    db.refresh(capability)

    return capability


@router.delete("/{capability_id}", status_code=204)
def delete_capability(
    capability_id: str,
    db: Session = Depends(get_db),
) -> None:
    capability = db.get(Capability, capability_id)

    if capability is None:
        raise HTTPException(status_code=404, detail="Capability not found")

    db.delete(capability)
    db.commit()
