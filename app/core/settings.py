from typing import Final, List

from pydantic import AnyHttpUrl


class Settings(object):
    JWT_SECRET: str = "TEST_SECRET_DO_NOT_USE_IN_PROD"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 8  # 8 days

    BACKEND_CORS_ORIGINS: List[AnyHttpUrl] = []

    # @validator("BACKEND_CORS_ORIGINS", pre=True)
    # def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
    #     if isinstance(v, str) and not v.startswith("["):
    #         return [i.strip() for i in v.split(",")]
    #     elif isinstance(v, (list, str)):
    #         return v
    #     raise ValueError(v)

    SQLALCHEMY_DATABASE_URL: Final[
        str
    ] = "postgresql+asyncpg://postgres:postgres@localhost:5432/microservice-testing"
    # SQLALCHEMY_DATABASE_URL: Final[str] = 'sqlite:///example.db'
    FIRST_SUPERUSER: str = "admin"
    LIMIT_ENTITIES_DB_QUERY: Final[int] = 100

    class Config:
        case_sensitive = True


settings = Settings()
