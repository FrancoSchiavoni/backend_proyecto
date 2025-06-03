import os
from dotenv import load_dotenv
load_dotenv()

from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    secret_key: str
    access_token_duration: int = 1
    algorithm: str

    class Config:
        env_file = ".env"
        env_file_encoding = "utf-8"

settings = Settings()
