from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ....deps import get_db
from ....models.agent import Agent
from .schemas import AgentCreate, AgentResponse, AgentUpdate

router = APIRouter(prefix="/agents", tags=["agents"])


@router.post("", response_model=AgentResponse, status_code=201)
def create_agent(
    payload: AgentCreate,
    db: Session = Depends(get_db),
) -> Agent:
    if db.get(Agent, payload.agent_id) is not None:
        raise HTTPException(status_code=409, detail="Agent already exists")

    agent = Agent(**payload.model_dump())
    db.add(agent)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=409, detail="Agent already exists")

    db.refresh(agent)

    return agent


@router.get("/{agent_id}", response_model=AgentResponse)
def get_agent(
    agent_id: str,
    db: Session = Depends(get_db),
) -> Agent:
    agent = db.get(Agent, agent_id)

    if agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")

    return agent


@router.patch("/{agent_id}", response_model=AgentResponse)
def update_agent(
    agent_id: str,
    payload: AgentUpdate,
    db: Session = Depends(get_db),
) -> Agent:
    agent = db.get(Agent, agent_id)

    if agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")

    for field, value in payload.model_dump(exclude_unset=True).items():
        setattr(agent, field, value)

    db.commit()
    db.refresh(agent)

    return agent


@router.delete("/{agent_id}", status_code=204)
def delete_agent(
    agent_id: str,
    db: Session = Depends(get_db),
) -> None:
    agent = db.get(Agent, agent_id)

    if agent is None:
        raise HTTPException(status_code=404, detail="Agent not found")

    db.delete(agent)
    db.commit()
