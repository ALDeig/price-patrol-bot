from typing import Protocol

from pydantic import BaseModel, ConfigDict


class ProductData(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    article: str
    min_price: int
    max_price: int
    prices: dict[str, dict]
    name: str
    description: str | None


class Parser(Protocol):
    article: str

    async def get_product(self) -> ProductData:
        ...

    @staticmethod
    def _get_article(article_or_url: str) -> str:
        ...
