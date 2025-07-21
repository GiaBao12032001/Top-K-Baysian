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

