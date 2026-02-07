from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    domain: str = "http://localhost"
    backend_host: str = "0.0.0.0"
    backend_port: int = 9000
    service_host: str = "0.0.0.0"
    service_port: int = 8000
    frontend_host: str = "0.0.0.0"
    frontend_port: int = 3000
    
    # PATH
    model_path: str = "data/model.pkl"
    csv_data_path: str = "data/hackathon_income_test.csv"
    columns_list_path: str = "data/columns_list.txt"
    clients_db_path: str = "data/clients.db"
    
    # CORS
    cors_origins: list = ["*"]
    
    class Config:
        env_file = "config/.env"
        case_sensitive = False
        extra = 'allow'  # разрешает лишние поля

# Создаем глобальный экземпляр
settings = Settings()