import os
from dotenv import load_dotenv

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ENV_PATH = os.path.join(BASE_DIR, "..", ".env")

# Load variables from .env file
load_dotenv(ENV_PATH)

# Alias getenv to ENV
ENV = os.getenv

# Get database path from .env and resolve relative path
DATABASE_PATH = os.path.join(BASE_DIR, "..", ENV("DATABASE"))
os.environ["DATABASE_PATH"] = DATABASE_PATH
