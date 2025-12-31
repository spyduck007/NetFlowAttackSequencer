# NetFlowAttackSequencer
Lightwieght attack chain correlation engine for netowrk flow data  

[Demo Video](https://example.com/demo-video)  
[Technical Paper](TechnicalPaper.pdf)

## What is the problem?

Modern network intrusion detection systems (NIDS) generate massive amounts of log data. While they are good at flagging individual suspicious packets or flows, they often fail to connect the dots between disparate events.

An attacker doesn't just send one packet; they perform a sequence of actions—scanning ports, exploiting vulnerabilities, and exfiltrating data. Identifying these **sequences** or "chains" of activity amidst thousands of benign events is a complex challenge, often requiring manual correlation by security analysts.

## What does it do?

**NetFlowAttackSequencer** automates the correlation of network events to discover potential attack scenarios.

It works by:

1.  **Ingesting Flow Data**: Loads raw network traffic flows (currently optimized for CIC-IDS2017 data).
2.  **Building an Event Graph**: Constructs a graph where nodes are events and edges represent relationships.
    - **Temporal Proximity**: Events happening close together in time.
    - **Port Correlation**: Events targeting the same destination port.
    - **Feature Similarity**: Events with similar flow characteristics (packet size, duration, etc.).
3.  **Extracting Chains**: Traverses the graph to find long, connected sequences of events.
4.  **Pruning & Canonicalizing**: Removes redundant sub-chains to present only the most significant, unique attack paths.

## Getting Started

### Prerequisites

- Python 3.8+
- No external libraries required (Standard Library only).

### Installation

1.  Clone the repository:

    ```bash
    git clone https://github.com/spyduck007/NetFlowAttackSequencer.git
    cd NetFlowAttackSequencer
    ```

2.  Make the CLI executable:
    ```
    chmod +x cli.py
    ```

## How do I run it?

The easiest way to use NetFlowAttackSequencer is via the included CLI tool.

### Basic Usage

Run the tool with default settings (processes the first 50 events):

```bash
./cli.py
```

### CLI Options

You can customize the execution using flags:

```bash
./cli.py --help
```

| Flag              | Description                              | Default                    |
| ----------------- | ---------------------------------------- | -------------------------- |
| `-i`, `--input`   | Path to the input CSV file               | `data/raw/cic_ids2017.csv` |
| `-l`, `--limit`   | Number of events to load                 | `50`                       |
| `-w`, `--window`  | Time window (seconds) for linking events | `3`                        |
| `-o`, `--output`  | Path to save extracted chains to a file  | (stdout)                   |
| `-v`, `--verbose` | Enable detailed progress logs            | `False`                    |

### Examples

**Process 1000 events and enable verbose logging:**

```bash
./cli.py -l 1000 -v
```

**Save the results to a file:**

```bash
./cli.py -l 500 -o results.txt
```

## Results & Output

The program outputs a list of **Attack Chains**. Each chain is a sequence of Event IDs that the algorithm has determined are strongly correlated.

Example output:

```text
Extracted 5 attack chains:

Chain: [0, 1, 2, 3, 5, 9]
Chain: [4, 7, 10, 11]
Chain: [16, 18, 19]
...
```

- **Chain `[0, 1, 2, 3, 5, 9]`**: This indicates that Event 0 likely triggered or is related to Event 1, which led to Event 2, and so on. This could represent a port scan followed by a connection attempt.
- **Interpretation**: You can map these IDs back to the original CSV rows to investigate the specific timestamps, IPs, and attack labels associated with the chain.

## Limitations & Things to Consider

- **Heuristic Approach**: The links are created based on heuristics (time windows, similarity thresholds). This is probabilistic and may generate false positives (linking unrelated events) or false negatives (missing subtle attacks).
- **Scalability**: The current implementation builds an in-memory graph. For datasets with millions of events, memory usage will be significant.
- **Data Format**: The loader is currently hardcoded for the CIC-IDS2017 CSV format. Adapting to other log formats (like Zeek or Suricata) would require writing a new loader in `core/loader.py`.
- **Time Window Sensitivity**: The `-w` (window) parameter heavily influences the graph connectivity. A window that is too small might break chains; a window that is too large might connect unrelated traffic.
