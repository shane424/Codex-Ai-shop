from datetime import date, datetime, timezone
from sqlalchemy import Date, DateTime, Float, ForeignKey, Integer, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column
from backend.database import Base


def utcnow() -> datetime:
    return datetime.now(timezone.utc)


class Opportunity(Base):
    __tablename__ = "opportunities"
    id: Mapped[int] = mapped_column(primary_key=True)
    niche: Mapped[str] = mapped_column(String(80))
    problem: Mapped[str] = mapped_column(String(240))
    product_type: Mapped[str] = mapped_column(String(20))
    estimated_demand: Mapped[float] = mapped_column(Float)
    competition_score: Mapped[float] = mapped_column(Float)
    creation_cost: Mapped[float] = mapped_column(Float)
    selling_price: Mapped[int] = mapped_column(Integer)
    overall_score: Mapped[float] = mapped_column(Float)
    status: Mapped[str] = mapped_column(String(20), default="new")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class Product(Base):
    __tablename__ = "products"
    id: Mapped[int] = mapped_column(primary_key=True)
    slug: Mapped[str] = mapped_column(String(160), unique=True, index=True)
    name: Mapped[str] = mapped_column(String(200))
    description: Mapped[str] = mapped_column(Text)
    niche: Mapped[str] = mapped_column(String(80), index=True)
    product_type: Mapped[str] = mapped_column(String(20))
    price_cents: Mapped[int] = mapped_column(Integer)
    file_path: Mapped[str] = mapped_column(String(500))
    keywords: Mapped[str] = mapped_column(Text, default="")
    status: Mapped[str] = mapped_column(String(20), default="approved")
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class Order(Base):
    __tablename__ = "orders"
    id: Mapped[int] = mapped_column(primary_key=True)
    stripe_session_id: Mapped[str] = mapped_column(String(255), unique=True)
    stripe_payment_intent: Mapped[str] = mapped_column(String(255), default="")
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    email: Mapped[str] = mapped_column(String(255), default="")
    amount_cents: Mapped[int] = mapped_column(Integer)
    status: Mapped[str] = mapped_column(String(30))
    created_at: Mapped[datetime] = mapped_column(DateTime(timezone=True), default=utcnow)


class DownloadToken(Base):
    __tablename__ = "download_tokens"
    id: Mapped[int] = mapped_column(primary_key=True)
    token_hash: Mapped[str] = mapped_column(String(64), unique=True, index=True)
    order_id: Mapped[int] = mapped_column(ForeignKey("orders.id"))
    expires_at: Mapped[datetime] = mapped_column(DateTime(timezone=True))
    downloads: Mapped[int] = mapped_column(Integer, default=0)
    max_downloads: Mapped[int] = mapped_column(Integer, default=5)


class Metric(Base):
    __tablename__ = "metrics"
    __table_args__ = (UniqueConstraint("product_id", "date"),)
    id: Mapped[int] = mapped_column(primary_key=True)
    product_id: Mapped[int] = mapped_column(ForeignKey("products.id"))
    date: Mapped[date] = mapped_column(Date, default=date.today)
    views: Mapped[int] = mapped_column(Integer, default=0)
    checkout_starts: Mapped[int] = mapped_column(Integer, default=0)
    sales: Mapped[int] = mapped_column(Integer, default=0)
    revenue_cents: Mapped[int] = mapped_column(Integer, default=0)
