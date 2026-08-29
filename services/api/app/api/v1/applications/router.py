from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ....deps import get_db
from ....models.application import Application
from ....services.applications.service import (
    create_application as create_application_service,
    get_application as get_application_service,
    update_application as update_application_service,
    delete_application as delete_application_service,
)
from .schemas import ApplicationCreate, ApplicationResponse, ApplicationUpdate


router = APIRouter(
    prefix="/applications",
    tags=["applications"],
)


@router.post(
    "",
    response_model=ApplicationResponse,
    status_code=201,
)
def create_application(
    payload: ApplicationCreate,
    db: Session = Depends(get_db),
) -> Application:
    try:
        return create_application_service(
            db,
            payload.model_dump(),
        )

    except ValueError as error:
        raise HTTPException(
            status_code=409,
            detail=str(error),
        )


@router.get(
    "/{application_id}",
    response_model=ApplicationResponse,
)
def get_application(
    application_id: str,
    db: Session = Depends(get_db),
) -> Application:
    application = get_application_service(
        db,
        application_id,
    )

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found",
        )

    return application


@router.patch(
    "/{application_id}",
    response_model=ApplicationResponse,
)
def update_application(
    application_id: str,
    payload: ApplicationUpdate,
    db: Session = Depends(get_db),
) -> Application:
    application = get_application_service(
        db,
        application_id,
    )

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found",
        )

    return update_application_service(
        db,
        application,
        payload.model_dump(
            exclude_unset=True,
        ),
    )


@router.delete(
    "/{application_id}",
    status_code=204,
)
def delete_application(
    application_id: str,
    db: Session = Depends(get_db),
) -> None:
    application = get_application_service(
        db,
        application_id,
    )

    if application is None:
        raise HTTPException(
            status_code=404,
            detail="Application not found",
        )

    delete_application_service(
        db,
        application,
    )
