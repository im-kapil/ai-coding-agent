from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    OPENAI_API_KEY: str = ""
    OPENAI_MODEL: str = "gpt-4.1"

    class Config:
        env_file = ".env"

settings = Settings()