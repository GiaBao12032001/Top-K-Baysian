from algorithm import top_k_bayesian_networks
from typing import List, Dict
import csv
import random
from collections import defaultdict

Transaction = Dict[str, float]

def load_csv(filename: str) -> List[Transaction]:
    """Load probabilistic transaction data from a CSV file (header = item names, values = probabilities)."""
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

def load_groceries_uncertain(csv_path: str, min_prob: float = 0.5, max_prob: float = 1.0, seed: int = 42) -> List[Transaction]:
    """Convert Groceries_dataset.csv into uncertain data format with random probabilities."""
    random.seed(seed)
    transactions = defaultdict(list)
    try:
        with open(csv_path, newline='', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            for row in reader:
                txn_id = f"{row['Member_number']}|{row['Date']}"
                item = row['itemDescription'].strip()
                if item:
                    transactions[txn_id].append(item)
    except FileNotFoundError:
        print(f"File not found: {csv_path}")
        exit(1)

    uncertain_transactions = []
    for t in transactions.values():
        uncertain_t = {item: round(random.uniform(min_prob, max_prob), 2) for item in t}
        uncertain_transactions.append(uncertain_t)
    return uncertain_transactions

def generate_random_data(n_transactions: int, n_items: int) -> List[Transaction]:
    data = []
    for _ in range(n_transactions):
        txn = {}
        for i in range(n_items):
            item = chr(ord('A') + i)
            txn[item] = round(random.uniform(0.0, 1.0), 2)
        data.append(txn)
    return data

def get_static_data() -> List[Transaction]:
    return [
        {"A": 0.1, "B": 0.1},
        {"A": 0.9, "C": 0.8},
        {"B": 0.3, "D": 0.4},
        {"C": 0.9, "D": 0.95},
        {"B": 0.2, "C": 0.1},
    ]

if __name__ == "__main__":
    print("=== Top-K Bayesian Network Search ===")
    mode = input("Select data mode (static / csv / random / groceries): ").strip().lower()

    if mode == "csv":
        path = input("Enter CSV file path: ").strip()
        data = load_csv(path)
    elif mode == "groceries":
        path = input("Enter Groceries CSV file path: ").strip()
        data = load_groceries_uncertain(path)
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
    if sample_size == 0 or sample_size > len(data):
        sample_size = None
    max_items_input = input("Enter max number of items to keep (0 = no limit): ").strip()
    max_items = int(max_items_input) if max_items_input.isdigit() and int(max_items_input) > 0 else None

    print("\nRunning Top-K search...")
    topK = top_k_bayesian_networks(data, min_support, K, weight_support, sample_size, max_items)

    print("\n==== Top-K Structures ====")
    for idx, (edges, score) in enumerate(topK, 1):
        edge_str = [f"{u}->{v}" for u, v in edges]
        print(f"Top-{idx}: Score = {score:.4f}, Edges = {edge_str}")
