

# FastAPI Todo Application

This is a backend Todo application built with FastAPI. The application allows users to create, read, update, and delete todo items, and includes user authentication and authorization features.

## Table of Contents

- [Features](#features)
- [Installation](#installation)
- [Usage](#usage)
- [API Endpoints](#api-endpoints)
- [Running Tests](#running-tests)
- [Environment Variables](#environment-variables)

## Features

- User registration, authentication, and authorization using JWT tokens
- CRUD (Create, Read, Update, Delete) operations for todo items
- SQLite database integration for data persistence
- FastAPI dependency injection
- Swagger UI for API documentation

## Installation

### Prerequisites

- Python 3.7+
- Git

### Clone the Repository

```bash
git clone https://github.com/YourUsername/TodoApp-FastAPI.git
cd TodoApp-FastAPI
```

### Create a Virtual Environment

```bash
python -m venv .venv
source .venv/bin/activate  # On Windows use `.venv\Scripts\activate`
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Set Up Environment Variables

Create a `.env` file in the root directory and add the following environment variables:

```plaintext
SECRET_KEY=your_secret_key_here
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=30
```

Replace `your_secret_key_here` with a secure key of your choice.

### Database Setup

The project uses SQLite by default. To set up the database, run:

```bash
alembic upgrade head
```

This will apply the necessary database migrations.

## Usage

### Run the Application

To start the FastAPI server, run:

```bash
uvicorn main:app --reload
```

The application will be accessible at `http://127.0.0.1:8000`.

### API Documentation

FastAPI provides interactive API documentation at the following URLs:

- Swagger UI: `http://127.0.0.1:8000/docs`
- ReDoc: `http://127.0.0.1:8000/redoc`

## API Endpoints

### Authentication

- **POST** `/token`: Obtain a JWT token by providing valid user credentials.

### Users

- **POST** `/users/`: Register a new user.
- **GET** `/users/me/`: Get the details of the currently authenticated user.

### Todo Items

- **GET** `/todos/`: Get all todo items.
- **GET** `/todos/{todo_id}`: Get a specific todo item by ID.
- **POST** `/todos/`: Create a new todo item.
- **PUT** `/todos/{todo_id}`: Update an existing todo item by ID.
- **DELETE** `/todos/{todo_id}`: Delete a specific todo item by ID.

## Running Tests

### Install Test Dependencies

```bash
pip install pytest pytest-asyncio
```

### Run Tests

```bash
pytest
```

This will run all the test cases in the project.

## Environment Variables

The application uses the following environment variables:

- `SECRET_KEY`: The secret key used for generating JWT tokens.
- `ALGORITHM`: The algorithm used for encoding JWT tokens (default: HS256).
- `ACCESS_TOKEN_EXPIRE_MINUTES`: Token expiry time (default: 30 minutes).

