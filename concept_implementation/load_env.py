## importing the load_dotenv from the python-dotenv module
from dotenv import load_dotenv
import os

class LoadEnvData():
    
    def __init__(self) -> None:
        load_dotenv()

    def fetch_env_var(self,variable_name):
        return os.getenv(f"{variable_name}")