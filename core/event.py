from dataclasses import dataclass
from datetime import datetime
from typing import Dict, Any


@dataclass(frozen=True)
class Event:
    event_id: int
    timestamp: datetime
    destination_port: int
    label: str
    features: Dict[str, Any]
