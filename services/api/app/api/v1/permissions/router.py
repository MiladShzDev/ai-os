from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ....deps import get_db
from ....models.permission import Permission
from ....services.permissions.service import (
    create_permission as create_permission_service,
    get_permission as get_permission_service,
    update_permission as update_permission_service,
    delete_permission as delete_permission_service,
)
from .schemas import PermissionCreate, PermissionResponse, PermissionUpdate


router = APIRouter(
    prefix="/permissions",
    tags=["permissions"],
)


@router.post(
    "",
    response_model=PermissionResponse,
    status_code=201,
)
def create_permission(
    payload: PermissionCreate,
    db: Session = Depends(get_db),
) -> Permission:
    try:
        return create_permission_service(
            db,
            payload.model_dump(),
        )

    except ValueError as error:
        raise HTTPException(
            status_code=409,
            detail=str(error),
        )


@router.get(
    "/{permission_id}",
    response_model=PermissionResponse,
)
def get_permission(
    permission_id: str,
    db: Session = Depends(get_db),
) -> Permission:
    permission = get_permission_service(
        db,
        permission_id,
    )

    if permission is None:
        raise HTTPException(
            status_code=404,
            detail="Permission not found",
        )

    return permission


@router.patch(
    "/{permission_id}",
    response_model=PermissionResponse,
)
def update_permission(
    permission_id: str,
    payload: PermissionUpdate,
    db: Session = Depends(get_db),
) -> Permission:
    permission = get_permission_service(
        db,
        permission_id,
    )

    if permission is None:
        raise HTTPException(
            status_code=404,
            detail="Permission not found",
        )

    return update_permission_service(
        db,
        permission,
        payload.model_dump(
            exclude_unset=True,
        ),
    )


@router.delete(
    "/{permission_id}",
    status_code=204,
)
def delete_permission(
    permission_id: str,
    db: Session = Depends(get_db),
) -> None:
    permission = get_permission_service(
        db,
        permission_id,
    )

    if permission is None:
        raise HTTPException(
            status_code=404,
            detail="Permission not found",
        )

    delete_permission_service(
        db,
        permission,
    )
