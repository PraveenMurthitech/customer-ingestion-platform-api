from pydantic_settings import BaseSettings
class Settings(BaseSettings):
    DB_HOST: str
    DB_PORT: int = 5432
    DB_NAME: str
    DB_USER: str
    DB_PASSWORD: str

    POOL_MIN: int = 1
    POOL_MAX: int = 10

    class Config:
        env_file = ".env"

settings = Settings()