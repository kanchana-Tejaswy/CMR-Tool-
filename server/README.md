# CRM Backend API

This is the FastAPI backend for the CRM system supporting Contact and Task management.

## Setup Instructions

1.  Navigate to the server directory:
    ```bash
    cd c:\Users\v\OneDrive\Documents\CRM Tool\server
    ```

2.  Create a virtual environment:
    ```bash
    python -m venv venv
    ```

3.  Activate the virtual environment:
    *   **Windows:**
        ```bash
        venv\Scripts\activate
        ```
    *   **Mac/Linux:**
        ```bash
        source venv/bin/activate
        ```

4.  Install dependencies:
    ```bash
    pip install -r requirements.txt
    ```

5.  Run the application:
    ```bash
    uvicorn app.main:app --reload
    ```

The API will be available at `http://localhost:8000`.
You can access the interactive API documentation (Swagger UI) at `http://localhost:8000/docs`.

## Example API Requests

### Health Check

```bash
curl -X 'GET' 'http://localhost:8000/health'
```

**Response:**
```json
{
  "status": "ok"
}
```

### Create a Contact

```bash
curl -X 'POST' \
  'http://localhost:8000/contacts/' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "phone": "+1-555-0123",
  "company": "Tech Corp"
}'
```

**Response:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "phone": "+1-555-0123",
  "company": "Tech Corp",
  "id": 1,
  "tasks": []
}
```

### Get all Contacts

```bash
curl -X 'GET' 'http://localhost:8000/contacts/' -H 'accept: application/json'
```

### Create a Task (requires a valid Contact ID)

```bash
curl -X 'POST' \
  'http://localhost:8000/tasks/?contact_id=1' \
  -H 'accept: application/json' \
  -H 'Content-Type: application/json' \
  -d '{
  "title": "Follow up call",
  "description": "Call John to discuss the new contract proposal.",
  "is_completed": false
}'
```

**Response:**
```json
{
  "title": "Follow up call",
  "description": "Call John to discuss the new contract proposal.",
  "is_completed": false,
  "id": 1,
  "created_at": "2023-10-27T10:00:00",
  "contact_id": 1
}
```

### Get a Contact (with tasks)

```bash
curl -X 'GET' 'http://localhost:8000/contacts/1' -H 'accept: application/json'
```

**Response:**
```json
{
  "first_name": "John",
  "last_name": "Doe",
  "email": "john.doe@example.com",
  "phone": "+1-555-0123",
  "company": "Tech Corp",
  "id": 1,
  "tasks": [
    {
      "title": "Follow up call",
      "description": "Call John to discuss the new contract proposal.",
      "is_completed": false,
      "id": 1,
      "created_at": "2023-10-27T10:00:00",
      "contact_id": 1
    }
  ]
}
```
