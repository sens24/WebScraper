import os
from urllib.parse import quote_plus
from dotenv import load_dotenv
from sqlalchemy import create_engine

def get_engine(**kwargs):
    load_dotenv()
    user = os.getenv("POSTGRES_USERNAME", "postgres")
    password = quote_plus(os.environ["POSTGRES_PASSWORD"])
    host = os.getenv("POSTGRES_HOST", "localhost")
    port = os.getenv("POSTGRES_PORT", "5432")
    name = os.getenv("POSTGRES_DB", "steam")
    sslmode = os.getenv("POSTGRES_SSLMODE")
    connect_args = {"sslmode": sslmode} if sslmode else {}
    url = f"postgresql+psycopg2://{user}:{password}@{host}:{port}/{name}"
    return create_engine(url, connect_args=connect_args, **kwargs)