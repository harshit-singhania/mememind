from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "MemeMind API"
    
    # Supabase (Production)
    SUPABASE_URL: str = ""
    SUPABASE_ANON_KEY: str = ""
    SUPABASE_SERVICE_KEY: str = ""

    # Google Cloud
    GCP_PROJECT: str = ""

    class Config:
        env_file = ".env"

settings = Settings()
