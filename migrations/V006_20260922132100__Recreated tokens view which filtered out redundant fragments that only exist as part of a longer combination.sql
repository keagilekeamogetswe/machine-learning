-- Drop the existing view if it already exists
DROP VIEW IF EXISTS tokens;

-- Create the updated virtual table (View) named 'tokens'
CREATE VIEW tokens AS

-- Step 1: Filter out redundant fragments that only exist as part of a longer combination
WITH non_redundant_combinations AS (
    SELECT 
        c1.id,
        c1.combination,
        c1.size,
        c1.frequency
    FROM combinations c1
    WHERE NOT EXISTS (
        SELECT 1 
        FROM combinations c2
        -- Look for a strictly longer combination containing c1
        WHERE c2.size > c1.size
          AND c2.combination LIKE '%' || c1.combination || '%'
          -- If the longer combination occurs as frequently as (or more than) c1,
          -- then c1 is just a parasite fragment with no independent occurrences.
          AND c2.frequency >= c1.frequency
    )
),

-- Step 2: Calculate percentile rank on clean, non-redundant combinations
ranked_combinations AS (
    SELECT 
        id,
        combination,
        size,
        frequency,
        PERCENT_RANK() OVER (
            PARTITION BY size 
            ORDER BY frequency ASC
        ) AS pct_rank
    FROM non_redundant_combinations
)

-- Step 3: Select top 20% most frequent tokens per size category
SELECT 
    id,
    combination,
    size,
    frequency
FROM ranked_combinations
WHERE pct_rank >= 0.80;