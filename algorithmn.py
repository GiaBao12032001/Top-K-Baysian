import math
import heapq
from typing import List, Dict, Set, Tuple, Optional

Transaction = Dict[str, float]
Edge = Tuple[str, str]


def expected_support(itemset: Set[str], data: List[Transaction]) -> float:
    total = 0.0
    for t in data:
        prod = 1.0
        for item in itemset:
            prod *= t.get(item, 0.0)
        total += prod
    return total


def has_cycle(nodes: List[str], edges: Set[Edge]) -> bool:
    children = {n: [] for n in nodes}
    for u, v in edges:
        children[u].append(v)
    visited, stack = set(), set()

    def dfs(u: str) -> bool:
        visited.add(u)
        stack.add(u)
        for v in children.get(u, []):
            if v not in visited:
                if dfs(v):
                    return True
            elif v in stack:
                return True
        stack.remove(u)
        return False

    for n in nodes:
        if n not in visited and dfs(n):
            return True
    return False


def is_dag(nodes: List[str], edges: Set[Edge]) -> bool:
    return not has_cycle(nodes, edges)


def compute_score(
    nodes: List[str],
    edges: Set[Edge],
    data: List[Transaction],
    weight_support: float,
    marginals: Dict[str, float]
) -> float:
    parents = {n: [] for n in nodes}
    for u, v in edges:
        parents[v].append(u)

    support_sum = 0.0
    for node in nodes:
        if parents[node]:
            itemset = set(parents[node] + [node])
            support_sum += expected_support(itemset, data)

    for node in nodes:
        if len(parents[node]) > 2:
            return -float("inf")

    loglike = 0.0
    N = len(data)
    param_count = 0

    for node in nodes:
        P = parents[node]
        if P:
            for bits in range(2**len(P)):
                total_count = count_X1 = 0.0
                for t in data:
                    prob = 1.0
                    for i, p in enumerate(P):
                        prob *= t.get(p, 0.0) if (bits >> i) & 1 else (1 - t.get(p, 0.0))
                    total_count += prob
                    count_X1 += prob * t.get(node, 0.0)
                count_X0 = total_count - count_X1
                if total_count > 0:
                    param_count += 1
                    if count_X1 > 0:
                        loglike += count_X1 * math.log(count_X1 / total_count)
                    if count_X0 > 0:
                        loglike += count_X0 * math.log(count_X0 / total_count)
        else:
            total_count = float(N)
            count_X1 = marginals[node]
            count_X0 = total_count - count_X1
            if total_count > 0:
                param_count += 1
                if count_X1 > 0:
                    loglike += count_X1 * math.log(count_X1 / total_count)
                if count_X0 > 0:
                    loglike += count_X0 * math.log(count_X0 / total_count)

    bic = loglike - (math.log(N) / 2.0) * param_count
    return bic + weight_support * support_sum


def top_k_bayesian_networks(
    data: List[Transaction],
    min_support: float,
    K: int,
    weight_support: float,
    sample_size: Optional[int],
    max_items: Optional[int]
) -> List[Tuple[Set[Edge], float]]:
    if max_items is not None and max_items > 0:
        from collections import Counter
        item_freq = Counter(item for txn in data for item in txn)
        top_items = set(item for item, _ in item_freq.most_common(max_items))
        data = [{k: v for k, v in txn.items() if k in top_items} for txn in data]
        print("Remaining transactions:", len(data))
        print("Unique items remaining in sample:", len({item for txn in data for item in txn}))

    if sample_size is not None and sample_size < len(data):
        import random
        data = random.sample(data, sample_size)

    nodes = sorted({x for t in data for x in t.keys()})
    marginals = {node: sum(t.get(node, 0.0) for t in data) for node in nodes}
    edges_candidates = []

    for i in range(len(nodes)):
        for j in range(i + 1, len(nodes)):
            sup = expected_support({nodes[i], nodes[j]}, data)
            if sup >= min_support:
                edges_candidates.append((nodes[i], nodes[j]))
                edges_candidates.append((nodes[j], nodes[i]))

    initial_edges = frozenset()
    initial_score = compute_score(nodes, initial_edges, data, weight_support, marginals)
    heap = [(-initial_score, initial_edges)]
    visited = set()
    top_networks = []
    MAX_EXPANSIONS = 20
    loop_count = 0

    while heap and len(top_networks) < K and loop_count < MAX_EXPANSIONS:
        loop_count += 1
        negscore, edges = heapq.heappop(heap)
        score = -negscore
        print(f"Expanded {loop_count} DAGs... found {len(top_networks)} so far.")
        if edges in visited:
            continue
        visited.add(edges)
        top_networks.append((edges, score))

        for e in edges_candidates:
            if e in edges:
                continue
            new_edges = set(edges)
            new_edges.add(e)
            if is_dag(nodes, new_edges):
                new_edges = frozenset(new_edges)
                if new_edges not in visited:
                    new_score = compute_score(nodes, new_edges, data, weight_support, marginals)
                    heapq.heappush(heap, (-new_score, new_edges))

    return top_networks
