"""
Test health endpoint using FastAPI TestClient.
"""
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)


def test_health_endpoint():
    """Test the health check endpoint."""
    print("Testing /api/v1/health endpoint...")
    
    response = client.get("/api/v1/health")
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    data = response.json()
    
    # Verify required fields
    assert "status" in data, "Missing 'status' field"
    assert "timestamp" in data, "Missing 'timestamp' field"
    assert "version" in data, "Missing 'version' field"
    assert "environment" in data, "Missing 'environment' field"
    assert "database" in data, "Missing 'database' field"
    
    # Verify values
    assert data["status"] in ["healthy", "unhealthy", "degraded"]
    assert data["version"] == "1.0.0"
    assert data["database"] in ["connected", "disconnected"]
    
    print("\nHealth endpoint test PASSED!")
    print(f"  - Status: {data['status']}")
    print(f"  - Database: {data['database']}")
    if data.get('database_latency_ms'):
        print(f"  - Database Latency: {data['database_latency_ms']}ms")
    
    return True


def test_database_health_endpoint():
    """Test the database health endpoint."""
    print("\nTesting /api/v1/health/db endpoint...")
    
    response = client.get("/api/v1/health/db")
    
    print(f"Status Code: {response.status_code}")
    print(f"Response: {response.json()}")
    
    assert response.status_code == 200, f"Expected 200, got {response.status_code}"
    
    data = response.json()
    
    # Verify required fields
    assert "connected" in data, "Missing 'connected' field"
    
    print("\nDatabase health endpoint test PASSED!")
    print(f"  - Connected: {data['connected']}")
    if data.get('latency_ms'):
        print(f"  - Latency: {data['latency_ms']}ms")
    
    return True


if __name__ == "__main__":
    print("=" * 50)
    print("Health Endpoint Tests")
    print("=" * 50)
    
    try:
        test_health_endpoint()
        test_database_health_endpoint()
        
        print("\n" + "=" * 50)
        print("All tests PASSED!")
        print("=" * 50)
    except Exception as e:
        print(f"\nTest FAILED: {e}")
        print("=" * 50)
