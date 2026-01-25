from pydantic_settings import BaseSettings

class Settings(BaseSettings):

    domain: str = "http://localhost"
    backend_host: str = "0.0.0.0"
    backend_port: int = 9000
    service_host: str = "0.0.0.0"
    service_port: int = 8000
    
    # PATH
    model_path: str = "ml/data/model.pkl"
    csv_data_path: str = "ml/data/hackathon_income_test.csv"
    columns_list_path: str = "ml/data/columns_list.txt"
    
    # CORS
    cors_origins: list = ["*"]
    
    class Config:
        env_file = ".env"
        case_sensitive = False
        extra = 'allow'  # разрешает лишние поля

# Создаем глобальный экземпляр
settings = Settings()