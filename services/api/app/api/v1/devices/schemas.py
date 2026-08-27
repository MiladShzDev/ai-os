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
