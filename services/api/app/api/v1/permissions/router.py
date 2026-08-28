from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ....deps import get_db
from ....models.permission import Permission
from .schemas import PermissionCreate, PermissionResponse, PermissionUpdate

router = APIRouter(prefix="/permissions", tags=["permissions"])


@router.post("", response_model=PermissionResponse, status_code=201)
def create_permission(
    payload: PermissionCreate,
    db: Session = Depends(get_db),
) -> Permission:
    if db.get(Permission, payload.permission_id) is not None:
        raise HTTPException(status_code=409, detail="Permission already exists")

    permission = Permission(**payload.model_dump())
    db.add(permission)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Permission already exists")

    db.refresh(permission)

    return permission


@router.get("/{permission_id}", response_model=PermissionResponse)
def get_permission(
    permission_id: str,
    db: Session = Depends(get_db),
) -> Permission:
    permission = db.get(Permission, permission_id)

    if permission is None:
        raise HTTPException(status_code=404, detail="Permission not found")

    return permission


@router.patch("/{permission_id}", response_model=PermissionResponse)
def update_permission(
    permission_id: str,
    payload: PermissionUpdate,
    db: Session = Depends(get_db),
) -> Permission:
    permission = db.get(Permission, permission_id)

    if permission is None:
        raise HTTPException(status_code=404, detail="Permission not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(permission, field, value)

    db.commit()
    db.refresh(permission)

    return permission


@router.delete("/{permission_id}", status_code=204)
def delete_permission(
    permission_id: str,
    db: Session = Depends(get_db),
) -> None:
    permission = db.get(Permission, permission_id)

    if permission is None:
        raise HTTPException(status_code=404, detail="Permission not found")

    db.delete(permission)
    db.commit()
