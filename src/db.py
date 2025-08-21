# src/db.py
from sqlalchemy import create_engine
import pandas as pd

# To keep DB credentials
DB_USER = "postgres"
DB_PASS = "postgres"
DB_HOST = "localhost"
DB_PORT = "5432"
DB_NAME = "nhs_dashboard"

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)


def fetch_df(query, params=None):
    with engine.connect() as conn:
        try:
            return pd.read_sql(query, conn, params=params)
        except TypeError:
            return pd.read_sql(query, conn)



