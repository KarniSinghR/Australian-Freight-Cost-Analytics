"""
db.py — Database connection helper.

Creates a SQLAlchemy engine that every ETL script imports,
so the connection details live in exactly one place.
"""

from sqlalchemy import create_engine

# Local Postgres.app: passwordless connection for the Mac user.
# Format: postgresql://USER@HOST:PORT/DATABASE
DB_USER = "karnisinghrathore"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "freight_analytics"

CONNECTION_STRING = f"postgresql://{DB_USER}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# The engine is the object SQLAlchemy uses to talk to the database.
engine = create_engine(CONNECTION_STRING)


# Quick self-test: run `python src/db.py` to check the connection works.
if __name__ == "__main__":
    from sqlalchemy import text
    with engine.connect() as conn:
        result = conn.execute(text("SELECT current_user;"))
        print("Connected as:", result.scalar())
