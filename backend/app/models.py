"""
SQLModel database models for the todo application.

This module defines the core database entities:
- User: Authentication and account management
- Todo: Task items owned by users (to be added in future tasks)

All models use UUID primary keys and include created_at/updated_at timestamps.
"""
from sqlmodel import SQLModel, Field, Relationship
from datetime import datetime
from uuid import UUID, uuid4
from typing import Optional, List, Literal
from passlib.context import CryptContext
import sqlalchemy as sa

# Priority level type for todos
PriorityLevel = Literal["high", "normal"]

# Password hashing context (bcrypt with 12 salt rounds)
pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


class User(SQLModel, table=True):
    """
    User database model for authentication and account management.

    Attributes:
        id: Unique identifier (UUID, auto-generated)
        email: Login email address (unique, indexed)
        hashed_password: Bcrypt-hashed password (never store plain text)
        name: User's display name (optional)
        created_at: Account creation timestamp
        updated_at: Last update timestamp

    Relationships:
        todos: One-to-many relationship with Todo items

    Security:
        - Passwords are hashed with bcrypt (12 salt rounds)
        - Email is unique and indexed for fast login queries
        - UUID primary key for security and distributed systems
    """
    __tablename__ = "user"

    # Primary Key
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        nullable=False,
        description="Unique user identifier"
    )

    # Authentication
    email: str = Field(
        max_length=255,
        unique=True,
        index=True,
        nullable=False,
        description="Login email address (unique, indexed)"
    )
    hashed_password: str = Field(
        max_length=255,
        nullable=False,
        description="Bcrypt-hashed password (never plain text)"
    )

    # Profile
    name: Optional[str] = Field(
        default=None,
        max_length=255,
        nullable=True,
        description="User's display name"
    )

    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        index=True,
        description="Account creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Last update timestamp"
    )

    # Relationships
    todos: List["Todo"] = Relationship(
        back_populates="owner",
        sa_relationship_kwargs={"cascade": "all, delete-orphan"}
    )

    def verify_password(self, plain_password: str) -> bool:
        """
        Verify a plain password against the hashed password.

        Args:
            plain_password: The plain text password to verify

        Returns:
            True if password matches, False otherwise
        """
        return pwd_context.verify(plain_password, self.hashed_password)

    @staticmethod
    def hash_password(plain_password: str) -> str:
        """
        Hash a plain password using bcrypt.

        Args:
            plain_password: The plain text password to hash

        Returns:
            Bcrypt-hashed password string
        """
        return pwd_context.hash(plain_password)

    class Config:
        """SQLModel configuration"""
        json_schema_extra = {
            "example": {
                "email": "user@example.com",
                "name": "John Doe",
            }
        }


class Todo(SQLModel, table=True):
    """
    Todo database model for task management.

    Attributes:
        id: Unique identifier (UUID, auto-generated)
        user_id: Owner of the todo (foreign key to users.id)
        title: Todo title/summary (max 500 characters)
        description: Optional detailed description (unlimited text)
        completed: Completion status (default: False)
        priority: Priority level - "high" or "normal" (default: "normal")
        created_at: Creation timestamp
        updated_at: Last update timestamp

    Relationships:
        owner: Many-to-one relationship with User

    Security:
        - All queries MUST filter by user_id to prevent cross-user data access
        - User ID extracted from JWT token (NEVER from request body)
        - Ownership verification required before UPDATE/DELETE operations
        - Foreign key with CASCADE delete ensures cleanup when user is deleted

    Performance:
        - user_id indexed for fast user-scoped queries
        - completed indexed for filtering by status
        - created_at indexed for sorting by creation date
    """
    __tablename__ = "todo"

    # Primary Key
    id: UUID = Field(
        default_factory=uuid4,
        primary_key=True,
        nullable=False,
        description="Unique todo identifier"
    )

    # Foreign Key to User
    user_id: UUID = Field(
        foreign_key="user.id",
        nullable=False,
        index=True,
        description="Owner of the todo (foreign key to users.id, CASCADE on delete)"
    )

    # Todo Fields
    title: str = Field(
        max_length=500,
        nullable=False,
        index=True,  # Index for search queries
        description="Todo title/summary (1-500 characters)"
    )
    description: Optional[str] = Field(
        default=None,
        nullable=True,
        description="Optional detailed description (0-2000 characters)"
    )
    completed: bool = Field(
        default=False,
        nullable=False,
        index=True,  # Index for filtering by completion status
        description="Completion status (default: False)"
    )
    priority: str = Field(
        default="normal",
        description="Priority level: 'high' or 'normal' (default: normal)",
        sa_column=sa.Column(sa.String(20), nullable=False, index=True, default="normal")
    )

    # Timestamps
    created_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        index=True,  # Index for sorting by creation date
        description="Creation timestamp"
    )
    updated_at: datetime = Field(
        default_factory=datetime.utcnow,
        nullable=False,
        description="Last update timestamp"
    )

    # Relationships
    owner: Optional[User] = Relationship(back_populates="todos")

    class Config:
        """SQLModel configuration"""
        json_schema_extra = {
            "example": {
                "title": "Buy groceries",
                "description": "Milk, eggs, bread, and coffee",
                "completed": False,
            }
        }
