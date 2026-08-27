from sqlalchemy import String
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column

from .base import Base


class Application(Base):
    __tablename__ = "applications"

    application_id: Mapped[str] = mapped_column(String(255), primary_key=True)
    node_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    package_id: Mapped[str] = mapped_column(String(255), nullable=False, index=True)
    name: Mapped[str] = mapped_column(String(255), nullable=False)
    version: Mapped[str] = mapped_column(String(100), nullable=False)
    install_state: Mapped[str] = mapped_column(String(50), nullable=False)
    launch_info: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
    capabilities: Mapped[list] = mapped_column(JSONB, nullable=False, default=list)
    store_metadata: Mapped[dict] = mapped_column(JSONB, nullable=False, default=dict)
