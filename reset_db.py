import sqlite3
from pathlib import Path


ROOT = Path(__file__).resolve().parent
DATABASE = ROOT / "store.db"
SCHEMA = ROOT / "schema.sql"


def reset_database():
    if DATABASE.exists():
        DATABASE.unlink()
    connection = sqlite3.connect(DATABASE)
    try:
        connection.executescript(SCHEMA.read_text(encoding="utf-8"))
        connection.commit()
    finally:
        connection.close()
    print(f"Database reset: {DATABASE.name}")


if __name__ == "__main__":
    reset_database()
