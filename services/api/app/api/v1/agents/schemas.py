from pydantic import BaseModel, Field


class AgentCreate(BaseModel):
    agent_id: str = Field(min_length=1, max_length=255)
    agent_type: str = Field(min_length=1, max_length=100)
    node_id: str = Field(min_length=1, max_length=255)
    status: str = Field(min_length=1, max_length=50)
    capabilities: list
    tools: list
    permissions: list
    state: dict


class AgentResponse(AgentCreate):
    pass


class AgentUpdate(BaseModel):
    agent_type: str | None = Field(default=None, min_length=1, max_length=100)
    node_id: str | None = Field(default=None, min_length=1, max_length=255)
    status: str | None = Field(default=None, min_length=1, max_length=50)
    capabilities: list | None = None
    tools: list | None = None
    permissions: list | None = None
    state: dict | None = None
