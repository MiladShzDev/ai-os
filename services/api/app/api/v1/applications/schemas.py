from pydantic import BaseModel, Field


class ApplicationCreate(BaseModel):
    application_id: str = Field(min_length=1, max_length=255)
    node_id: str = Field(min_length=1, max_length=255)
    package_id: str = Field(min_length=1, max_length=255)
    name: str = Field(min_length=1, max_length=255)
    version: str = Field(min_length=1, max_length=100)
    install_state: str = Field(min_length=1, max_length=50)
    launch_info: dict
    capabilities: list
    store_metadata: dict


class ApplicationResponse(ApplicationCreate):
    pass


class ApplicationUpdate(BaseModel):
    node_id: str | None = Field(default=None, min_length=1, max_length=255)
    package_id: str | None = Field(default=None, min_length=1, max_length=255)
    name: str | None = Field(default=None, min_length=1, max_length=255)
    version: str | None = Field(default=None, min_length=1, max_length=100)
    install_state: str | None = Field(default=None, min_length=1, max_length=50)
    launch_info: dict | None = None
    capabilities: list | None = None
    store_metadata: dict | None = None
