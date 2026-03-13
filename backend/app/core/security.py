"""
Core security utilities.

JWT token handling, password hashing, and authentication.

Security best practices:
- Bcrypt for password hashing (adaptive cost factor)
- JWT with HS256 algorithm
- Separate access and refresh tokens
- Timing attack prevention in password verification
"""
from datetime import datetime, timedelta, timezone
from typing import Any, Optional

import bcrypt
from jose import JWTError, jwt

from app.config import get_settings

# Get settings
settings = get_settings()


def verify_password(plain_password: str, hashed_password: str) -> bool:
    """
    Verify a password against its hash.
    
    Uses constant-time comparison to prevent timing attacks.

    Args:
        plain_password: The plain text password
        hashed_password: The hashed password

    Returns:
        bool: True if password matches
    """
    try:
        return bcrypt.checkpw(
            plain_password.encode("utf-8"),
            hashed_password.encode("utf-8")
        )
    except Exception:
        return False


def get_password_hash(password: str) -> str:
    """
    Hash a password using bcrypt.
    
    Bcrypt automatically generates a salt and includes it in the hash.

    Args:
        password: The plain text password

    Returns:
        str: The hashed password (bcrypt format)
    """
    return bcrypt.hashpw(
        password.encode("utf-8"),
        bcrypt.gensalt(rounds=12)
    ).decode("utf-8")


def create_access_token(
    data: dict[str, Any],
    expires_delta: timedelta | None = None
) -> str:
    """
    Create a JWT access token.
    
    Access tokens are short-lived and used for API authentication.

    Args:
        data: Token payload data (e.g., {"sub": username})
        expires_delta: Optional custom expiration time

    Returns:
        str: Encoded JWT token
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            minutes=settings.access_token_expire_minutes
        )

    to_encode.update({
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "type": "access"
    })

    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm
    )

    return encoded_jwt


def create_refresh_token(
    data: dict[str, Any],
    expires_delta: timedelta | None = None
) -> str:
    """
    Create a JWT refresh token.
    
    Refresh tokens are long-lived and used to obtain new access tokens.

    Args:
        data: Token payload data (e.g., {"sub": username})
        expires_delta: Optional custom expiration time

    Returns:
        str: Encoded JWT token
    """
    to_encode = data.copy()

    if expires_delta:
        expire = datetime.now(timezone.utc) + expires_delta
    else:
        expire = datetime.now(timezone.utc) + timedelta(
            days=settings.refresh_token_expire_days
        )

    to_encode.update({
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "type": "refresh"
    })

    encoded_jwt = jwt.encode(
        to_encode,
        settings.secret_key,
        algorithm=settings.algorithm
    )

    return encoded_jwt


def decode_access_token(token: str) -> dict[str, Any] | None:
    """
    Decode and validate a JWT access token.
    
    Verifies signature, expiration, and token type.

    Args:
        token: The JWT token

    Returns:
        dict: Token payload or None if invalid
    """
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
            options={"verify_exp": True}
        )
        
        # Verify token type
        if payload.get("type") != "access":
            return None
            
        return payload
    except JWTError:
        return None


def decode_refresh_token(token: str) -> dict[str, Any] | None:
    """
    Decode and validate a JWT refresh token.
    
    Verifies signature, expiration, and token type.

    Args:
        token: The JWT token

    Returns:
        dict: Token payload or None if invalid
    """
    try:
        payload = jwt.decode(
            token,
            settings.secret_key,
            algorithms=[settings.algorithm],
            options={"verify_exp": True}
        )
        
        # Verify token type
        if payload.get("type") != "refresh":
            return None
            
        return payload
    except JWTError:
        return None


def authenticate_user(
    stored_hashed_password: str,
    plain_password: str
) -> bool:
    """
    Authenticate a user by verifying their password.
    
    Includes timing attack prevention by always running
    the verification even if the stored hash is invalid.

    Args:
        stored_hashed_password: The stored hashed password
        plain_password: The plain text password to verify

    Returns:
        bool: True if authentication successful
    """
    if not stored_hashed_password:
        # Run against a dummy hash to prevent timing attacks
        dummy_hash = "$2b$12$dummyhashfortimingattackprevention"
        bcrypt.checkpw(
            plain_password.encode("utf-8"),
            dummy_hash.encode("utf-8")
        )
        return False
    
    return verify_password(plain_password, stored_hashed_password)
