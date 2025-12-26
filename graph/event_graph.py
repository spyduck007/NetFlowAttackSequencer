from collections import defaultdict
from typing import List, Dict
from core.event import Event
from .link import Link


class EventGraph:
    def __init__(self, events: List[Event]):
        self.events = {e.event_id: e for e in events}
        self.links: Dict[int, List[Link]] = defaultdict(list)

    def add_link(self, link: Link):
        self.links[link.source_event_id].append(link)

    def get_outgoing_links(self, event_id: int) -> List[Link]:
        return self.links.get(event_id, [])

    def __len__(self):
        return len(self.events)
