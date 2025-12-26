from typing import List, Tuple
from collections import defaultdict


def prune_dominated_chains(
    chains: List[List[int]],
) -> List[List[int]]:
    groups = defaultdict(list)

    for c in chains:
        groups[(c[0], c[-1])].append(c)

    pruned = []

    for _, group in groups.items():
        group.sort(key=len, reverse=True)

        kept = []

        for c in group:
            dominated = False
            for k in kept:
                it = iter(k)
                if all(x in it for x in c):
                    dominated = True
                    break

            if not dominated:
                kept.append(c)

        pruned.extend(kept)

    return pruned
