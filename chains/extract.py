from typing import List
from graph.event_graph import EventGraph


def extract_chains(
    graph: EventGraph,
    min_length: int = 3,
    max_length: int = 6,
    min_confidence: float = 0.8,
) -> List[List[int]]:
    chains = []

    def dfs(current, path, confidence):
        if len(path) > max_length:
            return

        extended = False

        for link in graph.get_outgoing_links(current):
            if link.target_event_id in path:
                continue

            new_confidence = confidence * link.weight

            if new_confidence < min_confidence:
                continue

            extended = True
            dfs(
                link.target_event_id,
                path + [link.target_event_id],
                new_confidence,
            )

        if not extended and len(path) >= min_length:
            chains.append(path[:])

    for event_id in graph.events:
        dfs(event_id, [event_id], confidence=1.0)

    return chains
