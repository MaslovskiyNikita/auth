from pydantic_settings import BaseSettings, SettingsConfigDict


class RedisSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", env_prefix="REDIS_", extra="ignore"
    )

    host: str
    port: int
    db: int

    @property
    def redis_url(self) -> str:
        return f"redis://{self.host}:{self.port}/{self.db}"


class JWTTokensSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    access_token_expire: int
    refresh_token_expire: int
    jwt_hashing: str


class AppSettings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env", env_file_encoding="utf-8", extra="ignore"
    )

    db_url: str
    salt: str
    hashing_type: str
    iterations: int
    services: str
    backend_url: str
    email_host_user: str
    region: str
    aws_ses_access_key_id: str
    aws_ses_secret_access_key: str
    aws_ses_endpoint_url: str
    token_secret_key: str
    test_db_url: str

    redis_config: RedisSettings = RedisSettings()
    jwt_config: JWTTokensSettings = JWTTokensSettings()


settings = AppSettings()
