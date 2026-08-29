from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session

from ...models.agent import Agent


def create_agent(
    db: Session,
    data: dict,
) -> Agent:
    if db.get(Agent, data["agent_id"]) is not None:
        raise ValueError("Agent already exists")

    agent = Agent(**data)

    db.add(agent)

    try:
        db.commit()
    except IntegrityError:
        db.rollback()
        raise ValueError("Agent already exists")

    db.refresh(agent)

    return agent


def get_agent(
    db: Session,
    agent_id: str,
) -> Agent | None:
    return db.get(
        Agent,
        agent_id,
    )


def update_agent(
    db: Session,
    agent: Agent,
    updates: dict,
) -> Agent:
    for field, value in updates.items():
        setattr(
            agent,
            field,
            value,
        )

    db.commit()
    db.refresh(agent)

    return agent


def delete_agent(
    db: Session,
    agent: Agent,
) -> None:
    db.delete(agent)
    db.commit()
