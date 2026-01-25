"""Authentication request DTOs."""

from pydantic import BaseModel, EmailStr, Field


class LoginRequest(BaseModel):
    """DTO for user requst."""

    email: EmailStr
    password: str = Field(..., min_length=1, max_length=128)

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "user@example.com",
                    "password": "SecurePass123",
                }
            ]
        }
    }


class RefreshTokenRequest(BaseModel):
    """DTO for token refresh request."""

    refresh_token: str = Field(..., min_length=1)
