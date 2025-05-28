# src/models/dlr.py
from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class DLR(BaseModel):
    campaign_id: str
    msisdn: str
    status_code: int
    response_text: str
    timestamp: datetime = datetime.now()
    status: Optional[str] = None  # delivered, failed, etc.
    error_code: Optional[str] = None

class DLRUpdate(BaseModel):
    campaign_id: str
    msisdn: str
    status: str
    error_code: Optional[str] = None