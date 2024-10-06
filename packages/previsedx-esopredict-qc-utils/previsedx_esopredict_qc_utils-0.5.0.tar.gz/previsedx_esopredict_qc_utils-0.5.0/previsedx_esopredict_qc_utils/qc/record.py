from pydantic import BaseModel
from typing import List, Optional


class Record(BaseModel):
    """A record of a QC check."""
    id: Optional[str] = None
    number: Optional[int] = None
    status: Optional[str] = None
    name: Optional[str] = None
    desc: Optional[str] = None
    pass_list: Optional[List[str]] = None
    fail_list: Optional[List[str]] = None
