import os
from dataclasses import dataclass

from dotenv import load_dotenv


load_dotenv()


@dataclass
class Configuration:

    version: str = os.getenv(
        "KRISH_VERSION",
        "1.0.0"
    )

    environment: str = os.getenv(
        "KRISH_ENV",
        "development"
    )

    database: str = os.getenv(
        "KRISH_DB",
        "data/krish.db"
    )

    ollama_host: str = os.getenv(
        "OLLAMA_HOST",
        "http://127.0.0.1:11434"
    )

    ollama_model: str = os.getenv(
        "OLLAMA_MODEL",
        "qwen2.5:3b"
    )

    log_level: str = os.getenv(
        "KRISH_LOG_LEVEL",
        "INFO"
    )

    max_memory: int = int(
        os.getenv(
            "KRISH_MAX_MEMORY",
            "1000"
        )
    )

    session_minutes: int = int(
        os.getenv(
            "KRISH_SESSION_MINUTES",
            "30"
        )
    )