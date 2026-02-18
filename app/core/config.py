from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    APP_NAME: str = "Product API"
    APP_VERSION: str = "1.0.0"
    API_V1_PREFIX: str = "/api/v1"

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
