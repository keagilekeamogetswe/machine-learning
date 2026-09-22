import sqlite3
from config.env import ENV
import os

connection = sqlite3.connect(ENV("DATABASE_PATH"))
cursor = connection.cursor()

connection.commit()
connection.close()
