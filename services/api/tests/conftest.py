import pytest

from app.db import SessionLocal
from app.models.agent import Agent
from app.models.device import Device
from app.models.permission import Permission
from app.models.task import Task


@pytest.fixture
def db_session():
    db = SessionLocal()

    try:
        yield db
    finally:
        db.rollback()

        db.query(Permission).delete()
        db.query(Device).delete()
        db.query(Agent).delete()
        db.query(Task).delete()

        db.commit()
        db.close()
