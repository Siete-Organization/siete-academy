from functools import lru_cache
from typing import Literal

from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore", case_sensitive=False)

    app_env: Literal["development", "staging", "production"] = "development"
    app_secret_key: str = "change-me"
    public_base_url: str = "http://localhost:5173"
    allowed_origins: str = "http://localhost:5173"

    # Path prefix bajo el que está servida la API (OpenAPI metadata + URL en swagger).
    # Vacío significa raíz del subdominio (ej: api-academy.wearesiete.com/auth/me).
    # NO agrega prefix a las rutas; si necesitás strip-prefix, hacelo en el reverse proxy.
    api_root_path: str = ""

    # When true, get_current_user accepts an `X-Dev-User: <email>` header
    # and skips Firebase verification. ONLY for local demo — must be false in prod.
    dev_auth_bypass: bool = True

    # When true, Celery runs tasks inline (no broker needed). ONLY for dev.
    celery_always_eager: bool = True

    database_url: str = "postgresql+psycopg://siete:siete@localhost:5432/siete_academy"
    redis_url: str = "redis://localhost:6379/0"

    firebase_credentials_json: str | None = None
    firebase_credentials_path: str | None = None
    firebase_project_id: str | None = None

    anthropic_api_key: str | None = None
    anthropic_model: str = "claude-opus-4-7"

    smtp_host: str | None = None
    smtp_port: int = 587
    smtp_user: str | None = None
    smtp_password: str | None = None
    smtp_from: str = "Siete Academy <noreply@siete.com>"

    # Slack incoming webhook que recibe la notificación cuando un alumno sube
    # el video de fin de módulo (capa_2) o de la Prueba Final. Si no está set,
    # las notificaciones quedan stubeadas (logueadas, no enviadas).
    slack_video_notify_url: str | None = None

    # Comma-separated emails que reciben rol "admin" automáticamente al loguear.
    # Setear en .env / Coolify, no hardcodear identidades aquí.
    admin_emails: str = ""

    @property
    def cors_origins(self) -> list[str]:
        return [o.strip() for o in self.allowed_origins.split(",") if o.strip()]

    @property
    def admin_emails_list(self) -> list[str]:
        return [e.strip().lower() for e in self.admin_emails.split(",") if e.strip()]


@lru_cache
def get_settings() -> Settings:
    return Settings()
