import secrets
from abc import (
    ABC,
    abstractmethod,
)
from redis import Redis

from core import config


class AbstractTokensHelper(ABC):
    @abstractmethod
    def token_exists(
        self,
        token: str,
    ) -> bool:
        """
        Проверка на существование и валидность токена
        """

    @abstractmethod
    def add_token(
        self,
        token: str,
    ) -> None:
        """
        Сохранить токен в БД
        """

    @classmethod
    def generate_token(cls) -> str:
        return secrets.token_urlsafe(16)

    def generete_and_save_token(self) -> str:
        token = self.generate_token()
        self.add_token(token)
        return token


class RedisTokenHandler(AbstractTokensHelper):
    def __init__(
        self,
        host: str,
        port: int,
        db: int,
        tokens_set_name: str,
    ):
        redis = Redis(
            host=host,
            port=port,
            db=db,
            decode_responses=True,
        )
        self.tokens_set = tokens_set_name

    def token_exists(
        self,
        token: str,
    ) -> bool:
        return bool(
            self.redis.sismember(
                self.tokens_set,
                token,
            )
        )

    def add_token(
        self,
        token: str,
    ) -> None:
        self.redis.sadd(
            self.tokens_set,
            token,
        )


redis_tokens = RedisTokenHandler(
    host=config.REDIS_HOST,
    port=config.REDIS_PORT,
    db=config.REDIS_DB_TOKENS,
    tokens_set_name=config.REDIS_TOKENS_SET_NAME,
)
