from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    database_url: str = "postgresql://postgres:admin@172.23.224.1:5433/fastapi"

    class Config:
        env_file = ".env"  # Nếu muốn sử dụng tệp .env trong dự án

# Tạo đối tượng cấu hình
settings = Settings()

# Truyền giá trị DATABASE_URL vào ứng dụng FastAPI
# print(settings.Config)
