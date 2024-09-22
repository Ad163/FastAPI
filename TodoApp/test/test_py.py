from ..routers.todo import get_current_user, get_db
from fastapi.testclient import TestClient
from sqlalchemy.pool import StaticPool
from sqlalchemy import create_engine, text
from sqlalchemy.orm import sessionmaker
from ..database import Base
from ..main import app
from ..models import Todo  # Import the Todo model
import pytest

SQLALCHEMY_DATABASE_URL = "sqlite:///./test.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL, 
    connect_args={"check_same_thread": False}, 
    poolclass=StaticPool
)

TestingSessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Ensure the table is created
Base.metadata.create_all(bind=engine)

def override_get_db():
    db = TestingSessionLocal()
    try:
        yield db
    finally:
        db.close()

app.dependency_overrides[get_db] = override_get_db

client = TestClient(app)

@pytest.fixture
def test_todo():
    db = TestingSessionLocal()
    # Clear the table before each test
    db.query(Todo).delete()
    db.commit()
    
    todo = Todo(
        title="Test Todo",
        description="Test Description",
        user_id=2,
        completed=False,
        priority=1
    )
    db.add(todo)
    db.commit()
    yield todo
    with engine.connect() as connection:
        connection.execute(text("DELETE FROM todo WHERE title='Test Todo'"))
        db.commit()

def test_readall_authenticated(test_todo):
    response = client.get("/api/todos/")
    assert response.status_code == 200
    expected_response = [{
        "title": "Test Todo",
        "description": "Test Description",
        "completed": False,
        "priority": 1,
        "user_id": 2,
        "id": test_todo.id  # Ensure the ID matches the created todo
    }]
    assert response.json() == expected_response

def test_readone_authenticated(test_todo):
    response = client.get(f"/api/todos/{test_todo.id}")
    assert response.status_code == 200
    expected_response = {
        "title": "Test Todo",
        "description": "Test Description",
        "completed": False,
        "priority": 1,
        "user_id": 2,
        "id": test_todo.id
    }
    assert response.json() == expected_response

def test_readone_notfound(test_todo):
    response = client.get("/api/todos/9999")  # Assuming 9999 is an ID that does not exist
    assert response.status_code == 404
    assert response.json() == {"detail": "Todo not found"}

def test_readone_unauthenticated(test_todo):
    # Assuming the endpoint requires authentication, which is not provided here
    response = client.get(f"/api/todos/{test_todo.id}")
    assert response.status_code == 401
    assert response.json() == {"detail": "Unauthorized"}