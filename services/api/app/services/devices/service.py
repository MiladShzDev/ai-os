from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ...models.device import Device


def create_device(
    db: Session,
    data: dict,
) -> Device:
    if db.get(Device, data["node_id"]) is not None:
        raise ValueError("Device already exists")

    device = Device(**data)

    db.add(device)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("Device already exists")

    db.refresh(device)

    return device


def get_device(
    db: Session,
    node_id: str,
) -> Device | None:
    return db.get(
        Device,
        node_id,
    )


def list_devices(
    db: Session,
    limit: int = 50,
    offset: int = 0,
    node_type: str | None = None,
    platform: str | None = None,
    status: str | None = None,
    agent_id: str | None = None,
) -> list[Device]:
    query = db.query(Device)

    if node_type is not None:
        query = query.filter(
            Device.node_type == node_type
        )

    if platform is not None:
        query = query.filter(
            Device.platform == platform
        )

    if status is not None:
        query = query.filter(
            Device.status == status
        )

    if agent_id is not None:
        query = query.filter(
            Device.agent_id == agent_id
        )

    return (
        query
        .order_by(Device.node_id)
        .offset(offset)
        .limit(limit)
        .all()
    )


def update_device(
    db: Session,
    device: Device,
    updates: dict,
) -> Device:
    for field, value in updates.items():
        setattr(
            device,
            field,
            value,
        )

    db.commit()
    db.refresh(device)

    return device


def delete_device(
    db: Session,
    device: Device,
) -> None:
    db.delete(device)
    db.commit()
