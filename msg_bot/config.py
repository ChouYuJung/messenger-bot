from typing import Text

from ksuid import Ksuid
from pydantic import Field
from pydantic_settings import BaseSettings
from rich.console import Console

from .version import VERSION

console = Console()


class ApplicationSettings(BaseSettings):
    APP_NAME: Text = Field(default="msg_bot")
    APP_VERSION: Text = Field(default=VERSION)


class SecretsSettings(BaseSettings):
    AWS_IOT_CORE_ENDPOINT: Text = Field(...)
    AWS_IOT_CORE_CLIENT_ID_BASE: Text | None = Field(default=None)
    AWS_IOT_CORE_CLIENT_ID: Text = Field(default="")
    AWS_IOT_CORE_SECRET_KEY_FILEPATH: Text = Field(...)
    AWS_IOT_CORE_CERTIFICATES_FILEPATH: Text = Field(...)
    AWS_IOT_CORE_CA_FILEPATH: Text = Field(...)


class PubSubSettings(BaseSettings):
    TOPIC_BASE: Text = Field(default="messenger")
    TOPIC_PATH_ORG: Text = Field(default="org")
    TOPIC_PATH_CONV: Text = Field(default="conv")
    TOPIC_PATH_MSG: Text = Field(default="msg")


class Settings(ApplicationSettings, SecretsSettings, PubSubSettings):
    def validate_attributes(self):
        if not self.AWS_IOT_CORE_CLIENT_ID:
            if not self.AWS_IOT_CORE_CLIENT_ID_BASE:
                raise ValueError(
                    "Value 'AWS_IOT_CORE_CLIENT_ID_BASE' or "
                    "'AWS_IOT_CORE_CLIENT_ID' is required"
                )
            self.AWS_IOT_CORE_CLIENT_ID = (
                f"{self.AWS_IOT_CORE_CLIENT_ID_BASE}-{str(Ksuid())}"
            )


settings = Settings()  # type: ignore
settings.validate_attributes()
