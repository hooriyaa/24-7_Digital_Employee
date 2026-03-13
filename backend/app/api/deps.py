"""
API routes and dependencies.

Authentication and authorization dependencies for protected endpoints.
"""
from typing import Annotated, Optional

from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer

from app.core.security import decode_access_token, decode_refresh_token
from app.schemas.token import TokenData
from app.schemas.user import UserInDB

# OAuth2 scheme for Bearer token authentication
# The tokenUrl points to the login endpoint
oauth2_scheme = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login",
    scheme_name="JWT",
    description="JWT Bearer token for authentication",
)

# Optional OAuth2 scheme for endpoints that don't require auth
oauth2_scheme_optional = OAuth2PasswordBearer(
    tokenUrl="/api/v1/auth/login",
    scheme_name="JWT",
    auto_error=False,
)


async def get_current_user(
    token: Annotated[str, Depends(oauth2_scheme)]
) -> UserInDB:
    """
    Get current authenticated user from JWT token.
    
    This dependency is used for protected endpoints that require authentication.
    
    Args:
        token: JWT Bearer token from Authorization header
        
    Returns:
        UserInDB: The authenticated user
        
    Raises:
        HTTPException: 401 if token is invalid or user not found
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    # Decode and validate token
    payload = decode_access_token(token)
    
    if payload is None:
        raise credentials_exception
    
    # Extract user information from token
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception
    
    token_data = TokenData(
        sub=email,
        exp=payload.get("exp"),
        iat=payload.get("iat"),
        type=payload.get("type"),
        email=payload.get("email"),
        role=payload.get("role"),
    )
    
    # TODO: Fetch user from database
    # For now, return a mock user
    # In production, this should query the database
    # user = await get_user_by_email(email)
    # if user is None:
    #     raise credentials_exception
    
    # Mock user for development
    user = UserInDB(
        id="00000000-0000-0000-0000-000000000000",
        email=email,
        name="Test User",
        role=token_data.role or "agent",
        is_active=True,
        created_at=payload.get("iat"),
        updated_at=payload.get("iat"),
        hashed_password="$2b$12$mockhashedpassword",
    )
    
    return user


async def get_current_user_optional(
    token: Annotated[Optional[str], Depends(oauth2_scheme_optional)]
) -> Optional[UserInDB]:
    """
    Get current user if authenticated, otherwise return None.
    
    This dependency is used for endpoints that work for both
    authenticated and anonymous users.
    
    Args:
        token: Optional JWT Bearer token
        
    Returns:
        UserInDB | None: The authenticated user or None
    """
    if token is None:
        return None
    
    try:
        return await get_current_user(token)
    except HTTPException:
        return None


async def get_current_active_user(
    current_user: Annotated[UserInDB, Depends(get_current_user)]
) -> UserInDB:
    """
    Get current active user.
    
    Additional check to ensure the user account is active.
    
    Args:
        current_user: The authenticated user
        
    Returns:
        UserInDB: The active user
        
    Raises:
        HTTPException: 403 if user is inactive
    """
    if not current_user.is_active:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Inactive user account",
        )
    return current_user


async def get_current_admin_user(
    current_user: Annotated[UserInDB, Depends(get_current_user)]
) -> UserInDB:
    """
    Get current admin user.
    
    Requires user to have admin role.
    
    Args:
        current_user: The authenticated user
        
    Returns:
        UserInDB: The admin user
        
    Raises:
        HTTPException: 403 if user is not an admin
    """
    if current_user.role != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required",
        )
    return current_user


def verify_refresh_token(
    token: str
) -> TokenData:
    """
    Verify refresh token and return token data.
    
    Args:
        token: JWT refresh token
        
    Returns:
        TokenData: Decoded token data
        
    Raises:
        HTTPException: 401 if token is invalid
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Invalid refresh token",
        headers={"WWW-Authenticate": "Bearer"},
    )
    
    payload = decode_refresh_token(token)
    
    if payload is None:
        raise credentials_exception
    
    email: str = payload.get("sub")
    if email is None:
        raise credentials_exception
    
    return TokenData(
        sub=email,
        exp=payload.get("exp"),
        iat=payload.get("iat"),
        type=payload.get("type"),
        email=payload.get("email"),
        role=payload.get("role"),
    )
