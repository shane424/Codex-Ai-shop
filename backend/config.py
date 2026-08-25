from functools import lru_cache
from pathlib import Path
from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file='.env', extra='ignore')
    environment: str = 'development'
    database_url: str = 'sqlite:///./data/money_maker.db'
    product_storage_path: Path = Path('./products/approved')
    openai_api_key: str = ''
    llm_provider: str = 'mock'
    stripe_secret_key: str = ''
    stripe_webhook_secret: str = ''
    base_url: str = 'http://localhost:3000'
    cors_origins: list[str] = ['http://localhost:3000']
    admin_token: str = 'change-me'
    max_new_products_per_day: int = Field(5, ge=0, le=100)
    max_llm_cost_per_day: float = Field(5, ge=0, le=1000)
    max_regenerations_per_product: int = Field(2, ge=0, le=10)
    min_product_score: float = Field(75, ge=0, le=100)
    download_ttl_minutes: int = Field(1440, ge=1, le=10080)
    download_limit: int = Field(3, ge=1, le=20)
    enable_scheduler: bool = False

    @field_validator('cors_origins', mode='before')
    @classmethod
    def split_origins(cls, value):
        return [x.strip() for x in value.split(',')] if isinstance(value, str) else value

@lru_cache
def get_settings() -> Settings:
    return Settings()
