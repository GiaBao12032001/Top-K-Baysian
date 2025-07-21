TOP-K FREQUENT BAYSIAN NETWORKS MINING IN UNCERTAIN DATA

- This respository contains an algorithmn to find and extract the TOP-K Baysian networks from uncertain transactional data sets. This method uses a expected support with a BIC-based scoring function, with a best first search algorithmn over valid Direct Acylic Graphs (DAGs)

FEATURES:

-Works on uncertain data

-Uses expected support for itemset frequency

-Scores networks using a modified BIC (Bayesian Information Criterion)

-Ensures output networks are acyclic

-Prunes search space by:

      -Sampling transactions
  
      -Limiting top-N frequent items (max_items)
  
      -Capping DAG expansions

ALGORITHMN OVERVIEW

How this works is:

1.Preprocessing:

      Filter top max_items by frequency (optional)

      Sample up to sample_size transactions

2.Candidate Edge Generation:

      Generate edges between items with expected support ≥ min_support

3.Best-First DAG Expansion:

      Start from empty DAG

      Expand by adding valid edges (no cycles)

      Score using:

      score = BIC + (weight_support × total expected support)

      Track and return top-K DAGs with highest scores

HOW TO USE

Run the Script:

      python algorithmn.py
      python main.py
      
You will be prompted for:

- Dataset type (static / csv / random):
- static made built into the code
- a random data set with a fixed size
- a csv data set to import

- Minimum support threshold

- K (number of top networks)

- Support weight (0 = use BIC only)

- Sample size (0 = use full data)

- Max number of items (0 = no limit)

IF YOU WANT TO USE A CSV

Input CSV must have:

- Header row: item names

- Each row: float values between 0 and 1, representing item presence probabilities

Example:

      milk,bread,butter
      0.8,0.2,0.0
      0.1,0.9,0.3
      ...

Example Output:

      Expanded 6 DAGs... found 5 so far.
      Top-1: Score = -13.7389, Edges = []
      Top-2: Score = -13.3962, Edges = [D->C]
      Top-3: Score = -13.1398, Edges = [C->A, D->C]
      ...
