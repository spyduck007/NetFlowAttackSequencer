from core.loader import load_cic_ids2017
from graph.build_graph import build_event_graph


def main():
    events = load_cic_ids2017(
        "data/raw/cic_ids2017.csv",
        limit=20
    )

    graph = build_event_graph(events, time_window_seconds=3)

    print(f"Graph has {len(graph)} events\n")

    for event_id in range(5):
        links = graph.get_outgoing_links(event_id)
        print(f"Event {event_id} -> {len(links)} links")
        for l in links:
            print("  ", l)


if __name__ == "__main__":
    main()
