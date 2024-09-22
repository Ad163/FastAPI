from fastapi.testclient import TestClient
from ..main import app
from ..database import SessionLocal
import json
from sqlalchemy.orm import Session
import pytest


client = TestClient(app)


def test_health():
    response = client.get("/health")
    assert response.status_code == 200
    assert response.json() == {"status": "Healthy Service"}