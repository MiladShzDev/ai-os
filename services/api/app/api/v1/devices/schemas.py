from datetime import datetime

from pydantic import BaseModel


class DeviceCreate(BaseModel):
    node_id: str
    node_type: str
    platform: str
    version: str
    status: str
    capabilities: list
    agent_id: str
    last_seen: datetime


class DeviceResponse(DeviceCreate):
    pass


class DeviceUpdate(BaseModel):
    node_type: str | None = None
    platform: str | None = None
    version: str | None = None
    status: str | None = None
    capabilities: list | None = None
    agent_id: str | None = None
    last_seen: datetime | None = None
