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
        assert "service" in data
        assert "version" in data
    
    def test_health_endpoint_performance(self):
        """Test health endpoint response time"""
        response = client.get("/api/v1/health")
        assert response.elapsed.total_seconds() < 0.1


class TestAPIStartup:
    """Test API startup and configuration"""
    
    def test_app_exists(self):
        """Test that FastAPI app is created"""
        assert app is not None
    
    def test_app_has_openapi(self):
        """Test that OpenAPI schema exists"""
        response = client.get("/openapi.json")
        assert response.status_code == 200
        
        schema = response.json()
        assert "info" in schema
        assert "paths" in schema
    
    def test_swagger_ui_available(self):
        """Test that Swagger UI is available"""
        response = client.get("/docs")
        assert response.status_code == 200
        assert "swagger" in response.text.lower()
    
    def test_redoc_available(self):
        """Test that ReDoc is available"""
        response = client.get("/redoc")
        assert response.status_code == 200


class TestAPIMiddleware:
    """Test API middleware"""
    
    def test_request_handled(self):
        """Test that requests are handled properly"""
        response = client.get("/api/v1/health")
        assert response.status_code == 200


class TestErrorHandling:
    """Test error handling"""
    
    def test_404_endpoint_not_found(self):
        """Test 404 error on non-existent endpoint"""
        response = client.get("/api/v1/nonexistent")
        assert response.status_code == 404
    
    def test_404_response_format(self):
        """Test 404 response has proper structure"""
        response = client.get("/api/v1/nonexistent")
        data = response.json()
        
        assert "detail" in data or "message" in data


class TestAPIDocumentation:
    """Test API documentation"""
    
    def test_openapi_info(self):
        """Test OpenAPI info contains correct data"""
        response = client.get("/openapi.json")
        schema = response.json()
        
        assert schema["info"]["title"]
        assert schema["info"]["version"]
        assert schema["info"]["description"]
    
    def test_health_endpoint_documented(self):
        """Test health endpoint is documented in OpenAPI"""
        response = client.get("/openapi.json")
        schema = response.json()
        
        assert "/api/v1/health" in schema["paths"]


if __name__ == "__main__":
    pytest.main([__file__, "-v"])
