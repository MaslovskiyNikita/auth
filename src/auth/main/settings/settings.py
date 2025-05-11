from pydantic import Field
from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisSettings(BaseSettings):
    redis_host: str = Field(..., env="REDIS_HOST")
    redis_port: int = Field(..., env="REDIS_PORT")
    redis_db: int = Field(..., env="REDIS_DB")
    celery_broker_url: str = Field(..., env="CELERY_BROKER_URL")

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    @property
    def redis_url(self):
        return f"redis://{self.redis_host}:{self.redis_port}/{self.redis_db}"


class Settings(BaseSettings):
    db_url: str = Field(..., env="DB_URL")
    salt: str = Field(..., env="SALT")
    hashing_type: str = Field(..., env="HASHING_TYPE")
    iterations: int = Field(..., env="ITERATIONS")

    redis_settings: RedisSettings = RedisSettings()

    services: str = Field(..., env="SERVICES")
    backend_url: str = Field(..., env="BACKEND_URL")
    email_host_user: str = Field(..., env="EMAIL_HOST_USER")
    region: str = Field(..., env="REGION")
    aws_ses_access_key_id: str = Field(..., env="AWS_SES_ACCESS_KEY_ID")
    aws_ses_secret_access_key: str = Field(..., env="AWS_SES_SECRET_ACCESS_KEY")
    aws_ses_endpoint_url: str = Field(..., env="AWS_SES_ENDPOINT_URL")
    token_secret_key: str = Field(..., env="TOKEN_SECRET_KEY")
    test_db_url: str = Field(..., env="TEST_DB_URL")

    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )


settings = Settings()
