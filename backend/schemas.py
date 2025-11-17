from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

# Each model corresponds to a MongoDB collection (lowercased class name)

class Lead(BaseModel):
    name: str = Field(..., min_length=1, max_length=120)
    email: Optional[EmailStr] = None
    phone: Optional[str] = Field(None, max_length=30)
    company: Optional[str] = Field(None, max_length=120)
    message: Optional[str] = Field(None, max_length=2000)
    interested_channels: List[str] = Field(default_factory=list, description="e.g., calls, email, whatsapp")

class DemoRequest(BaseModel):
    company: str
    contact_name: str
    contact_email: EmailStr
    use_case: str

class AgentTemplate(BaseModel):
    title: str
    description: str
    price_per_month: float = Field(..., ge=0)
    capabilities: List[str] = Field(default_factory=list)

class ContactMessage(BaseModel):
    name: str
    email: Optional[EmailStr] = None
    channel: str = Field(..., description="email|whatsapp|phone")
    content: str

class Inserted(BaseModel):
    id: str
    created_at: datetime
    updated_at: datetime
