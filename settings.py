from pydantic.v1 import BaseSettings


class Settings(BaseSettings):
    BOT_TOKEN: str
    DATABASE_URL: str
    ADMINS: str

    class Config:
        env_file = '.env'


env_settings = Settings()