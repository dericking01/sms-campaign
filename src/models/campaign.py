# src/models/campaign.py
from pydantic import BaseModel, UUID4
from typing import Optional

class Campaign(BaseModel):
    id: str  # Or UUID4 if you prefer
    message: str
    sender_id: str
    dlr_callback_url: str
    status: str = "pending"  # pending, running, completed, failed
    total_recipients: Optional[int] = None
    started_at: Optional[str] = None
    completed_at: Optional[str] = None