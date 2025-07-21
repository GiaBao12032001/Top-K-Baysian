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

      Candidate Edge Generation:

      Generate edges between items with expected support ≥ min_support

2.Best-First DAG Expansion:

      Start from empty DAG

      Expand by adding valid edges (no cycles)

3.Score using:

      score = BIC + (weight_support × total expected support)

      Track and return top-K DAGs with highest scores
