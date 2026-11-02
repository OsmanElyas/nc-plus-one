from pydantic import BaseModel
from datetime import datetime

class EventRequest(BaseModel):
    title: str
    description: str
    starts_at: datetime
    ends_at: datetime
    venue_id:int