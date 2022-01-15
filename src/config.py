import logging
import os

from functools import lru_cache, partial
from typing import Any, Callable, Dict, Optional, Type, TypeVar, cast

from pydantic import BaseSettings, validator
from pydantic.env_settings import SettingsError
from pydantic.errors import ConfigError
from pydantic.networks import PostgresDsn
from pydantic.types import SecretStr

T = TypeVar("T")


DEFAULT_APP_NAME = "BeARzzzBot"


class BaseConfig(BaseSettings):
    class Config:
        case_sensitive = True
        extra = "allow"


class CommonSettings(BaseConfig):
    LOG_LEVEL: str = "INFO"

    @validator("LOG_LEVEL")
    def __set_log_level(cls, v: str):
        if not v and v != 0:
            return "INFO"
        level = logging.getLevelName(v.upper())
        return logging._levelToName[level]

    ENV: str = "development"
    DEV: bool = True
    APP_NAME: str = DEFAULT_APP_NAME


class DBSettings(BaseConfig):
    POSTGRES_HOST: Optional[str] = None
    POSTGRES_PORT: str = "5432"
    POSTGRES_USER: Optional[str] = None
    POSTGRES_PASSWORD: Optional[SecretStr] = None
    POSTGRES_DB: Optional[str] = None
    SQLALCHEMY_DATABASE_URI: Optional[PostgresDsn] = None

    @validator("SQLALCHEMY_DATABASE_URI", pre=True)
    def __assemble_pg_dsn(
        cls, v: Optional[str], values: Dict[str, Any]  # noqa: B902
    ) -> Any:
        if isinstance(v, str) and v:
            return v
        password = values.get("POSTGRES_PASSWORD")
        return PostgresDsn.build(
            scheme="postgresql",
            user=values.get("POSTGRES_USER"),
            password=password.get_secret_value() if password else None,
            host=str(values.get("POSTGRES_HOST")),
            port=values.get("POSTGRES_PORT") or "5432",
            path=f"/{values.get('POSTGRES_DB') or ''}",
        )


class LineBotSettings(BaseConfig):
    CHANNEL_ACCESS_TOKEN: str
    CHANNEL_SECRET: str
    GROUPIDA: str
    GROUPIDB: str
    LIFFID: str


class Settings(
    CommonSettings,
    DBSettings,
    LineBotSettings,
):
    ...


def settings_loader(settings_cls: Type["T"]) -> "T":
    _env_file = os.getenv("ENV_FILE", ".env")
    try:
        return settings_cls(_env_file=_env_file)
    except (ConfigError, SettingsError, ValueError, KeyError, AttributeError) as e:
        raise ConfigError(e)


def cache_settings_factory(factory: Type["T"]) -> Callable[..., "T"]:
    fn = partial(settings_loader, factory)
    return cast('Callable[..., "T"]', lru_cache(fn))


get_settings = cache_settings_factory(Settings)
