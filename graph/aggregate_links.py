from collections import defaultdict
from typing import Dict, List
from .link import Link
from .event_graph import EventGraph


def aggregate_links(
    graph: EventGraph,
    min_weight: float = 0.3
):
    aggregated = defaultdict(list)

    for src, links in graph.links.items():
        for link in links:
            if link.weight > 0:
                aggregated[(src, link.target_event_id)].append(link)

    graph.links.clear()

    for (src, tgt), links in aggregated.items():
        total_weight = min(1.0, sum(l.weight for l in links))

        if total_weight < min_weight:
            continue

        reasons = ",".join(sorted(set(l.reason for l in links)))

        graph.add_link(
            Link(
                source_event_id=src,
                target_event_id=tgt,
                reason=reasons,
                weight=total_weight,
            )
        )
