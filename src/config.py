import os

from dotenv import load_dotenv


load_dotenv()

class Settings:
    db_host: str = os.getenv("DB_HOST", "localhost")
    db_port: int = int(os.getenv("DB_PORT", "5432"))
    db_name: str = os.getenv("DB_NAME", "")
    db_user: str = os.getenv("DB_USER", "")
    db_pass: str = os.getenv("DB_PASS", "")
    db_echo: bool = bool(os.getenv("DB_ECHO", False))

    jwt_secret_key: str = os.getenv("JWT_SECRET_KEY", "")
    jwt_algorithm: str = os.getenv("JWT_ALGORITHM", "HS256")
    jwt_access_token_expired_minute: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRED_MINUTE", 10))
    jwt_refresh_token_expired_minute: int = int(os.getenv("JWT_ACCESS_TOKEN_EXPIRED_MINUTE", 3600))

    @property
    def database_url(self) -> str:
        return (
            f"postgresql+asyncpg://{self.db_user}:{self.db_pass}"
            f"@{self.db_host}:{self.db_port}/{self.db_name}"
        )


settings = Settings()