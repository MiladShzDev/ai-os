from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session

from ....deps import get_db
from ....services.devices.service import (
    create_device as create_device_service,
    get_device as get_device_service,
    list_devices as list_devices_service,
    update_device as update_device_service,
    delete_device as delete_device_service,
)
from .schemas import DeviceCreate, DeviceResponse, DeviceUpdate


router = APIRouter(
    prefix="/devices",
    tags=["devices"],
)


@router.post(
    "",
    response_model=DeviceResponse,
    status_code=201,
)
def create_device(
    payload: DeviceCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_device_service(
            db,
            payload.model_dump(),
        )

    except ValueError as error:
        raise HTTPException(
            status_code=409,
            detail=str(error),
        )


@router.get(
    "/{node_id}",
    response_model=DeviceResponse,
)
def get_device(
    node_id: str,
    db: Session = Depends(get_db),
):
    device = get_device_service(
        db,
        node_id,
    )

    if device is None:
        raise HTTPException(
            status_code=404,
            detail="Device not found",
        )

    return device


@router.get(
    "",
    response_model=list[DeviceResponse],
)
def list_devices(
    limit: int = Query(
        default=50,
        ge=1,
        le=100,
    ),
    offset: int = Query(
        default=0,
        ge=0,
    ),
    node_type: str | None = Query(
        default=None,
        min_length=1,
        max_length=100,
    ),
    platform: str | None = Query(
        default=None,
        min_length=1,
        max_length=100,
    ),
    status: str | None = Query(
        default=None,
        min_length=1,
        max_length=50,
    ),
    agent_id: str | None = Query(
        default=None,
        min_length=1,
        max_length=255,
    ),
    db: Session = Depends(get_db),
):
    return list_devices_service(
        db,
        limit,
        offset,
        node_type,
        platform,
        status,
        agent_id,
    )


@router.patch(
    "/{node_id}",
    response_model=DeviceResponse,
)
def update_device(
    node_id: str,
    payload: DeviceUpdate,
    db: Session = Depends(get_db),
):
    device = get_device_service(
        db,
        node_id,
    )

    if device is None:
        raise HTTPException(
            status_code=404,
            detail="Device not found",
        )

    return update_device_service(
        db,
        device,
        payload.model_dump(
            exclude_unset=True,
        ),
    )


@router.delete(
    "/{node_id}",
    status_code=204,
)
def delete_device(
    node_id: str,
    db: Session = Depends(get_db),
):
    device = get_device_service(
        db,
        node_id,
    )

    if device is None:
        raise HTTPException(
            status_code=404,
            detail="Device not found",
        )

    delete_device_service(
        db,
        device,
    )
