from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    db_url: str = Field(..., env="DB_URL")
    salt: str = Field(..., env="SALT")
    hashing_type: str = Field(..., env="HASHING_TYPE")
    iterations: int = Field(..., env="ITERATIONS")

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
