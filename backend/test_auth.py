"""
Test JWT authentication system.
"""
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_password_hashing():
    """Test password hashing and verification."""
    from app.core.security import get_password_hash, verify_password
    
    print("Testing password hashing...")
    
    password = "TestPass123"  # Shorter password for bcrypt compatibility
    hashed = get_password_hash(password)
    
    assert hashed != password, "Hash should be different from password"
    assert hashed.startswith("$2"), "Bcrypt hash should start with $2"
    assert verify_password(password, hashed), "Password should verify"
    assert not verify_password("wrongpassword", hashed), "Wrong password should not verify"
    
    print("  Password hashing: PASSED")
    print(f"  Hash: {hashed[:30]}...")
    return True


def test_jwt_token_creation():
    """Test JWT token creation and decoding."""
    from app.core.security import create_access_token, create_refresh_token, decode_access_token, decode_refresh_token
    
    print("\nTesting JWT token creation...")
    
    # Test access token
    access_token = create_access_token(
        data={"sub": "test@example.com", "role": "agent"}
    )
    assert access_token, "Access token should be created"
    assert len(access_token) > 50, "Access token should be a valid JWT"
    
    # Decode access token
    payload = decode_access_token(access_token)
    assert payload is not None, "Access token should decode successfully"
    assert payload["sub"] == "test@example.com", "Subject should match"
    assert payload["role"] == "agent", "Role should match"
    assert payload["type"] == "access", "Token type should be access"
    
    # Test refresh token
    refresh_token = create_refresh_token(
        data={"sub": "test@example.com", "role": "agent"}
    )
    assert refresh_token, "Refresh token should be created"
    
    # Decode refresh token
    payload = decode_refresh_token(refresh_token)
    assert payload is not None, "Refresh token should decode successfully"
    assert payload["type"] == "refresh", "Token type should be refresh"
    
    print("  JWT token creation: PASSED")
    return True


def test_login_endpoint():
    """Test login endpoint."""
    print("\nTesting login endpoint...")
    
    response = client.post(
        "/api/v1/auth/login",
        data={
            "username": "test@example.com",
            "password": "TestPass123",
        }
    )
    
    print(f"  Status Code: {response.status_code}")
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    data = response.json()
    assert "access_token" in data, "Response should have access_token"
    assert "refresh_token" in data, "Response should have refresh_token"
    assert data["token_type"] == "bearer", "Token type should be bearer"
    assert "expires_in" in data, "Response should have expires_in"
    
    print("  Login endpoint: PASSED")
    print(f"  Access Token: {data['access_token'][:50]}...")
    print(f"  Expires In: {data['expires_in']} seconds")
    
    return data


def test_protected_endpoint(token: str):
    """Test protected endpoint with token."""
    print("\nTesting protected endpoint (/api/v1/auth/me)...")
    
    response = client.get(
        "/api/v1/auth/me",
        headers={"Authorization": f"Bearer {token}"}
    )
    
    print(f"  Status Code: {response.status_code}")
    
    # Should succeed with valid token
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    data = response.json()
    assert "email" in data, "Response should have email"
    assert "role" in data, "Response should have role"
    
    print("  Protected endpoint: PASSED")
    return True


def test_unauthorized_access():
    """Test unauthorized access to protected endpoint."""
    print("\nTesting unauthorized access...")
    
    response = client.get("/api/v1/auth/me")
    
    print(f"  Status Code: {response.status_code}")
    
    # Should fail without token
    assert response.status_code == 401, f"Expected 401, got {response.status_code}"
    
    print("  Unauthorized access test: PASSED")
    return True


def test_token_refresh(refresh_token: str):
    """Test token refresh endpoint."""
    print("\nTesting token refresh...")
    
    response = client.post(
        "/api/v1/auth/refresh",
        json={"refresh_token": refresh_token}
    )
    
    print(f"  Status Code: {response.status_code}")
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    data = response.json()
    assert "access_token" in data, "Response should have access_token"
    assert "refresh_token" in data, "Response should have refresh_token"
    
    print("  Token refresh: PASSED")
    return data


if __name__ == "__main__":
    print("=" * 50)
    print("JWT Authentication Tests")
    print("=" * 50)
    
    try:
        # Test core security functions
        test_password_hashing()
        test_jwt_token_creation()
        
        # Test endpoints
        tokens = test_login_endpoint()
        test_protected_endpoint(tokens["access_token"])
        test_unauthorized_access()
        test_token_refresh(tokens["refresh_token"])
        
        print("\n" + "=" * 50)
        print("All JWT Authentication Tests PASSED!")
        print("=" * 50)
        
    except Exception as e:
        print(f"\nTest FAILED: {e}")
        print("=" * 50)
        raise
