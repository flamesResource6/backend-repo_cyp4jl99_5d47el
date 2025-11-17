from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional, Dict, Any
import os

from database import db, create_document, get_documents
from schemas import Lead, DemoRequest, AgentTemplate, ContactMessage

app = FastAPI(title="AI Agent Sales API", version="1.0.0")

# CORS setup for frontend
frontend_url = os.getenv("FRONTEND_URL", "*")
app.add_middleware(
    CORSMiddleware,
    allow_origins=[frontend_url, "*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.get("/")
async def root():
    return {"message": "AI Agent Sales API running"}


@app.get("/test")
async def test():
    # Verify DB connection and list collections
    try:
        _ = db()
        # Try to list collections to verify connection
        collections = _ .list_collection_names()
        from os import getenv
        return {
            "backend": "ok",
            "database": "mongodb",
            "database_url": getenv("DATABASE_URL", "unknown"),
            "database_name": getenv("DATABASE_NAME", "appdb"),
            "connection_status": "connected",
            "collections": collections,
        }
    except Exception as e:
        return {
            "backend": "ok",
            "database": "mongodb",
            "connection_status": f"error: {str(e)}",
        }


# Public catalog of agent templates
@app.get("/templates", response_model=List[Dict[str, Any]])
async def list_templates():
    items = get_documents("agenttemplate", {})
    return items


@app.post("/templates", response_model=Dict[str, Any])
async def create_template(template: AgentTemplate):
    try:
        inserted = create_document("agenttemplate", template.model_dump())
        return inserted
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Leads from landing page forms
@app.post("/leads", response_model=Dict[str, Any])
async def create_lead(lead: Lead):
    try:
        inserted = create_document("lead", lead.model_dump())
        return inserted
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# Demo request form submissions
@app.post("/demo-requests", response_model=Dict[str, Any])
async def create_demo_request(req: DemoRequest):
    try:
        inserted = create_document("demorequest", req.model_dump())
        return inserted
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


# General contact messages
@app.post("/messages", response_model=Dict[str, Any])
async def create_message(msg: ContactMessage):
    try:
        inserted = create_document("contactmessage", msg.model_dump())
        return inserted
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
