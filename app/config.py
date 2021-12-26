from pydantic import BaseSettings


# Application settings
class Settings(BaseSettings):
    database_hostname: str
    database_port: str
    database_password: str
    database_username: str
    database_name: str
    secret_key: str
    signing_algorithm: str
    access_token_expire_min: int

    class Config:
        env_file = ".env"


# Creating instance of settings class
settings = Settings()
