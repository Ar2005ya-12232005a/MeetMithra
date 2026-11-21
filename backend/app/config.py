from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(env_file=".env", extra="ignore")

    anthropic_api_key: str = ""
    supabase_url: str = ""
    supabase_service_key: str = ""
    supabase_anon_key: str = ""
    database_url: str = ""
    frontend_url: str = "http://localhost:3000"
    slack_webhook_url: str = ""

    extraction_model: str = "claude-haiku-5-5"
    chat_model: str = "claude-sonnet-5-5"


settings = Settings()