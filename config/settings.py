from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    META_ACCESS_TOKEN: str
    META_APP_ID: Optional[str] = None
    META_APP_SECRET: Optional[str] = None
    DEFAULT_AD_ACCOUNT: str
    META_BUSINESS_ID: Optional[str] = None

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

settings = Settings()
