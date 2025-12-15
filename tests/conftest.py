"""
Pytest configuration for API tests
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

@pytest.fixture
def client():
    """Provide test client for all tests"""
    from src.api.main import app
    return TestClient(app)

@pytest.fixture
def app():
    """Provide FastAPI app for tests"""
    from src.api.main import app
    return app
