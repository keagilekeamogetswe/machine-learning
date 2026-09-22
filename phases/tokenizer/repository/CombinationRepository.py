import sqlite3 as mysql
from config.env import ENV

class CombinationRepository:
    def __init__(self):
        # Open persistent connection and track the execution cursor
        self.connection = mysql.connect(ENV("DATABASE_PATH"))
        self.sql = self.connection.cursor()

    def add(self, combination_stats: dict[str, dict[str, int]]):
        """
        Accepts n-gram stats from NgramExtractor.getNgramStats().
        Example:
            {
              "BP": {"size": 2, "frequency": 2},
              "PE": {"size": 2, "frequency": 2}
            }
        Inserts each combination with UPSERT logic.
        """
        for combo, meta in combination_stats.items():
            frequency = meta.get("frequency", 1)

            self.sql.execute("""
                INSERT INTO combinations (combination, frequency)
                VALUES (?, ?)
                ON CONFLICT(combination)
                DO UPDATE SET frequency = frequency + excluded.frequency;
            """, (combo, frequency))

        self.connection.commit()

    def close(self):
        """Safely closes the underlying database resources."""
        if self.sql:
            self.sql.close()
        if self.connection:
            self.connection.close()
