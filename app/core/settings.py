from typing import Final


class Settings(object):
    SQLALCHEMY_DATABASE_URL: Final[
        str
    ] = "postgresql+asyncpg://postgres:postgres@localhost:5432/microservice-testing"
    # SQLALCHEMY_DATABASE_URL: Final[str] = 'sqlite:///example.db'
    FIRST_SUPERUSER: str = "admin"
    LIMIT_ENTITIES_DB_QUERY: Final[int] = 100


settings = Settings()
