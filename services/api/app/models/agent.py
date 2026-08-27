from datetime import datetime

from sqlalchemy import DateTime, String, func
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Agent(Base):
    __tablename__ = "agents"

    agent_id: Mapped[str] = mapped_column(String(255), primary_key=True)
    agent_type: Mapped[str] = mapped_column(String(100), nullable=False)
    node_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    status: Mapped[str] = mapped_column(String(50), nullable=False)
    capabilities: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    tools: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    permissions: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    state: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
