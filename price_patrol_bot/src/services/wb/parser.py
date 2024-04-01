import logging
import re
from typing import Literal

from httpx import AsyncClient, ConnectError
from pydantic import BaseModel, Field, ValidationError, field_validator

from price_patrol_bot.src.services.parsers.base_parser import ProductData
from price_patrol_bot.src.services.parsers.exceptions import (
    CantGetProduct,
    NotValidateUrl,
)

logger = logging.getLogger(__name__)


class WBProductData(ProductData):
    prices: dict[str, dict[Literal["price", "in_stock"], int]]


class WBProductSchema(BaseModel):
    article: int = Field(alias="id")
    brand: str
    name: str
    sale_price: int = Field(alias="salePriceU")
    basic_price: int = Field(alias="priceU")
    in_stock: bool = Field(default=None, alias="wh")

    @field_validator("sale_price", "basic_price")
    @classmethod
    def get_price(cls, v: int) -> int:
        return int(v / 100)

    @field_validator("in_stock", mode="before")
    @classmethod
    def check_in_stock(cls, v):
        if v is None:
            return False
        return True


class WBParser:
    def __init__(self, article_or_url: str) -> None:
        self.article = self._get_article(article_or_url)

    async def get_product(self) -> WBProductData:
        params = self._get_params()
        async with AsyncClient() as client:
            try:
                response = await client.get(
                    url="https://card.wb.ru/cards/v1/detail", params=params, timeout=20
                )
            except ConnectError:
                logger.error(f"ConnectError - {self.article}")
                raise CantGetProduct
        try:
            product = WBProductSchema.model_validate(
                response.json()["data"]["products"][0]
            )
        except (IndexError, KeyError, ValidationError):
            raise CantGetProduct
        return WBProductData(
            article=str(product.article),
            min_price=product.sale_price,
            max_price=product.sale_price,
            prices={"default": {"price": product.sale_price, "in_stock": product.in_stock}},
            name=product.name,
            description=None,
        )

    def get_photo_url(self) -> str:
        """Формирует url для загрузки фото товара"""
        base_url_with_parts = self._get_base_url_with_parts()
        url = f"{base_url_with_parts}/images/big/1.jpg"
        return url

    def _get_base_url_with_parts(self) -> str:
        url = (
            f"https://{self._get_basket_url(int(self.article[:-5]))}.wb.ru/"
            f"vol{self.article[:-5]}/"
            f"part{self.article[:-3]}/"
            f"{self.article}"
        )
        return url

    @staticmethod
    def _get_basket_url(val: int) -> str:
        """Возвращает версию basket для загрузки фотографии"""
        baskets = {
            (0, 144): "01",
            (144, 288): "02",
            (288, 432): "03",
            (432, 720): "04",
            (720, 1008): "05",
            (1008, 1062): "06",
            (1062, 1116): "07",
            (1116, 1170): "08",
            (1170, 1314): "09",
            (1314, 1602): "10",
            (1602, 1656): "11",
            (1656, 1920): "12",
            (1920, 2046): "13",
            (2046, 2189): "14",
        }
        for range_, basket in baskets.items():
            if val in range(*range_):
                return f"basket-{basket}"
        return "basket-15"

    def _get_params(self) -> dict:
        """Возвращает параметры для сбора информации по артикулу"""
        params = {
            "appType": 1,
            "curr": "rub",
            "dest": "-1257786",
            "spp": 30,
            "nm": self.article,
        }
        return params

    @staticmethod
    def _get_article(article_or_url) -> str:
        """Если передат url, то достает из него артикул, если передат ариткул,
        то возвращяет его"""
        if article_or_url.isdigit():
            return article_or_url
        clear_url = article_or_url.split("?")[0]
        digits = re.search(r"\d+", clear_url)
        if digits is None:
            raise NotValidateUrl
        return digits.group()
