from sqlalchemy import BigInteger, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from price_patrol_bot.src.services.db.base import Base


class MUser(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)


class MProduct(Base):
    __tablename__ = "products"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    article: Mapped[str]
    store_id: Mapped[int] = mapped_column(ForeignKey("stores.id", ondelete="CASCADE"))
    min_price: Mapped[int]
    price: Mapped[int]
    max_price: Mapped[int]
    name: Mapped[str]
    description: Mapped[str]
    trackings: Mapped[list["MTracking"]] = relationship(back_populates="product")


class MStore(Base):
    __tablename__ = "stores"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    name: Mapped[str]
    products: Mapped[list["MProduct"]] = relationship()


class MTracking(Base):
    __tablename__ = "trackings"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))

    product: Mapped[MProduct] = relationship(back_populates="trackings")
