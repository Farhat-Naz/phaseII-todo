"""
Authentication endpoints for user registration, login, and profile access.

This module implements secure JWT-based authentication with:
- User registration with email uniqueness validation
- Login with credential verification
- Protected route for getting current user profile

Security Features:
- Passwords are hashed with bcrypt (12 salt rounds)
- JWT tokens with configurable expiration
- Generic error messages to prevent user enumeration
- Email uniqueness enforcement at database level

Endpoints:
- POST /api/auth/register - Create new user account
- POST /api/auth/login - Authenticate and get JWT token
- GET /api/auth/me - Get current authenticated user profile
"""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from typing import Annotated

from app.database import get_db
from app.models import User
from app.schemas import UserRegister, UserLogin, Token, UserPublic
from app.dependencies import get_current_user, CurrentUser
# Placeholder import - will be implemented by auth-config-specialist agent
from app.auth import create_access_token

# Create router with tags for API documentation
router = APIRouter(
    tags=["Authentication"],
    responses={
        401: {"description": "Unauthorized - Invalid or expired token"},
        422: {"description": "Validation Error - Invalid request data"},
    },
)


@router.post(
    "/register",
    response_model=Token,
    status_code=status.HTTP_201_CREATED,
    summary="Register new user",
    description="Create a new user account with email, password, and name. "
                "Email must be unique. Password must meet complexity requirements.",
    responses={
        201: {
            "description": "User successfully registered",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "token_type": "bearer",
                        "user": {
                            "id": "123e4567-e89b-12d3-a456-426614174000",
                            "email": "user@example.com",
                            "name": "John Doe"
                        }
                    }
                }
            }
        },
        400: {
            "description": "Email already registered",
            "content": {
                "application/json": {
                    "example": {"detail": "Email already registered"}
                }
            }
        },
    }
)
async def register(
    user_data: UserRegister,
    db: Annotated[Session, Depends(get_db)]
) -> Token:
    """
    Register a new user account.

    Process:
    1. Validate email uniqueness
    2. Hash password with bcrypt
    3. Create user record in database
    4. Generate JWT access token
    5. Return token and user data

    Args:
        user_data: Registration data (email, password, name)
        db: Database session dependency

    Returns:
        Token: JWT token and public user data

    Raises:
        HTTPException 400: If email is already registered
        HTTPException 422: If validation fails (automatic from Pydantic)
    """
    # Check if email already exists
    statement = select(User).where(User.email == user_data.email)
    existing_user = db.exec(statement).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Email already registered"
        )

    # Hash password using User model's static method
    hashed_password = User.hash_password(user_data.password)

    # Create new user
    new_user = User(
        email=user_data.email,
        hashed_password=hashed_password,
        name=user_data.name
    )

    # Save to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    # Generate JWT access token
    access_token = create_access_token(data={"sub": str(new_user.id)})

    # Return token and user data
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=UserPublic.model_validate(new_user)
    )


@router.post(
    "/login",
    response_model=Token,
    status_code=status.HTTP_200_OK,
    summary="Login user",
    description="Authenticate with email and password. Returns JWT token on success.",
    responses={
        200: {
            "description": "Login successful",
            "content": {
                "application/json": {
                    "example": {
                        "access_token": "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9...",
                        "token_type": "bearer",
                        "user": {
                            "id": "123e4567-e89b-12d3-a456-426614174000",
                            "email": "user@example.com",
                            "name": "John Doe"
                        }
                    }
                }
            }
        },
        401: {
            "description": "Invalid credentials",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid credentials"}
                }
            }
        },
    }
)
async def login(
    credentials: UserLogin,
    db: Annotated[Session, Depends(get_db)]
) -> Token:
    """
    Authenticate user with email and password.

    Security:
    - Returns generic "Invalid credentials" message for both:
      - Email not found
      - Incorrect password
    - This prevents user enumeration attacks

    Process:
    1. Query user by email
    2. Verify password hash
    3. Generate JWT access token
    4. Return token and user data

    Args:
        credentials: Login credentials (email, password)
        db: Database session dependency

    Returns:
        Token: JWT token and public user data

    Raises:
        HTTPException 401: If email not found or password incorrect
        HTTPException 422: If validation fails (automatic from Pydantic)
    """
    # Query user by email
    statement = select(User).where(User.email == credentials.email)
    user = db.exec(statement).first()

    # Check if user exists and password is correct
    # Use generic error message to prevent user enumeration
    if not user or not user.verify_password(credentials.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Generate JWT access token
    access_token = create_access_token(data={"sub": str(user.id)})

    # Return token and user data
    return Token(
        access_token=access_token,
        token_type="bearer",
        user=UserPublic.model_validate(user)
    )


@router.get(
    "/me",
    response_model=UserPublic,
    status_code=status.HTTP_200_OK,
    summary="Get current user",
    description="Get the authenticated user's profile information. Requires valid JWT token.",
    responses={
        200: {
            "description": "Current user profile",
            "content": {
                "application/json": {
                    "example": {
                        "id": "123e4567-e89b-12d3-a456-426614174000",
                        "email": "user@example.com",
                        "name": "John Doe"
                    }
                }
            }
        },
        401: {
            "description": "Not authenticated or token invalid",
            "content": {
                "application/json": {
                    "example": {"detail": "Invalid authentication credentials"}
                }
            }
        },
    }
)
async def get_me(current_user: CurrentUser) -> UserPublic:
    """
    Get the current authenticated user's profile.

    This endpoint demonstrates the authentication dependency pattern.
    The get_current_user dependency:
    - Validates JWT token
    - Verifies user exists in database
    - Returns User model instance
    - Raises 401 if token invalid or user not found

    Args:
        current_user: Authenticated user from JWT token (injected by dependency)

    Returns:
        UserPublic: Current user's public profile data (excludes password)

    Raises:
        HTTPException 401: If token is invalid, expired, or user not found
    """
    return UserPublic.model_validate(current_user)


# Future endpoints:
# - POST /auth/refresh - Refresh access token using refresh token
# - POST /auth/logout - Invalidate tokens (requires token blacklist)
# - POST /auth/forgot-password - Request password reset email
# - POST /auth/reset-password - Reset password with token
# - POST /auth/verify-email - Verify email address with token
# - POST /auth/resend-verification - Resend verification email
