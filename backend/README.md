# CRM Authentication API

A secure backend authentication system for a CRM built with FastAPI, using bcrypt for password hashing and JWT for authentication.

## Features
- **User Registration**: `POST /auth/register` to create a new user.
- **User Login**: `POST /auth/login` to authenticate and receive a JWT.
- **Current User**: `GET /auth/me` to get details of the currently logged-in user.
- **Protected Routes**: Contains sample endpoints like `/contacts`, `/deals`, and `/tasks` that require a valid JWT.

## Requirements
- Python 3.8+

## Setup Instructions

1. **Navigate to the Backend Directory**
   ```bash
   cd backend
   ```

2. **Activate the Virtual Environment**
   On Windows:
   ```bash
   .\venv\Scripts\activate
   ```
   On macOS/Linux:
   ```bash
   source venv/bin/activate
   ```

3. **Install Dependencies** (if not already installed)
   ```bash
   pip install fastapi uvicorn passlib[bcrypt] python-jose[cryptography] sqlalchemy pydantic[email]
   ```

4. **Run the Application**
   ```bash
   uvicorn app.main:app --reload
   ```

5. **View API Documentation**
   Open your browser and navigate to:
   - Swagger UI: `http://127.0.0.1:8000/docs`
   - ReDoc: `http://127.0.0.1:8000/redoc`

## Security Practices Followed
- Passwords are never stored in plain text; they are hashed using **bcrypt**.
- **JWT (JSON Web Tokens)** are used for stateless authentication.
- Dependencies such as `Depends(get_current_user)` ensure that protected routes are only accessible to valid token holders.
- Included password hashing algorithms are secure and up-to-date.
