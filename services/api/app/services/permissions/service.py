from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ...models.permission import Permission


def create_permission(
    db: Session,
    data: dict,
) -> Permission:
    if db.get(
        Permission,
        data["permission_id"],
    ) is not None:
        raise ValueError(
            "Permission already exists"
        )

    permission = Permission(**data)

    db.add(permission)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError(
            "Permission already exists"
        )

    db.refresh(permission)

    return permission


def get_permission(
    db: Session,
    permission_id: str,
) -> Permission | None:
    return db.get(
        Permission,
        permission_id,
    )


def update_permission(
    db: Session,
    permission: Permission,
    updates: dict,
) -> Permission:
    for field, value in updates.items():
        setattr(
            permission,
            field,
            value,
        )

    db.commit()
    db.refresh(permission)

    return permission


def delete_permission(
    db: Session,
    permission: Permission,
) -> None:
    db.delete(permission)
    db.commit()
