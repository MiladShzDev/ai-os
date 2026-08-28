from datetime import datetime

from pydantic import BaseModel, Field


class DeviceCreate(BaseModel):
    node_id: str = Field(min_length=1, max_length=255)
    node_type: str = Field(min_length=1, max_length=100)
    platform: str = Field(min_length=1, max_length=100)
    version: str = Field(min_length=1, max_length=100)
    status: str = Field(min_length=1, max_length=50)
    capabilities: list
    agent_id: str = Field(min_length=1, max_length=255)
    last_seen: datetime


class DeviceResponse(DeviceCreate):
    pass


class DeviceUpdate(BaseModel):
    node_type: str | None = Field(default=None, min_length=1, max_length=100)
    platform: str | None = Field(default=None, min_length=1, max_length=100)
    version: str | None = Field(default=None, min_length=1, max_length=100)
    status: str | None = Field(default=None, min_length=1, max_length=50)
    capabilities: list | None = None
    agent_id: str | None = Field(default=None, min_length=1, max_length=255)
    last_seen: datetime | None = None
