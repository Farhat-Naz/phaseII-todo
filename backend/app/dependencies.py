"""
FastAPI dependency injection functions for authentication and database sessions.

This module provides reusable dependencies for:
- Current user extraction from JWT tokens
- Database session management
- Future: Role-based access control, rate limiting, etc.

Security Pattern:
- JWT tokens are validated on every request
- User existence is verified in database
- Invalid/expired tokens return 401 Unauthorized
- All protected endpoints use Depends(get_current_user)
"""
from fastapi import Depends, HTTPException, status
from sqlmodel import Session, select
from typing import Annotated
from uuid import UUID

from app.database import get_db
from app.models import User
# Placeholder imports - will be implemented by auth-config-specialist agent
from app.auth import decode_access_token, oauth2_scheme


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)],
    db: Annotated[Session, Depends(get_db)]
) -> User:
    """
    Extract and validate the current authenticated user from JWT token.

    This dependency:
    1. Extracts the JWT token from Authorization header (via oauth2_scheme)
    2. Decodes and validates the token signature and expiration
    3. Extracts user_id from the "sub" claim
    4. Queries database to verify user exists
    5. Returns User model instance

    Security:
    - Token signature is verified using SECRET_KEY
    - Token expiration is checked
    - User existence is verified in database
    - Returns 401 if any validation fails

    Args:
        token: JWT token string from Authorization header
        db: Database session dependency

    Returns:
        User: Authenticated user model instance

    Raises:
        HTTPException 401: If token is invalid, expired, or user not found

    Example:
        @app.get("/protected")
        def protected_route(current_user: User = Depends(get_current_user)):
            return {"user_id": current_user.id, "email": current_user.email}
    """
    # Decode and validate JWT token
    # This will raise HTTPException 401 if token is invalid or expired
    payload = decode_access_token(token)

    # Extract user_id from "sub" claim
    user_id_str: str | None = payload.get("sub")
    if user_id_str is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Convert string UUID to UUID object
    try:
        user_id = UUID(user_id_str)
    except ValueError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user ID format in token",
            headers={"WWW-Authenticate": "Bearer"},
        )

    # Query database for user
    statement = select(User).where(User.id == user_id)
    user = db.exec(statement).first()

    if user is None:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    return user


async def get_current_user_optional(
    token: Annotated[str | None, Depends(oauth2_scheme)] = None,
    db: Annotated[Session, Depends(get_db)] = None
) -> User | None:
    """
    Optional authentication dependency for endpoints that support both
    authenticated and unauthenticated access.

    Returns None if no token is provided or if token is invalid.
    Use this for public endpoints that show additional data for logged-in users.

    Args:
        token: Optional JWT token from Authorization header
        db: Database session dependency

    Returns:
        User | None: User if authenticated, None otherwise

    Example:
        @app.get("/public")
        def public_route(current_user: User | None = Depends(get_current_user_optional)):
            if current_user:
                return {"message": f"Hello {current_user.name}"}
            return {"message": "Hello guest"}
    """
    if token is None:
        return None

    try:
        return await get_current_user(token, db)
    except HTTPException:
        return None


# Type alias for cleaner dependency injection
CurrentUser = Annotated[User, Depends(get_current_user)]
OptionalCurrentUser = Annotated[User | None, Depends(get_current_user_optional)]


# Future dependencies:
# - get_current_active_user (checks user.is_active flag)
# - get_current_superuser (checks user.is_superuser flag)
# - get_current_verified_user (checks user.email_verified flag)
# - rate_limiter (rate limiting per user/IP)
# - pagination_params (page, limit validation)
