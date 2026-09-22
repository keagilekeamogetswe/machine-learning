-- Create a virtual table (View) named 'tokens' that dynamically calculates popular combinations
CREATE VIEW tokens AS

-- Define a Common Table Expression (CTE) to calculate relative popularity per size group
WITH ranked_combinations AS (
    SELECT 
        id,
        combination,
        size,
        frequency,
        
        -- Calculate the percentile rank (0.0 to 1.0) for each combination:
        -- PARTITION BY size: Evaluates combinations independently based on length so long ones aren't drowned out by short ones.
        -- ORDER BY frequency ASC: Orders from least to most frequent to place high-frequency items near 1.0.
        PERCENT_RANK() OVER (
            PARTITION BY size 
            ORDER BY frequency ASC
        ) AS pct_rank
        
    FROM combinations
)

-- Select the fields to expose in the final 'tokens' view
SELECT 
    id,
    combination,
    size,
    frequency
FROM ranked_combinations

-- Keep only combinations in the 80th percentile or above (the top 20% most frequent per size)
WHERE pct_rank >= 0.80;