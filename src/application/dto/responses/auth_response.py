"""Authentication response DTOs."""

from pydantic import BaseModel, Field


class TokenResponse(BaseModel):
    """DTO for authentication token response."""

    access_token: str
    refresh_token: str
    token_type: str = Field(default="bearer")

    model_config = {
        "json_schema_extra": {
            "example": {
                "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "refresh_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                "token_type": "bearer",
            }
        }
    }
