from functools import lru_cache
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")
    database_url: str = "sqlite:///./data/shop.db"
    product_storage_path: Path = Path("products/approved")
    base_url: str = "http://localhost:8000"
    admin_token: str = "change-me-before-deploying"
    download_token_ttl_hours: int = 24
    stripe_secret_key: str = ""
    stripe_webhook_secret: str = ""
    openai_api_key: str = ""
    llm_provider: str = "deterministic"
    max_new_products_per_day: int = 5
    max_llm_cost_per_day: float = 5
    max_regenerations_per_product: int = 2
    min_product_score: float = 75

    def prepare(self) -> None:
        Path("data").mkdir(exist_ok=True)
        self.product_storage_path.mkdir(parents=True, exist_ok=True)


@lru_cache
def get_settings() -> Settings:
    settings = Settings()
    settings.prepare()
    return settings

