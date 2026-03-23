from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

app = FastAPI(
    title="CRM API",
    description="A simple CRM backend API without authentication.",
    version="1.0.0"
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"], # Next.js frontend
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def read_root():
    return {"message": "Welcome to the CRM API"}

@app.get("/contacts", tags=["CRM"])
def get_contacts():
    return {
        "contacts": [
            {"id": 1, "name": "Jane Doe", "company": "Acme Corp"},
            {"id": 2, "name": "John Smith", "company": "Global Tech"}
        ]
    }

@app.get("/deals", tags=["CRM"])
def get_deals():
    return {
        "deals": [
            {"id": 1, "title": "Software License", "amount": 10000},
            {"id": 2, "title": "Consulting Services", "amount": 5000}
        ]
    }

@app.get("/tasks", tags=["CRM"])
def get_tasks():
    return {
        "tasks": [
            {"id": 1, "title": "Follow up with Jane"},
            {"id": 2, "title": "Send proposal to Global Tech"}
        ]
    }
