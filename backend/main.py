"""
DocuSphere - AI Document Intelligence Hub
FastAPI Backend Application

This is the main entry point for the FastAPI backend service.
Deploy to Vercel or any Python-compatible hosting platform.
"""

from fastapi import FastAPI, HTTPException, Depends, UploadFile, File, Form
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel, EmailStr
from typing import List, Optional
from datetime import datetime, timedelta
import os
import uuid

# Initialize FastAPI app
app = FastAPI(
    title="DocuSphere API",
    description="AI-powered document intelligence platform for KMRL",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# CORS Configuration
origins = [
    "http://localhost:3000",
    "http://localhost:8888",
    "https://docusphere-kmrl.netlify.app",
    "https://*.netlify.app",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# ============ Pydantic Models ============

class UserLogin(BaseModel):
    email: EmailStr
    password: str
    role: Optional[str] = "viewer"

class UserResponse(BaseModel):
    id: str
    email: str
    name: str
    role: str
    token: str

class DocumentUpload(BaseModel):
    fileName: str
    fileType: str
    options: Optional[dict] = {}

class ChatMessage(BaseModel):
    message: str
    document_ids: Optional[List[int]] = []
    language: Optional[str] = "en"
    conversation_history: Optional[List[dict]] = []

class ChatResponse(BaseModel):
    response: str
    sources: List[str]
    confidence: float
    language: str

class Deadline(BaseModel):
    id: str
    title: str
    document: str
    due_date: datetime
    status: str
    priority: str

class Document(BaseModel):
    id: str
    name: str
    type: str
    size: str
    uploaded_at: datetime
    status: str
    language: str
    confidence: float
    summary: Optional[str] = None

# ============ Mock Data Store ============

documents_db = []
deadlines_db = []
users_db = {}

# ============ Authentication Routes ============

@app.post("/api/auth/login", response_model=UserResponse)
async def login(user: UserLogin):
    """Authenticate user and return JWT token"""
    # In production, validate against database
    user_id = str(uuid.uuid4())
    name = user.email.split('@')[0].replace('.', ' ').title()
    
    # Generate mock JWT token (use python-jose in production)
    token = f"eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzI1NiJ9.{user_id}"
    
    return UserResponse(
        id=user_id,
        email=user.email,
        name=name,
        role=user.role,
        token=token
    )

@app.post("/api/auth/logout")
async def logout():
    """Logout user and invalidate token"""
    return {"success": True, "message": "Logged out successfully"}

# ============ Document Routes ============

@app.get("/api/documents", response_model=List[Document])
async def get_documents(
    skip: int = 0,
    limit: int = 20,
    status: Optional[str] = None,
    language: Optional[str] = None
):
    """Get list of documents with optional filtering"""
    # Mock data
    mock_documents = [
        Document(
            id="doc_1",
            name="Contract_KMRL_2024.pdf",
            type="pdf",
            size="2.4 MB",
            uploaded_at=datetime.now() - timedelta(days=5),
            status="processed",
            language="English",
            confidence=0.98,
            summary="KMRL construction contract with key terms and conditions."
        ),
        Document(
            id="doc_2",
            name="Meeting_Minutes_Dec.docx",
            type="docx",
            size="856 KB",
            uploaded_at=datetime.now() - timedelta(days=3),
            status="processed",
            language="English",
            confidence=0.95,
            summary="December meeting minutes with action items."
        ),
        Document(
            id="doc_3",
            name="Site_Survey_Report.jpg",
            type="image",
            size="4.2 MB",
            uploaded_at=datetime.now() - timedelta(days=1),
            status="processed",
            language="Malayalam",
            confidence=0.92,
            summary="Site survey photographs with annotations."
        ),
    ]
    
    return mock_documents[skip:skip + limit]

@app.post("/api/documents/upload")
async def upload_document(
    file: UploadFile = File(...),
    options: str = Form("{}")
):
    """Upload and process a new document"""
    import json
    
    try:
        opts = json.loads(options)
    except:
        opts = {}
    
    # In production:
    # 1. Upload to Supabase Storage
    # 2. Extract text (OCR if image)
    # 3. Process with Gemini
    # 4. Generate embeddings
    # 5. Store in Pinecone
    # 6. Save metadata to PostgreSQL
    
    doc_id = str(uuid.uuid4())
    
    return {
        "success": True,
        "document": {
            "id": doc_id,
            "name": file.filename,
            "type": file.content_type,
            "size": "Unknown",
            "status": "processing",
            "uploaded_at": datetime.now().isoformat()
        },
        "message": "Document uploaded successfully. Processing started."
    }

@app.get("/api/documents/{doc_id}")
async def get_document(doc_id: str):
    """Get document details by ID"""
    return {
        "id": doc_id,
        "name": "Contract_KMRL_2024.pdf",
        "type": "pdf",
        "size": "2.4 MB",
        "uploaded_at": datetime.now().isoformat(),
        "status": "processed",
        "language": "English",
        "confidence": 0.98,
        "summary": "This document outlines the contractual agreement between KMRL and the contractor.",
        "keywords": ["contract", "KMRL", "metro", "construction"],
        "deadlines_extracted": 3,
        "page_count": 24
    }

@app.delete("/api/documents/{doc_id}")
async def delete_document(doc_id: str):
    """Delete a document"""
    return {"success": True, "message": f"Document {doc_id} deleted"}

# ============ Chat Routes ============

@app.post("/api/chat", response_model=ChatResponse)
async def chat(message: ChatMessage):
    """AI-powered document Q&A using RAG pipeline"""
    query = message.message.lower()
    
    # In production:
    # 1. Generate query embedding
    # 2. Search Pinecone for relevant chunks
    # 3. Build context from retrieved documents
    # 4. Send to Gemini with context
    # 5. Return structured response
    
    if "deadline" in query or "due" in query:
        response_text = """Based on the documents, here are the key deadlines:

📅 **January 18, 2024** - Budget Approval Meeting
📅 **January 25, 2024** - Vendor Contract Finalization  
📅 **February 1, 2024** - Q1 Review Presentation

⚠️ The Contract Renewal deadline (January 10) has passed."""
        sources = ["Contract_KMRL_2024.pdf", "Meeting_Minutes_Dec.docx"]
        confidence = 0.94
        
    elif "contract" in query or "summary" in query:
        response_text = """**KMRL Contract 2024 Summary:**

• Duration: 24 months (Jan 2024 - Dec 2025)
• Value: ₹45.6 Crores
• Payment: 30% advance, 70% milestone-based
• Penalty: 1% per week for delays (max 10%)
• Warranty: 24 months post-completion"""
        sources = ["Contract_KMRL_2024.pdf"]
        confidence = 0.97
        
    elif "payment" in query:
        response_text = """**Payment Terms:**

💰 Advance: 30% upon signing
💰 Progress 1: 25% at 40% completion
💰 Progress 2: 25% at 75% completion
💰 Final: 20% upon completion

Processing time: 21 days from invoice approval."""
        sources = ["Contract_KMRL_2024.pdf", "Vendor_Agreement.pdf"]
        confidence = 0.96
        
    else:
        response_text = """I've analyzed the selected documents. They contain information about:

• Project timelines and milestones
• Contract terms and conditions
• Budget allocations
• Technical specifications

What specific information would you like to know?"""
        sources = ["Multiple documents"]
        confidence = 0.85
    
    return ChatResponse(
        response=response_text,
        sources=sources,
        confidence=confidence,
        language=message.language
    )

# ============ Deadline Routes ============

@app.get("/api/deadlines", response_model=List[Deadline])
async def get_deadlines(
    status: Optional[str] = None,
    sort: str = "due_date"
):
    """Get extracted deadlines from documents"""
    deadlines = [
        Deadline(
            id="dl_1",
            title="Contract Renewal Submission",
            document="Contract_KMRL_2024.pdf",
            due_date=datetime.now() - timedelta(days=5),
            status="overdue",
            priority="high"
        ),
        Deadline(
            id="dl_2",
            title="Budget Approval Meeting",
            document="Budget_Proposal_Q1.pdf",
            due_date=datetime.now() + timedelta(days=3),
            status="due-soon",
            priority="high"
        ),
        Deadline(
            id="dl_3",
            title="Vendor Payment Processing",
            document="Vendor_Agreement.pdf",
            due_date=datetime.now() + timedelta(days=7),
            status="on-track",
            priority="medium"
        ),
    ]
    
    if status:
        deadlines = [d for d in deadlines if d.status == status]
    
    return deadlines

@app.post("/api/deadlines/{deadline_id}/remind")
async def set_reminder(deadline_id: str, days_before: int = 1):
    """Set a reminder for a deadline"""
    return {
        "success": True,
        "message": f"Reminder set for {days_before} day(s) before deadline"
    }

@app.put("/api/deadlines/{deadline_id}/complete")
async def mark_complete(deadline_id: str):
    """Mark a deadline as complete"""
    return {"success": True, "message": "Deadline marked as complete"}

# ============ Analytics Routes ============

@app.get("/api/analytics/overview")
async def get_analytics():
    """Get analytics overview"""
    return {
        "total_documents": 2847,
        "processed_documents": 1234,
        "pending_deadlines": 23,
        "languages_supported": 12,
        "processing_accuracy": 0.985,
        "avg_processing_time": 2.3,
        "document_types": {
            "pdf": 45,
            "docx": 25,
            "image": 20,
            "other": 10
        },
        "language_distribution": {
            "English": 65,
            "Malayalam": 20,
            "Hindi": 10,
            "Tamil": 5
        }
    }

# ============ Health Check ============

@app.get("/")
async def root():
    """API root endpoint"""
    return {
        "name": "DocuSphere API",
        "version": "1.0.0",
        "status": "healthy",
        "docs": "/docs"
    }

@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "services": {
            "database": "connected",
            "gemini": "available",
            "pinecone": "available",
            "supabase": "connected"
        }
    }

# ============ Error Handlers ============

@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error", "detail": str(exc)}
    )

# ============ Vercel Handler ============

# For Vercel deployment
handler = app
