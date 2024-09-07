# main.py file
from load_env import LoadEnvData
from db_connection import DatabaseConfigs


if __name__ == "__main__":
    env = LoadEnvData()
    print(env.fetch_env_var("DB_HOST"))

    # database configs

    db_config = DatabaseConfigs(db_name='DB_NAME', db_host='DB_HOST', db_password='DB_PASSWORD', db_user='DB_USER', db_port='DB_PORT')

    print(db_config.get_postgres_url())
