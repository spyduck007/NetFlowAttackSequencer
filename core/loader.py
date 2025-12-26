import csv
from datetime import datetime, timedelta
from typing import List
from .event import Event


def _get(row, key):
    for k in row:
        if k.strip().lower() == key.lower():
            return row[k]
    raise KeyError(f"Column '{key}' not found")


def load_cic_ids2017(csv_path: str, limit: int = 1000) -> List[Event]:
    events = []

    base_time = datetime(2017, 7, 7, 13, 0, 0)

    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)

        for idx, row in enumerate(reader):
            if idx >= limit:
                break

            timestamp = base_time + timedelta(seconds=idx)

            event = Event(
                event_id=idx,
                timestamp=timestamp,
                destination_port=int(_get(row, "Destination Port")),
                label=_get(row, "Label").strip(),
                features={
                    "flow_duration": float(_get(row, "Flow Duration")),
                    "total_fwd_packets": float(_get(row, "Total Fwd Packets")),
                    "total_bwd_packets": float(_get(row, "Total Backward Packets")),
                    "syn_flag_count": float(_get(row, "SYN Flag Count")),
                    "ack_flag_count": float(_get(row, "ACK Flag Count")),
                    "packet_length_mean": float(_get(row, "Packet Length Mean")),
                    "flow_bytes_per_sec": float(_get(row, "Flow Bytes/s")),
                },
            )

            events.append(event)

    return events
