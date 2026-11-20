from pydantic_settings import BaseSettings
from pydantic import ConfigDict
import os

class Settings(BaseSettings):
    model_config = ConfigDict(case_sensitive=True)

    PROJECT_NAME: str = "Arsi-TeX API"
    API_V1_STR: str = "/api"
    DATABASE_URL: str = os.getenv("DATABASE_URL", "sqlite:///./arsitex.db")
    TEMPLATES_DIR: str = os.getenv("TEMPLATES_DIR", "app/templates")
    STORAGE_DIR: str = os.getenv("STORAGE_DIR", "storage")

settings = Settings()
