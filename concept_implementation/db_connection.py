from load_env import LoadEnvData


class DatabaseConfigs():

    def __init__(self, db_name, db_host,db_password, db_user, db_port) -> None:
        env = LoadEnvData()
        self.DB_USER = env.fetch_env_var(f"{db_user}")
        self.DB_NAME = env.fetch_env_var(f"{db_name}")
        self.DB_PASSWORD = env.fetch_env_var(f"{db_password}")
        self.DB_HOST = env.fetch_env_var(f"{db_host}")
        self.DB_PORT = env.fetch_env_var(f"{db_port}")


    def get_postgres_url(self) -> str:
        # Generate PostgreSQL URL
        return (f"postgresql://{self.DB_USER}:{self.DB_PASSWORD}@"
                f"{self.DB_HOST}:{self.DB_PORT}/{self.DB_NAME}")