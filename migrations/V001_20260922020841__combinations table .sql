CREATE TABLE combinations (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    combination TEXT NOT NULL,
    -- Automatically calculates length and stores it on disk
    size INTEGER GENERATED ALWAYS AS (length(combination)) STORED,
    frequency INTEGER DEFAULT 1,
    -- add combination UNIQUE constraint
    UNIQUE (combination)
);