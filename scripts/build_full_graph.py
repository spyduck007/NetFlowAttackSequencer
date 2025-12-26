from core.loader import load_cic_ids2017
from graph.build_graph import build_event_graph
from graph.port_correlation import add_port_similarity_links
from graph.feature_similarity import add_feature_similarity_links


def main():
    events = load_cic_ids2017(
        "data/raw/cic_ids2017.csv",
        limit=50
    )

    graph = build_event_graph(events, time_window_seconds=3)

    add_port_similarity_links(graph, events)
    add_feature_similarity_links(graph, events)

    for event_id in range(5):
        links = graph.get_outgoing_links(event_id)
        print(f"\nEvent {event_id} -> {len(links)} links")
        for l in links:
            print(" ", l)


if __name__ == "__main__":
    main()
