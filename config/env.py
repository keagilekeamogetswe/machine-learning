import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, "..", ".env")
DEFAULT_DATABASE = "machine-learning.db"

# Load variables from .env file
load_dotenv(ENV_PATH)

# Alias getenv to ENV
ENV = os.getenv

# Resolve the database path from the environment, with a repository-local default
raw_database_path = ENV("DATABASE_PATH")
if raw_database_path is None:
    raw_database_path = ENV("DATABASE") or DEFAULT_DATABASE
    DATABASE_PATH = os.path.join(BASE_DIR, "..", raw_database_path)
else:
    DATABASE_PATH = raw_database_path

os.environ["DATABASE_PATH"] = DATABASE_PATH
