import os
from typing import Optional
from dotenv import load_dotenv
from pydantic import SecretStr
from functools import lru_cache

load_dotenv()


class Config:
    """Base configuration class for the financial analysis application."""

    DATABASE_CONNECTION_STRING: SecretStr = SecretStr(
        os.getenv("DATABASE_CONNECTION_STRING", "")
    )

    PROJECT_NAME: str = "Financial Analysis API"
    PROJECT_VERSION: str = "1.0.0"

    @classmethod
    def validate_config(cls) -> None:
        """Validate that required secret environment variables are set."""
        required_secrets = {
            "DATABASE_CONNECTION_STRING": cls.DATABASE_CONNECTION_STRING.get_secret_value(),
        }

        missing_secrets = [
            var_name
            for var_name, var_value in required_secrets.items()
            if not var_value or var_value == "<secret_here>"
        ]

        if missing_secrets:
            raise ValueError(
                f"Missing required secret environment variables: {', '.join(missing_secrets)}. "
                f"Please check your .env file."
            )

    @classmethod
    def get_database_url(cls) -> str:
        """Get the database connection URL with secret password."""
        return cls.DATABASE_CONNECTION_STRING.get_secret_value()



@lru_cache(maxsize=1)
def getConfig() -> Config:
    config = Config()
    config.validate_config()
    return config
