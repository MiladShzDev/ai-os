from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from ....deps import get_db
from ....services.agents.service import (
    create_agent as create_agent_service,
    delete_agent as delete_agent_service,
    get_agent as get_agent_service,
    update_agent as update_agent_service,
)
from .schemas import AgentCreate, AgentResponse, AgentUpdate

router = APIRouter(prefix="/agents", tags=["agents"])


@router.post("", response_model=AgentResponse, status_code=201)
def create_agent(
    payload: AgentCreate,
    db: Session = Depends(get_db),
):
    try:
        return create_agent_service(
            db,
            payload.model_dump(),
        )
    except ValueError as error:
        raise HTTPException(
            status_code=409,
            detail=str(error),
        )


@router.get("/{agent_id}", response_model=AgentResponse)
def get_agent(
    agent_id: str,
    db: Session = Depends(get_db),
):
    agent = get_agent_service(
        db,
        agent_id,
    )

    if agent is None:
        raise HTTPException(
            status_code=404,
            detail="Agent not found",
        )

    return agent


@router.patch("/{agent_id}", response_model=AgentResponse)
def update_agent(
    agent_id: str,
    payload: AgentUpdate,
    db: Session = Depends(get_db),
):
    agent = get_agent_service(
        db,
        agent_id,
    )

    if agent is None:
        raise HTTPException(
            status_code=404,
            detail="Agent not found",
        )

    return update_agent_service(
        db,
        agent,
        payload.model_dump(
            exclude_unset=True,
        ),
    )


@router.delete("/{agent_id}", status_code=204)
def delete_agent(
    agent_id: str,
    db: Session = Depends(get_db),
):
    agent = get_agent_service(
        db,
        agent_id,
    )

    if agent is None:
        raise HTTPException(
            status_code=404,
            detail="Agent not found",
        )

    delete_agent_service(
        db,
        agent,
    )
