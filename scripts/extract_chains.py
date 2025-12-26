from core.loader import load_cic_ids2017
from graph.build_graph import build_event_graph
from graph.port_correlation import add_port_similarity_links
from graph.feature_similarity import add_feature_similarity_links
from graph.aggregate_links import aggregate_links
from chains.extract import extract_chains
from chains.prune import prune_dominated_chains
from chains.canonicalize import canonicalize_chains



def main():
    events = load_cic_ids2017(
        "data/raw/cic_ids2017.csv",
        limit=50
    )

    graph = build_event_graph(events, time_window_seconds=3)
    add_port_similarity_links(graph, events)
    add_feature_similarity_links(graph, events)

    aggregate_links(graph)

    chains = extract_chains(graph)
    chains = prune_dominated_chains(chains)
    chains = canonicalize_chains(chains)

    print(f"\nExtracted {len(chains)} attack chains:\n")

    for c in chains[:5]:
        print("Chain:", c)


if __name__ == "__main__":
    main()
