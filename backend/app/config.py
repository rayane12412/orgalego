"""Configuration centralisée de l'application."""

from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Settings chargés depuis l'environnement ou .env."""

    app_name: str = "OrgaLego"
    version: str = "0.1.0"
    debug: bool = True

    # CORS
    cors_origins: list[str] = [
        "http://localhost:5173",
        "http://localhost:3000",
        "http://127.0.0.1:5173",
    ]

    # Chemins
    base_dir: Path = Path(__file__).resolve().parent
    blocks_dir: Path = base_dir / "blocks"

    # Base de données
    database_url: str = "sqlite:///./orgalego.db"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
