import os
import sqlite3
import pytest
from config.env import ENV
from phases.tokenizer.essay.EssayAutoloader import autoLoadPaths
from phases.tokenizer.StreamReader import StreamReader
from phases.tokenizer.NGramExtractor import NgramExtractor
from phases.tokenizer.repository.CombinationRepository import CombinationRepository

@pytest.fixture
def setup_db(monkeypatch):
    db_path = ENV("DATABASE_PATH")
    monkeypatch.setenv("DATABASE_PATH", db_path)

    conn = sqlite3.connect(db_path)
    cursor = conn.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS combinations (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            combination TEXT NOT NULL,
            size INTEGER GENERATED ALWAYS AS (length(combination)) STORED,
            frequency INTEGER DEFAULT 1,
            UNIQUE (combination)
        );
    """)
    conn.commit()
    conn.close()

    return db_path


def test_process_project_essays(setup_db):
    essay_paths = autoLoadPaths()  # your real essay folder
    assert essay_paths, "No essay files found in ./src"

    repo = CombinationRepository()
    try:
        for path in essay_paths:
            reader = StreamReader(path, word_limit=1000)
            while True:
                has_more, chunk = reader.next()
                stats = NgramExtractor(chunk).getNgramStats()
                repo.add(stats)
                if not has_more:
                    break
    finally:
        repo.close()

    # Verify DB has data
    conn = sqlite3.connect(setup_db)
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM combinations")
    count = cursor.fetchone()[0]
    conn.close()

    assert count > 0, "No combinations were inserted from essays"
