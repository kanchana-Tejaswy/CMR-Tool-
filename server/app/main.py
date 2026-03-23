from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from . import models
from .database import engine
from .routes import leads, tasks

# Create database tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
    title="CRM API",
    description="Backend API for a CRM system supporting Lead and Task management.",
    version="1.0.0",
)

# Configure CORS
origins = [
    "http://localhost",
    "http://localhost:3000",
    "http://localhost:5173",
    "http://localhost:8000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include routers
app.include_router(leads.router)
app.include_router(tasks.router)

@app.get("/health", tags=["health"])
def health_check():
    return {"status": "ok"}

