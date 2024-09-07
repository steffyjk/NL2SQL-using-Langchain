from load_env import LoadEnvData
from langchain_community.utilities.sql_database import SQLDatabase
from sqlalchemy import create_engine
from groq import Groq

env = LoadEnvData()


class DatabaseConfigs:

    def __init__(self, db_name, db_host, db_password, db_user, db_port) -> None:
        self.DB_USER = env.fetch_env_var(f"{db_user}")
        self.DB_NAME = env.fetch_env_var(f"{db_name}")
        self.DB_PASSWORD = env.fetch_env_var(f"{db_password}")
        self.DB_HOST = env.fetch_env_var(f"{db_host}")
        self.DB_PORT = env.fetch_env_var(f"{db_port}")

    def get_postgres_uri(self) -> str:
        # Generate PostgreSQL URL
        return (
            f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@"
            f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}"
        )
    
    def create_engine(self, db_uri):
        return create_engine(db_uri)

    def create_db_connection(self, db_uri):
        engine = create_engine(db_uri)
        db = SQLDatabase(engine=engine)
        return db


class GroqConnetion:

    def __init__(self, groq_api_key) -> None:
        self.api_key = env.fetch_env_var(f"{groq_api_key}")

    def create_client(self):
        # Create a Groq client
        return Groq(
            api_key=self.api_key,
        )
