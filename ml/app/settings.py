from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    domain: str
    backend_host: str
    backend_port: int
    service_host: str
    service_port: int
    frontend_host: str
    frontend_port: int
    
    # PATH
    csv_data_path: str
    clients_db_path: str
    
    # CORS
    cors_origins: list = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = 'allow'  # разрешает лишние поля

# Создаем глобальный экземпляр
settings = Settings()