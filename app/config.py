from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
  db_name: str
  db_password: str
  db_port: str
  db_host: str
  db_user: str
  table_name: str
  secret_key: str
  access_token_expire_minutes: int
  algorithm: str
  database_url: str

  model_config = SettingsConfigDict(env_file=".env")

  # class Config:
  #       env_file = ".env"


settings = Settings()