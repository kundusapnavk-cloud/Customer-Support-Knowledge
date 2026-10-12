from dataclasses import dataclass
from typing import Optional

#This defines what one support document should look like inside Python. Instead of passing random text around, every document has the same structure.
@dataclass
class SupportDocument:
    content: str
    title: str
    category: str
    source_path: str

    product: Optional[str] = None
    plan: Optional[str] = None
    last_updated: Optional[str] = None
    source_type: Optional[str] = None