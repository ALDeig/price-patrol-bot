from datetime import datetime

from sqlalchemy import BigInteger, DateTime, ForeignKey, Index, Integer
from sqlalchemy.dialects.postgresql import JSONB
from sqlalchemy.orm import Mapped, mapped_column, relationship

from price_patrol_bot.src.services.db.base import Base
from price_patrol_bot.src.services.stores import Stores


class MUser(Base):
    __tablename__ = "users"

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=False)


class MProduct(Base):
    __tablename__ = "products"
    __table_args__ = (Index("idx-article-store", "article", "store"),)

    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    article: Mapped[str]
    store: Mapped[Stores] = mapped_column(Integer)
    name: Mapped[str]
    description: Mapped[str]
    min_price: Mapped[int]
    max_price: Mapped[int]
    prices: Mapped[dict] = mapped_column(JSONB)
    updated: Mapped[datetime] = mapped_column(
        DateTime, default=datetime.now, onupdate=datetime.now
    )

    # prices: Mapped[list["MPrice"]] = relationship(lazy="selectin")
    trackings: Mapped[list["MTracking"]] = relationship(back_populates="product")


# class MPrice(Base):
#     __tablename__ = "prices"
#
#     id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
#     product_id: Mapped[int] = mapped_column(
#         ForeignKey("products.id", ondelete="CASCADE")
#     )
#     data: Mapped[dict] = mapped_column(JSONB)


class MTracking(Base):
    __tablename__ = "trackings"
    id: Mapped[int] = mapped_column(BigInteger, primary_key=True, autoincrement=True)
    user_id: Mapped[int] = mapped_column(ForeignKey("users.id"))
    product_id: Mapped[int] = mapped_column(
        ForeignKey("products.id", ondelete="CASCADE"), index=True
    )

    product: Mapped[MProduct] = relationship(back_populates="trackings")
