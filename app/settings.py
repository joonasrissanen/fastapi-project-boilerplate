from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    def __init__(self):
        super().__init__()

    environment: str = "development"
    log_level: str = "INFO"
    database_url: str = "postgresql+asyncpg://user:pass@postgres:5432/database"


settings = Settings()
