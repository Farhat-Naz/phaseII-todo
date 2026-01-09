"""
Pydantic schemas for request/response validation.

This module defines all API data models using Pydantic v2:
- User authentication schemas (register, login, token)
- User public schemas (excludes sensitive data like passwords)
- Todo schemas (to be added in future tasks)

All schemas include field validation and examples for API documentation.
"""
from pydantic import BaseModel, EmailStr, Field, field_validator
from uuid import UUID
from typing import Optional, Literal
from datetime import datetime
import re

# Priority level type for todos (must match models.py)
PriorityLevel = Literal["high", "normal"]


class UserRegister(BaseModel):
    """
    User registration request schema.

    Validates:
    - Email format (EmailStr)
    - Password strength (min 8 chars, 1 uppercase, 1 lowercase, 1 number)
    - Name presence
    """
    email: EmailStr = Field(
        ...,
        description="User email address (must be unique)",
        examples=["user@example.com"]
    )
    password: str = Field(
        ...,
        min_length=8,
        description="Password (min 8 chars, 1 uppercase, 1 lowercase, 1 number)",
        examples=["SecurePass123"]
    )
    name: str = Field(
        ...,
        min_length=1,
        max_length=255,
        description="User's display name",
        examples=["John Doe"]
    )

    @field_validator("password")
    @classmethod
    def validate_password_complexity(cls, v: str) -> str:
        """
        Validate password complexity requirements.

        Requirements:
        - At least 8 characters (enforced by Field min_length)
        - At least 1 uppercase letter
        - At least 1 lowercase letter
        - At least 1 number

        Args:
            v: Password string to validate

        Returns:
            str: Validated password

        Raises:
            ValueError: If password doesn't meet complexity requirements
        """
        if not re.search(r"[A-Z]", v):
            raise ValueError("Password must contain at least 1 uppercase letter")
        if not re.search(r"[a-z]", v):
            raise ValueError("Password must contain at least 1 lowercase letter")
        if not re.search(r"\d", v):
            raise ValueError("Password must contain at least 1 number")
        return v

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "john.doe@example.com",
                    "password": "SecurePass123",
                    "name": "John Doe"
                }
            ]
        }
    }


class UserLogin(BaseModel):
    """
    User login request schema.

    Validates:
    - Email format
    - Password presence
    """
    email: EmailStr = Field(
        ...,
        description="User email address",
        examples=["user@example.com"]
    )
    password: str = Field(
        ...,
        description="User password",
        examples=["SecurePass123"]
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "email": "john.doe@example.com",
                    "password": "SecurePass123"
                }
            ]
        }
    }


class UserPublic(BaseModel):
    """
    Public user schema (excludes sensitive data).

    Used in responses to avoid exposing:
    - hashed_password
    - Any other sensitive fields

    Includes:
    - id: User UUID
    - email: User email
    - name: User display name
    """
    id: UUID = Field(
        ...,
        description="Unique user identifier",
        examples=["123e4567-e89b-12d3-a456-426614174000"]
    )
    email: str = Field(
        ...,
        description="User email address",
        examples=["user@example.com"]
    )
    name: Optional[str] = Field(
        None,
        description="User's display name",
        examples=["John Doe"]
    )

    model_config = {
        "from_attributes": True,  # Allow creation from ORM models
        "json_schema_extra": {
            "examples": [
                {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "email": "john.doe@example.com",
                    "name": "John Doe"
                }
            ]
        }
    }


class Token(BaseModel):
    """
    JWT token response schema.

    Returned after successful login or registration.

    Fields:
    - access_token: JWT token string
    - token_type: Token type (always "bearer")
    - user: Public user data (excludes password)
    """
    access_token: str = Field(
        ...,
        description="JWT access token",
        examples=["eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9..."]
    )
    token_type: str = Field(
        default="bearer",
        description="Token type (OAuth2 standard)",
        examples=["bearer"]
    )
    user: UserPublic = Field(
        ...,
        description="Authenticated user data (excludes password)"
    )

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJzdWIiOiIxMjM0NTY3ODkwIiwibmFtZSI6IkpvaG4gRG9lIiwiaWF0IjoxNTE2MjM5MDIyfQ.SflKxwRJSMeKKF2QT4fwpMeJf36POk6yJV_adQssw5c",
                    "token_type": "bearer",
                    "user": {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "email": "john.doe@example.com",
                        "name": "John Doe"
                    }
                }
            ]
        }
    }


# ============================================
# Todo Schemas
# ============================================


