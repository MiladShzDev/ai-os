from pydantic import BaseModel, Field


class CapabilityCreate(BaseModel):
    capability_id: str = Field(min_length=1, max_length=255)
    name: str = Field(min_length=1, max_length=255)
    description: str = Field(min_length=1, max_length=1000)
    platforms: list
    risk_level: str = Field(min_length=1, max_length=50)
    execution_scope: str = Field(min_length=1, max_length=50)
    input_schema: dict
    output_schema: dict


class CapabilityResponse(CapabilityCreate):
    pass


class CapabilityUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    description: str | None = Field(default=None, min_length=1, max_length=1000)
    platforms: list | None = None
    risk_level: str | None = Field(default=None, min_length=1, max_length=50)
    execution_scope: str | None = Field(default=None, min_length=1, max_length=50)
    input_schema: dict | None = None
    output_schema: dict | None = None
