TOP-K FREQUENT BAYESIAN NETWORKS MINING IN UNCERTAIN DATA

- This repository contains an algorithm to find and extract the TOP-K Beyesian networks from uncertain transactional data sets. This method uses a expected support with a BIC-based scoring function, with a best first search algorithmn over valid Direct Acylic Graphs (DAGs)

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

First you run the alogrithm then the main to make sure main can import from the aglorithm

      python algorithmn.py
      python main.py
      
You will be prompted for:

- Dataset type (static / csv / random / groceries):

        - static made built into the code
        - a random data set with a fixed size
        - a csv data set to import
        - an edge case, used for Groceries_Dataset.csv testing, and any other dataset like it.

- Minimum support threshold

- K (number of top networks)

- Support weight (0 = use BIC only)

- Sample size (0 = use full data)

- Max number of items (0 = no limit)

HOW TO USE A CUSTOM CSV

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

EVALUATION:

- This algorithm has been tested and compared with the baselines of apiori and FP-GROWTH and it has produced similar results using the Kaggle Groceries Dataset
- Unlike the sandard, it does show which products are bought with which, such as which product tends to be bought alongside another one:
  
  Example being Edges: [('whole milk', 'other vegetables')] Score: -14951.444591597454: shows that whole milk is likely to be boughyt with other vegetables.
  
- This algorithmn:

        Edges: [] Score: -14960.236718021642
        Edges: [('whole milk', 'other vegetables')] Score: -14951.444591597454
        Edges: [('rolls/buns', 'whole milk'), ('whole milk', 'other vegetables')] Score: -14943.943611318413
        Edges: [('rolls/buns', 'whole milk'), ('whole milk', 'other vegetables'), ('whole milk', 'yogurt')] Score: -14937.600814715435
        Edges: [('rolls/buns', 'whole milk'), ('whole milk', 'other vegetables'), ('whole milk', 'soda'), ('whole milk', 'yogurt')] Score: -14931.313400037438
        Edges: [('other vegetables', 'frankfurter'), ('rolls/buns', 'whole milk'), ('whole milk', 'other vegetables'), ('whole milk', 'soda'), ('whole milk', 'yogurt')] Score: -14927.04919472743
        Edges: [('other vegetables', 'frankfurter'), ('rolls/buns', 'whole milk'), ('whole milk', 'canned beer'), ('whole milk', 'other vegetables'), ('whole milk', 'soda'), ('whole milk', 'yogurt')] Score: -14923.312506237555
        Edges: [('other vegetables', 'frankfurter'), ('rolls/buns', 'whole milk'), ('whole milk', 'canned beer'), ('whole milk', 'other vegetables'), ('whole milk', 'root vegetables'), ('whole milk', 'soda'), ('whole milk', 'yogurt')] Score: -14919.773674190916
        Edges: [('other vegetables', 'frankfurter'), ('rolls/buns', 'whole milk'), ('whole milk', 'canned beer'), ('whole milk', 'other vegetables'), ('whole milk', 'root vegetables'), ('whole milk', 'sausage'), ('whole milk', 'soda'), ('whole milk', 'yogurt')] Score: -14916.728670319533
        Edges: [('other vegetables', 'frankfurter'), ('rolls/buns', 'whole milk'), ('whole milk', 'canned beer'), ('whole milk', 'other vegetables'), ('whole milk', 'root vegetables'), ('whole milk', 'sausage'), ('whole milk', 'soda'), ('whole milk', 'tropical fruit'), ('whole milk', 'yogurt')] Score: -14913.814612864788

  - Apiori:

                support            itemsets
    
            2  0.157923        (whole milk)
            0  0.122101  (other vegetables)
            1  0.110005        (rolls/buns)
  - FP-GROWTH:
    
                support            itemsets
    
            1  0.156519        (whole milk)
            2  0.121299  (other vegetables)
            0  0.108802        (rolls/buns)

- However, there is one caveat. The algorithm is significantly slower than that of the baselines. Mostly due to BIC scoring and scanning for edge cases, expanding DAGs. It's why we had to set limitations, on samplesizes, item sizes, and such to have it run at an acceptable runtime.
