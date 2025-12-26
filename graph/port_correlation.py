from typing import List
from core.event import Event
from .event_graph import EventGraph
from .link import Link


def add_port_similarity_links(
    graph: EventGraph,
    events: List[Event],
    weight: float = 0.6
):
    events_by_port = {}

    for e in events:
        events_by_port.setdefault(e.destination_port, []).append(e)

    for port, port_events in events_by_port.items():
        port_events = sorted(port_events, key=lambda e: e.timestamp)

        for i, e1 in enumerate(port_events):
            for e2 in port_events[i + 1:]:
                link = Link(
                    source_event_id=e1.event_id,
                    target_event_id=e2.event_id,
                    reason=f"same_destination_port:{port}",
                    weight=weight,
                )
                graph.add_link(link)