class TodoCreate(BaseModel):
    """
    Todo creation request schema.

    Validates:
    - Title presence and length (1-500 characters)
    - Description length (max 2000 characters)
    - Completed status (defaults to False)

    Security:
    - user_id is NEVER accepted from request body
    - user_id is always extracted from JWT token (current_user.id)
    """
    title: str = Field(
        ...,
        min_length=1,
        max_length=500,
        description="Todo title/summary (1-500 characters, required)",
        examples=["Buy groceries"]
    )
    description: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="Optional detailed description (max 2000 characters)",
        examples=["Milk, eggs, bread, and coffee"]
    )
    completed: bool = Field(
        default=False,
        description="Completion status (defaults to False)",
        examples=[False]
    )
    priority: PriorityLevel = Field(
        default="normal",
        description="Priority level: 'high' or 'normal' (defaults to 'normal')",
        examples=["normal"]
    )

    @field_validator("title")
    @classmethod
    def validate_title_not_blank(cls, v: str) -> str:
        """
        Validate that title is not just whitespace.

        Args:
            v: Title string to validate

        Returns:
            str: Validated and stripped title

        Raises:
            ValueError: If title is empty or only whitespace
        """
        stripped = v.strip()
        if not stripped:
            raise ValueError("Title cannot be empty or only whitespace")
        return stripped

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "title": "Buy groceries",
                    "description": "Milk, eggs, bread, and coffee",
                    "completed": False
                }
            ]
        }
    }


class TodoUpdate(BaseModel):
    """
    Todo update request schema (PATCH - partial update).

    All fields are optional for PATCH semantics:
    - Only provided fields will be updated
    - Omitted fields remain unchanged
    - Allows toggling completion status without modifying other fields

    Security:
    - Ownership verification required before update
    - user_id cannot be changed (enforced at endpoint level)
    """
    title: Optional[str] = Field(
        default=None,
        min_length=1,
        max_length=500,
        description="Todo title/summary (1-500 characters, optional)",
        examples=["Buy groceries and cleaning supplies"]
    )
    description: Optional[str] = Field(
        default=None,
        max_length=2000,
        description="Detailed description (max 2000 characters, optional)",
        examples=["Milk, eggs, bread, coffee, and dish soap"]
    )
    completed: Optional[bool] = Field(
        default=None,
        description="Completion status (optional)",
        examples=[True]
    )
    priority: Optional[PriorityLevel] = Field(
        default=None,
        description="Priority level: 'high' or 'normal' (optional)",
        examples=["high"]
    )

    @field_validator("title")
    @classmethod
    def validate_title_not_blank(cls, v: Optional[str]) -> Optional[str]:
        """
        Validate that title is not just whitespace if provided.

        Args:
            v: Title string to validate (or None)

        Returns:
            str | None: Validated and stripped title, or None

        Raises:
            ValueError: If title is empty or only whitespace
        """
        if v is None:
            return None
        stripped = v.strip()
        if not stripped:
            raise ValueError("Title cannot be empty or only whitespace")
        return stripped

    model_config = {
        "json_schema_extra": {
            "examples": [
                {
                    "completed": True
                },
                {
                    "title": "Buy groceries and cleaning supplies",
                    "description": "Milk, eggs, bread, coffee, and dish soap"
                },
                {
                    "title": "Updated title",
                    "description": "Updated description",
                    "completed": False
                }
            ]
        }
    }


class TodoPublic(BaseModel):
    """
    Public todo schema for API responses.

    Includes all todo data that should be visible to the owner.
    Never includes data from other users' todos.

    Fields:
    - id: Unique todo identifier (UUID)
    - user_id: Owner's user ID (UUID)
    - title: Todo title/summary
    - description: Optional detailed description
    - completed: Completion status
    - priority: Priority level ('high' or 'normal')
    - created_at: Creation timestamp
    - updated_at: Last update timestamp
    """
    id: UUID = Field(
        ...,
        description="Unique todo identifier",
        examples=["123e4567-e89b-12d3-a456-426614174000"]
    )
    user_id: UUID = Field(
        ...,
        description="Owner's user ID (foreign key to users.id)",
        examples=["789e4567-e89b-12d3-a456-426614174999"]
    )
    title: str = Field(
        ...,
        description="Todo title/summary",
        examples=["Buy groceries"]
    )
    description: Optional[str] = Field(
        default=None,
        description="Optional detailed description",
        examples=["Milk, eggs, bread, and coffee"]
    )
    completed: bool = Field(
        ...,
        description="Completion status",
        examples=[False]
    )
    priority: PriorityLevel = Field(
        ...,
        description="Priority level: 'high' or 'normal'",
        examples=["normal"]
    )
    created_at: datetime = Field(
        ...,
        description="Creation timestamp (UTC)",
        examples=["2024-01-15T10:30:00Z"]
    )
    updated_at: datetime = Field(
        ...,
        description="Last update timestamp (UTC)",
        examples=["2024-01-15T14:45:00Z"]
    )

    model_config = {
        "from_attributes": True,  # Allow creation from SQLModel ORM models
        "json_schema_extra": {
            "examples": [
                {
                    "id": "123e4567-e89b-12d3-a456-426614174000",
                    "user_id": "789e4567-e89b-12d3-a456-426614174999",
                    "title": "Buy groceries",
                    "description": "Milk, eggs, bread, and coffee",
                    "completed": False,
                    "priority": "normal",
                    "created_at": "2024-01-15T10:30:00Z",
                    "updated_at": "2024-01-15T14:45:00Z"
                }
            ]
        }
    }
