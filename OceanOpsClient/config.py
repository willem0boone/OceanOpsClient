from pydantic import Field
from pydantic import SecretStr
from pydantic_settings import BaseSettings
from pydantic_settings import CliSettingsSource
from pydantic_settings import SettingsConfigDict


class Settings(BaseSettings):
    API_KEY_ID: str = Field(..., description="OceanOPS API key ID")
    API_KEY_TOKEN: SecretStr = Field(..., description="OceanOPS API token")

    model_config = SettingsConfigDict(env_file=".env")

    @classmethod
    def settings_customise_sources(
        cls,
        settings_cls,
        init_settings,
        env_settings,
        dotenv_settings,
        file_secret_settings,
    ):
        return (
            CliSettingsSource(settings_cls),
            init_settings,
            env_settings,
            dotenv_settings,
            file_secret_settings,
        )
