from algorithm import top_k_bayesian_networks
import csv
import random
from typing import List, Dict, Optional

Transaction = Dict[str, float]

def load_csv(filename: str) -> List[Transaction]:
    """Load probabilistic transaction data from a CSV file."""
    data = []
    try:
        with open(filename, newline='') as csvfile:
            reader = csv.DictReader(csvfile)
            for row in reader:
                data.append({k: float(v) for k, v in row.items()})
    except FileNotFoundError:
        print(f"File not found: {filename}")
        exit(1)
    return data

def generate_random_data(n_transactions: int, n_items: int) -> List[Transaction]:
    """Generate synthetic probabilistic transactions with random values."""
    data = []
    for _ in range(n_transactions):
        txn = {}
        for i in range(n_items):
            item = chr(ord('A') + i)
            txn[item] = round(random.uniform(0.0, 1.0), 2)
        data.append(txn)
    return data

def get_static_data() -> List[Transaction]:
    """Use a fixed small dataset for testing/debugging."""
    return [
        {"A": 0.1, "B": 0.1},
        {"A": 0.9, "C": 0.8},
        {"B": 0.3, "D": 0.4},
        {"C": 0.9, "D": 0.95},
        {"B": 0.2, "C": 0.1},
    ]

if __name__ == "__main__":
    print("=== Top-K Bayesian Network Search ===")
    mode = input("Select data mode (static / csv / random): ").strip().lower()

    if mode == "csv":
        path = input("Enter CSV file path: ").strip()
        data = load_csv(path)
    elif mode == "random":
        n_txn = int(input("Number of transactions: "))
        n_items = int(input("Number of items: "))
        data = generate_random_data(n_txn, n_items)
    else:
        data = get_static_data()

    # Get algorithm parameters
    min_support = float(input("Enter min support (e.g. 0.3): "))
    K = int(input("Enter top-K (e.g. 5): "))
    weight_support = float(input("Enter weight for support in scoring (e.g. 0): "))
    sample_size = int(input("Enter sample size (0 = full data): "))
    sample_size = None if sample_size == 0 or sample_size > len(data) else sample_size

    max_items_input = input("Enter max number of items to keep (0 = no limit): ").strip()
    max_items: Optional[int] = int(max_items_input) if max_items_input.isdigit() and int(max_items_input) > 0 else None

    print("\nRunning Top-K search...")
    topK = top_k_bayesian_networks(data, min_support, K, weight_support, sample_size, max_items)

    print("\n==== Top-K Structures ====")
    for idx, (edges, score) in enumerate(topK, 1):
        edge_str = ', '.join([f"{a}->{b}" for a, b in sorted(edges)])
        print(f"Top-{idx}: Score = {score:.4f}, Edges = [{edge_str}]")
