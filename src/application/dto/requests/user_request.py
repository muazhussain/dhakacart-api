"""User request DTOs for API input validation."""

from pydantic import BaseModel, EmailStr, Field


class RegisterUserRequest(BaseModel):
    """DTO for user registration request."""

    email: EmailStr
    password: str = Field(..., min_length=8, max_length=128)
    full_name: str = Field(..., min_length=2, max_length=100)
    phone: str | None

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "user@example.com",
                    "password": "SecurePass123",
                    "full_name": "John Doe",
                    "phone": "+8801712345678",
                }
            ]
        }
    }
