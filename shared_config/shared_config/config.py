from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    domain: str = "http://localhost"
    backend_host: str = "backend"
    backend_port: int = 9000
    service_host: str = "ml"
    service_port: int = 8000
    frontend_host: str = "frontend"
    frontend_port: int = 3000
    
    # PATH
    csv_data_path: str = "data/hackathon_income_test.csv"
    clients_db_path: str = "data/clients.db"
    
    # CORS
    cors_origins: list = ["*"]
    
    class Config:
        #env_file = ".env"
        case_sensitive = False
        extra = 'allow'  # разрешает лишние поля

# Создаем глобальный экземпляр
settings = Settings()