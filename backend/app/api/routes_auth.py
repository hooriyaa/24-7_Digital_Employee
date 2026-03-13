"""
Authentication API routes.

Endpoints for user login, token refresh, and logout.
"""
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, status
from fastapi.security import OAuth2PasswordRequestForm

from app.core.security import (
    create_access_token,
    create_refresh_token,
    decode_refresh_token,
    get_password_hash,
    authenticate_user,
)
from app.schemas.token import Token, RefreshTokenRequest, TokenData
from app.schemas.user import UserCreate, UserResponse, UserInDB, LoginRequest
from app.api.deps import get_current_user, verify_refresh_token

router = APIRouter(prefix="/auth", tags=["Authentication"])


@router.post("/login", response_model=Token)
async def login(
    form_data: OAuth2PasswordRequestForm = Depends(),
) -> Token:
    """
    Login to get access and refresh tokens.
    
    Uses OAuth2 password flow. The username should be the user's email.
    
    **Request:**
    - `username`: User email (OAuth2 standard field name)
    - `password`: User password
    - `scope`: Optional scopes (not used in v1.0)
    
    **Response:**
    - `access_token`: Short-lived JWT token (15 minutes)
    - `refresh_token`: Long-lived JWT token (7 days)
    - `token_type`: "bearer"
    - `expires_in`: Access token expiration in seconds
    """
    # For now, use mock authentication
    # In production, fetch user from database by email
    # user = await get_user_by_email(form_data.username)
    # if not user or not authenticate_user(user.hashed_password, form_data.password):
    #     raise HTTPException(
    #         status_code=status.HTTP_401_UNAUTHORIZED,
    #         detail="Incorrect email or password",
    #         headers={"WWW-Authenticate": "Bearer"},
    #     )
    
    # Mock authentication for development
    # Accept any email/password combination for testing
    if not form_data.username or not form_data.password:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Email and password are required",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    # Create mock user
    from datetime import datetime, timezone
    now = datetime.now(timezone.utc)
    
    user = UserInDB(
        id="00000000-0000-0000-0000-000000000000",
        email=form_data.username,
        name="Test User",
        role="agent",
        is_active=True,
        created_at=now,
        updated_at=now,
        hashed_password=get_password_hash(form_data.password),
    )
    
    # Create tokens
    access_token_expires = timedelta(minutes=15)
    access_token = create_access_token(
        data={
            "sub": user.email,
            "email": user.email,
            "role": user.role,
        },
        expires_delta=access_token_expires,
    )
    
    refresh_token = create_refresh_token(
        data={
            "sub": user.email,
            "email": user.email,
            "role": user.role,
        },
    )
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=int(access_token_expires.total_seconds()),
    )


@router.post("/refresh", response_model=Token)
async def refresh_token(
    request: RefreshTokenRequest,
) -> Token:
    """
    Refresh access token using refresh token.
    
    **Request:**
    - `refresh_token`: Valid refresh token
    
    **Response:**
    - New access and refresh tokens
    """
    # Verify refresh token
    token_data = verify_refresh_token(request.refresh_token)
    
    # Create new tokens
    access_token_expires = timedelta(minutes=15)
    access_token = create_access_token(
        data={
            "sub": token_data.sub,
            "email": token_data.email,
            "role": token_data.role,
        },
        expires_delta=access_token_expires,
    )
    
    # Optionally rotate refresh token
    refresh_token = create_refresh_token(
        data={
            "sub": token_data.sub,
            "email": token_data.email,
            "role": token_data.role,
        },
    )
    
    return Token(
        access_token=access_token,
        refresh_token=refresh_token,
        token_type="bearer",
        expires_in=int(access_token_expires.total_seconds()),
    )


@router.get("/me", response_model=UserResponse)
async def get_current_user_info(
    current_user: UserInDB = Depends(get_current_user),
) -> UserResponse:
    """
    Get current authenticated user information.
    
    Requires valid access token in Authorization header.
    
    **Response:**
    - User profile information (without password)
    """
    return UserResponse(
        id=current_user.id,
        email=current_user.email,
        name=current_user.name,
        role=current_user.role,
        is_active=current_user.is_active,
        created_at=current_user.created_at,
        updated_at=current_user.updated_at,
    )


@router.post("/logout")
async def logout(
    current_user: UserInDB = Depends(get_current_user),
) -> dict:
    """
    Logout (invalidate tokens).
    
    Note: JWT tokens are stateless, so true logout requires:
    1. Client to delete tokens
    2. Optional: Add token to blacklist (Redis/database)
    3. Refresh token rotation on each use
    
    In v1.0, logout is client-side only.
    """
    # TODO: Implement token blacklist with Redis
    # For now, just return success message
    return {
        "message": "Successfully logged out",
        "detail": "Please delete tokens from client storage",
    }
