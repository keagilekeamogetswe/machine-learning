import os
import tempfile
import sqlite3
import pytest
from phases.tokenizer.repository.CombinationRepository import CombinationRepository

# Create a temporary database for testing
@pytest.fixture
def temp_db(monkeypatch):
    tmp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".db")
    db_path = tmp_file.name
    tmp_file.close()

    # Monkeypatch ENV("DATABASE_PATH") to return our temp file
    monkeypatch.setenv("DATABASE_PATH", db_path)

    # Initialize schema
    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE combinations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            combination TEXT NOT NULL,
            size INTEGER GENERATED ALWAYS AS (length(combination)) STORED,
            frequency INTEGER DEFAULT 1,
            UNIQUE (combination)
        );
    """)
    conn.commit()
    conn.close()

    yield db_path

    os.remove(db_path)


def test_insert_and_upsert(temp_db):
    repo = CombinationRepository()

    # First insert
    repo.add({"BP": {"size": 2, "frequency": 2}})
    # Second insert (same combo, should increment)
    repo.add({"BP": {"size": 2, "frequency": 3}})
    repo.close()

    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()
    cursor.execute("SELECT combination, size, frequency FROM combinations WHERE combination='BP'")
    row = cursor.fetchone()
    conn.close()

    assert row[0] == "BP"
    assert row[1] == 2
    assert row[2] == 5  # 2 + 3 = 5


def test_multiple_combinations(temp_db):
    repo = CombinationRepository()
    stats = {
        "PE": {"size": 2, "frequency": 1},
        "BPE": {"size": 3, "frequency": 2}
    }
    repo.add(stats)
    repo.close()

    conn = sqlite3.connect(temp_db)
    cursor = conn.cursor()
    cursor.execute("SELECT combination, frequency FROM combinations ORDER BY combination")
    rows = cursor.fetchall()
    conn.close()

    assert ("BPE", 2) in rows
    assert ("PE", 1) in rows
