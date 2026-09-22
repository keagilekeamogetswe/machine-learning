import importlib
import os

import config.env as env_module


def test_database_path_defaults_when_database_env_missing(monkeypatch):
    monkeypatch.delenv("DATABASE", raising=False)
    monkeypatch.delenv("DATABASE_PATH", raising=False)

    reloaded_env = importlib.reload(env_module)

    expected_path = os.path.join(reloaded_env.BASE_DIR, "..", "machine-learning.db")
    assert reloaded_env.DATABASE_PATH == expected_path
    assert os.environ["DATABASE_PATH"] == expected_path


def test_database_path_preserves_existing_database_path(monkeypatch):
    database_path = "/tmp/test-machine-learning.db"
    monkeypatch.delenv("DATABASE", raising=False)
    monkeypatch.setenv("DATABASE_PATH", database_path)

    reloaded_env = importlib.reload(env_module)

    assert reloaded_env.DATABASE_PATH == database_path
    assert os.environ["DATABASE_PATH"] == database_path
