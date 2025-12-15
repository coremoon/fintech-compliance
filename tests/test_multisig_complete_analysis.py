"""
Tests for FastAPI Application
"""

import pytest
from fastapi.testclient import TestClient
import sys
import os

sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from src.api.main import app

client = TestClient(app)


class TestHealthEndpoint:
    """Test health check endpoint"""
    
    def test_health_endpoint_exists(self):
        """Test that health endpoint exists"""
        response = client.get("/api/v1/health")
        assert response.status_code == 200
    
    def test_health_endpoint_returns_json(self):
        """Test that health endpoint returns JSON"""
        response = client.get("/api/v1/health")
        assert response.headers["content-type"] == "application/json"
    
    def test_health_endpoint_structure(self):
        """Test health endpoint response structure"""
        response = client.get("/api/v1/health")
        data = response.json()
        
        assert "status" in data
        assert data["status"] == "healthy"
        assert "services" in data
        assert "version" in data
    
    def test_health_endpoint_performance(self):
        """Test health endpoint response time"""
        response = client.get("/api/v1/health")
        assert response.elapsed.total_seconds() < 0.1