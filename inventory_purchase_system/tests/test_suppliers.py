# ============================================================
# test_suppliers.py - Supplier API Tests
# ============================================================
# Uses httpx AsyncClient to test the FastAPI app.
# Run with: pytest tests/ -v
#
# NOTE: These tests require a running MongoDB instance.
# For CI/CD, use a MongoDB test container or mock.
# ============================================================

import pytest
from httpx import AsyncClient, ASGITransport
from app.main import app

# ---- Sample test data ----
SUPPLIER_PAYLOAD = {
    "supplier_name": "Test Supplier Co",
    "contact_number": "+91-9999999999",
    "city": "Chennai",
    "categories_supplied": ["Electronics", "Cables"],
    "active": True,
}

AUTH_PAYLOAD = {
    "username": "testuser",
    "email": "test@example.com",
    "password": "TestPass123",
}


@pytest.fixture
async def auth_token(async_client: AsyncClient) -> str:
    """Register and login a test user, return JWT token."""
    await async_client.post("/auth/register", json=AUTH_PAYLOAD)
    response = await async_client.post(
        "/auth/login",
        json={"username": AUTH_PAYLOAD["username"], "password": AUTH_PAYLOAD["password"]},
    )
    data = response.json()
    return data["data"]["access_token"]


@pytest.fixture
async def async_client():
    """Provide an async HTTP test client."""
    async with AsyncClient(
        transport=ASGITransport(app=app),
        base_url="http://test",
    ) as client:
        yield client


# ============================================================
# Test Cases
# ============================================================

@pytest.mark.asyncio
async def test_health_check(async_client: AsyncClient):
    """GET / should return 200 with success=True."""
    response = await async_client.get("/")
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True


@pytest.mark.asyncio
async def test_register_user(async_client: AsyncClient):
    """POST /auth/register should create user and return 201."""
    response = await async_client.post("/auth/register", json=AUTH_PAYLOAD)
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["data"]["username"] == AUTH_PAYLOAD["username"].lower()


@pytest.mark.asyncio
async def test_login_user(async_client: AsyncClient):
    """POST /auth/login should return JWT token."""
    await async_client.post("/auth/register", json=AUTH_PAYLOAD)
    response = await async_client.post(
        "/auth/login",
        json={"username": AUTH_PAYLOAD["username"], "password": AUTH_PAYLOAD["password"]},
    )
    assert response.status_code == 200
    data = response.json()
    assert data["success"] is True
    assert "access_token" in data["data"]


@pytest.mark.asyncio
async def test_create_supplier_requires_auth(async_client: AsyncClient):
    """POST /suppliers without token should return 401."""
    response = await async_client.post("/suppliers/", json=SUPPLIER_PAYLOAD)
    assert response.status_code == 401


@pytest.mark.asyncio
async def test_create_supplier_with_auth(async_client: AsyncClient, auth_token: str):
    """POST /suppliers with valid token should create supplier."""
    response = await async_client.post(
        "/suppliers/",
        json=SUPPLIER_PAYLOAD,
        headers={"Authorization": f"Bearer {auth_token}"},
    )
    assert response.status_code == 201
    data = response.json()
    assert data["success"] is True
    assert data["data"]["supplier_name"] == SUPPLIER_PAYLOAD["supplier_name"]
    assert "id" in data["data"]
