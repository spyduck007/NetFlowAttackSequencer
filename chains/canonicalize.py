from typing import List, Tuple
from collections import defaultdict


def canonicalize_chains(
    chains: List[List[int]],
) -> List[List[int]]:
    groups = defaultdict(list)

    for c in chains:
        groups[(c[0], c[-1])].append(c)

    canonical = []

    for _, group in groups.items():
        group.sort(key=lambda c: (-len(c), c))
        canonical.append(group[0])

    return canonical
