from core.loader import load_cic_ids2017


def main():
    events = load_cic_ids2017(
        "data/raw/cic_ids2017.csv",
        limit=10
    )

    print(f"Loaded {len(events)} events\n")

    for e in events:
        print(e)


if __name__ == "__main__":
    main()
