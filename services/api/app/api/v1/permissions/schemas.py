from datetime import datetime

from pydantic import BaseModel, Field


class PermissionCreate(BaseModel):
    permission_id: str = Field(min_length=1, max_length=255)
    subject: str = Field(min_length=1, max_length=255)
    capability: str = Field(min_length=1, max_length=255)
    scope: dict
    policy: str = Field(min_length=1, max_length=100)
    decision: str = Field(min_length=1, max_length=50)
    confirmation_required: bool = False
    expires_at: datetime | None = None


class PermissionResponse(PermissionCreate):
    pass


class PermissionUpdate(BaseModel):
    subject: str | None = Field(default=None, min_length=1, max_length=255)
    capability: str | None = Field(default=None, min_length=1, max_length=255)
    scope: dict | None = None
    policy: str | None = Field(default=None, min_length=1, max_length=100)
    decision: str | None = Field(default=None, min_length=1, max_length=50)
    confirmation_required: bool | None = None
    expires_at: datetime | None = None
