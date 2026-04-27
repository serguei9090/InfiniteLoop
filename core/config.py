from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    llm_base_url: str = "http://127.0.0.1:1234/v1"
    llm_api_key: str = "lm-studio"
    llm_model: str = "qwen/qwen3.5-9b"

    litellm_proxy_url: str = "http://127.0.0.1:4000/v1"
    litellm_api_key: str = "test"

    architect_base_url: str = "http://127.0.0.1:4000/v1"
    architect_api_key: str = "test"

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8", extra="ignore")

settings = Settings()
