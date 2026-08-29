from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ...models.application import Application


def create_application(
    db: Session,
    data: dict,
) -> Application:
    if db.get(
        Application,
        data["application_id"],
    ) is not None:
        raise ValueError(
            "Application already exists"
        )

    application = Application(**data)

    db.add(application)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError(
            "Application already exists"
        )

    db.refresh(application)

    return application


def get_application(
    db: Session,
    application_id: str,
) -> Application | None:
    return db.get(
        Application,
        application_id,
    )


def update_application(
    db: Session,
    application: Application,
    updates: dict,
) -> Application:
    for field, value in updates.items():
        setattr(
            application,
            field,
            value,
        )

    db.commit()
    db.refresh(application)

    return application


def delete_application(
    db: Session,
    application: Application,
) -> None:
    db.delete(application)
    db.commit()
