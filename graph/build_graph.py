from datetime import timedelta
from typing import List
from core.event import Event
from .event_graph import EventGraph
from .link import Link


def build_event_graph(
    events: List[Event],
    time_window_seconds: int = 5
) -> EventGraph:
    graph = EventGraph(events)

    sorted_events = sorted(events, key=lambda e: e.timestamp)

    for i, e1 in enumerate(sorted_events):
        for e2 in sorted_events[i + 1:]:
            delta = (e2.timestamp - e1.timestamp).total_seconds()

            if delta > time_window_seconds:
                break

            weight = max(0.0, 1.0 - (delta / time_window_seconds))

            link = Link(
                source_event_id=e1.event_id,
                target_event_id=e2.event_id,
                reason="temporal_proximity",
                weight=weight,
            )

            graph.add_link(link)

    return graph
