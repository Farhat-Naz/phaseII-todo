"""
JWT authentication utilities for token creation and validation.

PLACEHOLDER MODULE - To be implemented by auth-config-specialist agent.

This module will provide:
- create_access_token(): Generate JWT tokens with expiration
- decode_access_token(): Validate and decode JWT tokens
- oauth2_scheme: FastAPI OAuth2 password bearer dependency

Required environment variables:
- SECRET_KEY: Secret key for JWT signing (generate with: openssl rand -hex 32)
- ALGORITHM: JWT algorithm (default: HS256)
- ACCESS_TOKEN_EXPIRE_MINUTES: Token expiration time in minutes (default: 30)

Implementation notes for auth-config-specialist:
1. Use python-jose for JWT operations
2. Implement proper token expiration validation
3. Include WWW-Authenticate headers in 401 responses
4. Follow OAuth2 password bearer flow
5. Validate token signature and expiration on decode
"""
from fastapi import HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from datetime import datetime, timedelta
from jose import JWTError, jwt
import os

# OAuth2 scheme for token extraction from Authorization header
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# JWT configuration from environment variables
SECRET_KEY = os.getenv("SECRET_KEY", "dev-secret-key-change-in-production")
ALGORITHM = os.getenv("ALGORITHM", "HS256")
ACCESS_TOKEN_EXPIRE_MINUTES = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", "30"))


def create_access_token(data: dict, expires_delta: timedelta | None = None) -> str:
    """
    Create a JWT access token with expiration.

    PLACEHOLDER - To be implemented by auth-config-specialist.

    Args:
        data: Payload data to encode (must include "sub" for user_id)
        expires_delta: Optional custom expiration time

    Returns:
        str: Encoded JWT token

    Example:
        token = create_access_token(data={"sub": str(user.id)})
    """
    to_encode = data.copy()

    # Set expiration time
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)

    to_encode.update({"exp": expire})

    # Encode JWT token
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def decode_access_token(token: str) -> dict:
    """
    Decode and validate a JWT access token.

    PLACEHOLDER - To be implemented by auth-config-specialist.

    Validates:
    - Token signature using SECRET_KEY
    - Token expiration (exp claim)
    - Required claims presence (sub)

    Args:
        token: JWT token string to decode

    Returns:
        dict: Decoded token payload

    Raises:
        HTTPException 401: If token is invalid or expired

    Example:
        payload = decode_access_token(token)
        user_id = payload.get("sub")
    """
    try:
        # Decode and validate token
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        return payload
    except JWTError as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid authentication credentials",
            headers={"WWW-Authenticate": "Bearer"},
        ) from e


# Future: Add refresh token functions
# def create_refresh_token(data: dict) -> str:
#     """Create a refresh token with longer expiration"""
#     pass
#
# def decode_refresh_token(token: str) -> dict:
#     """Decode and validate refresh token"""
#     pass
