from typing import List
from core.event import Event
from .event_graph import EventGraph
from .link import Link


FEATURE_KEYS = [
    "flow_duration",
    "total_fwd_packets",
    "total_bwd_packets",
    "packet_length_mean",
]


def _distance(e1: Event, e2: Event) -> float:
    total = 0.0
    count = 0

    for k in FEATURE_KEYS:
        v1 = e1.features[k]
        v2 = e2.features[k]

        if v1 == 0 and v2 == 0:
            continue

        denom = max(v1, v2)
        total += abs(v1 - v2) / denom
        count += 1

    if count == 0:
        return 1.0

    return total / count


def add_feature_similarity_links(
    graph: EventGraph,
    events: List[Event],
    max_distance: float = 0.3
):
    for i, e1 in enumerate(events):
        for e2 in events[i + 1:]:
            dist = _distance(e1, e2)

            if dist <= max_distance:
                weight = 1.0 - dist

                link = Link(
                    source_event_id=e1.event_id,
                    target_event_id=e2.event_id,
                    reason="feature_similarity",
                    weight=weight,
                )
                graph.add_link(link)
