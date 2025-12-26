from dataclasses import dataclass


@dataclass(frozen=True)
class Link:
    source_event_id: int
    target_event_id: int
    reason: str
    weight: float
