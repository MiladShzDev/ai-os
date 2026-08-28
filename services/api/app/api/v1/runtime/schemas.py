from pydantic import BaseModel, Field


class RuntimeExecuteRequest(BaseModel):
    task_id: str = Field(min_length=1, max_length=255)


class RuntimeExecuteResponse(BaseModel):
    task_id: str
    state: str
    selected_agents: list
