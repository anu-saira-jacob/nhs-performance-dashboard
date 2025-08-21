# src/db.py
from sqlalchemy import create_engine
import pandas as pd

# To keep DB credentials
DB_USER = "<your_db_user>"
DB_PASS = "<your_db_password>"
DB_HOST = "<your_db_host>"
DB_PORT = "<your_db_port>"
DB_NAME = "<your_db_name>"

DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
engine = create_engine(DATABASE_URL)


def fetch_df(query, params=None):
    with engine.connect() as conn:
        try:
            return pd.read_sql(query, conn, params=params)
        except TypeError:
            return pd.read_sql(query, conn)



