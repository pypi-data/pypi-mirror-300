from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    AUTH_TOKEN: str = ""
    REGISTRY_URL: str = "ws://localhost:8080"
    NODE_MODE: str = "httpserver"
    HTTP_PORT: int = 8000
    AGENTIC_CONFIG_PATH: str = "src/agentic/agentic_config.py"
    HTTP_HEALTHCHECK : bool = False

    
settings = Settings()