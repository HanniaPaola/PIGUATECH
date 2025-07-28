from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class ReportCreate(BaseModel):
    pond_id: Optional[int] = None
    start_date: Optional[datetime] = None  
    end_date: Optional[datetime] = None     
    created_by: Optional[int] = None

class Report(BaseModel):
    report_id: int
    pond_id: Optional[int]
    start_date: Optional[datetime] = None   
    end_date: Optional[datetime] = None    
    created_at: datetime
    created_by: Optional[int]
    file_path: Optional[str] = None

    model_config = {
        "from_attributes": True
    }
