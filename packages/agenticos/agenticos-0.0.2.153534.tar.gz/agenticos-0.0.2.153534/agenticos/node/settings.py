from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    AUTH_TOKEN: str = ""
    
settings = Settings()