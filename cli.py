#!/usr/bin/env python3
import argparse
import sys
import os

sys.path.append(os.getcwd())

from core.loader import load_cic_ids2017
from graph.build_graph import build_event_graph
from graph.port_correlation import add_port_similarity_links
from graph.feature_similarity import add_feature_similarity_links
from graph.aggregate_links import aggregate_links
from chains.extract import extract_chains
from chains.prune import prune_dominated_chains
from chains.canonicalize import canonicalize_chains


def main():
    parser = argparse.ArgumentParser(
        description="NetFlowAttackSequencer: A tool to extract attack chains from network flow data"
    )

    parser.add_argument(
        "-i",
        "--input",
        default="data/raw/cic_ids2017.csv",
        help="Path to the input CSV file (default: data/raw/cic_ids2017.csv)",
    )

    parser.add_argument(
        "-l",
        "--limit",
        type=int,
        default=50,
        help="Number of events to load (default: 50)",
    )

    parser.add_argument(
        "-w",
        "--window",
        type=int,
        default=3,
        help="Time window in seconds for temporal proximity (default: 3)",
    )

    parser.add_argument(
        "-o", "--output", help="Path to save the extracted chains (optional)"
    )

    parser.add_argument(
        "-v", "--verbose", action="store_true", help="Enable verbose output"
    )

    args = parser.parse_args()

    if args.verbose:
        print(f"Loading events from {args.input} with limit {args.limit}...")

    try:
        events = load_cic_ids2017(args.input, limit=args.limit)
    except FileNotFoundError:
        print(f"Error: File not found at {args.input}")
        sys.exit(1)
    except Exception as e:
        print(f"Error loading events: {e}")
        sys.exit(1)

    if args.verbose:
        print(f"Loaded {len(events)} events.")
        print(f"Building event graph with time window {args.window}s...")

    graph = build_event_graph(events, time_window_seconds=args.window)

    if args.verbose:
        print("Adding port similarity links...")
    add_port_similarity_links(graph, events)

    if args.verbose:
        print("Adding feature similarity links...")
    add_feature_similarity_links(graph, events)

    if args.verbose:
        print("Aggregating links...")
    aggregate_links(graph)

    if args.verbose:
        print("Extracting chains...")
    chains = extract_chains(graph)

    if args.verbose:
        print(f"Extracted {len(chains)} raw chains.")
        print("Pruning dominated chains...")

    chains = prune_dominated_chains(chains)

    if args.verbose:
        print(f"Remaining chains after pruning: {len(chains)}")
        print("Canonicalizing chains...")

    chains = canonicalize_chains(chains)

    if args.verbose:
        print(f"Final extracted chains: {len(chains)}")

    if args.output:
        try:
            with open(args.output, "w") as f:
                for c in chains:
                    f.write(f"{c}\n")
            if args.verbose:
                print(f"Chains saved to {args.output}")
        except Exception as e:
            print(f"Error saving output: {e}")
    else:
        print(f"\nExtracted {len(chains)} attack chains:\n")
        for c in chains:
            print("Chain:", c)


if __name__ == "__main__":
    main()
