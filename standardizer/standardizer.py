from dadata.sync import DadataClient
from logger.logger import log


class Standardizer:

    def __init__(self, token: str, language: int = 0, count: int = 10):
        self.count = count
        self._token = token
        self._lang = language
        self._client = DadataClient(token)

    def get_addresses(self, query: str):
        addresses = self._client.suggest(
            name="address",
            query=query,
            count=self.count,
            language="en" if self._lang else "ru"
        )
        log.log_info(f"{query}, {addresses}")
        return addresses

    def update_settings(self, token: str, language: int):
        self.token = token
        self._lang = language

    @property
    def token(self):
        return self._token

    @token.setter
    def token(self, value):
        self._token = value
        self._client = DadataClient(value)

