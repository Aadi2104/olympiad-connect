from pydantic_settings import BaseSettings,SettingsConfigDict

class Settings(BaseSettings):
    DATABASE_URL : str
    SECRET_KEY : str
    ALGORITHM : str
    ACCESS_TOKEN_EXPIRY_MINUTES : int
    SIGNUP_TOKEN_EXPIRY_MINUTES : int
    RESET_PASSWORD_TOKEN_EXPIRY_MINUTES:int
    MAIL_USERNAME:str
    MAIL_PASSWORD:str
    MAIL_FROM_NAME:str
    MAIL_FROM:str
    MAIL_PORT:str
    MAIL_SERVER:str
    MAIL_STARTTLS:bool
    MAIL_SSL_TLS:bool
    
    model_config = SettingsConfigDict(
        env_file=".env",
        extra="ignore"
    )
    
settings=Settings()
