import pytest
from src.api.client import ApiClient


@pytest.fixture()
def admin_client():
    """Authenticated admin API client."""
    client = ApiClient()
    client.login_admin()
    return client


@pytest.fixture()
def api_client():
    """Unauthenticated client (for public booking API)."""
    return ApiClient()
