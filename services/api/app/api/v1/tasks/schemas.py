from datetime import datetime

from pydantic import BaseModel, Field


class TaskCreate(BaseModel):
    task_id: str = Field(min_length=1, max_length=255)
    parent_task_id: str | None = None
    request: str = Field(min_length=1)
    intent: str | None = Field(default=None, max_length=255)
    target_nodes: list
    selected_agents: list
    required_capabilities: list
    state: str = Field(min_length=1, max_length=50)
    priority: str = Field(min_length=1, max_length=50)
    created_at: datetime
    updated_at: datetime
    result: dict | None = None
    error: dict | None = None


class TaskResponse(TaskCreate):
    pass


class TaskUpdate(BaseModel):
    parent_task_id: str | None = None
    intent: str | None = Field(default=None, max_length=255)
    target_nodes: list | None = None
    selected_agents: list | None = None
    required_capabilities: list | None = None
    state: str | None = Field(default=None, min_length=1, max_length=50)
    priority: str | None = Field(default=None, min_length=1, max_length=50)
    result: dict | None = None
    error: dict | None = None
