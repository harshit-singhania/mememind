from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "MemeMind API"
    
    # Supabase (Production)
    SUPABASE_URL: str = ""
    SUPABASE_ANON_KEY: str = ""
    SUPABASE_SERVICE_KEY: str = ""

    # Google Cloud
    GCP_PROJECT: str = ""
    GOOGLE_API_KEY: str = ""

    class Config:
        env_file = "../../.env"
        env_file_encoding = "utf-8"

settings = Settings()
