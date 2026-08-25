from datetime import date, datetime, timezone
from sqlalchemy import Boolean, CheckConstraint, Date, DateTime, Float, ForeignKey, Index, Integer, JSON, String, Text, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship
from backend.database import Base

def utcnow(): return datetime.now(timezone.utc)

class Opportunity(Base):
    __tablename__='opportunities'
    id: Mapped[int]=mapped_column(primary_key=True)
    niche: Mapped[str]=mapped_column(String(100), index=True)
    problem: Mapped[str]=mapped_column(String(300))
    product_type: Mapped[str]=mapped_column(String(10))
    keywords: Mapped[list]=mapped_column(JSON, default=list)
    utility: Mapped[float]=mapped_column(Float); purchase_intent: Mapped[float]=mapped_column(Float)
    automation: Mapped[float]=mapped_column(Float); margin: Mapped[float]=mapped_column(Float)
    niche_specificity: Mapped[float]=mapped_column(Float); overall_score: Mapped[float]=mapped_column(Float)
    estimated_llm_cost_cents: Mapped[int]=mapped_column(Integer, default=0)
    status: Mapped[str]=mapped_column(String(30), default='discovered')
    regeneration_count: Mapped[int]=mapped_column(Integer, default=0)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=utcnow)
    __table_args__=(CheckConstraint('overall_score >= 0 AND overall_score <= 100'),)

class Product(Base):
    __tablename__='products'
    id: Mapped[int]=mapped_column(primary_key=True)
    slug: Mapped[str]=mapped_column(String(160), unique=True, index=True)
    name: Mapped[str]=mapped_column(String(200)); description: Mapped[str]=mapped_column(Text)
    niche: Mapped[str]=mapped_column(String(100), index=True); product_type: Mapped[str]=mapped_column(String(10))
    price_cents: Mapped[int]=mapped_column(Integer); file_path: Mapped[str]=mapped_column(Text)
    preview_path: Mapped[str|None]=mapped_column(Text, nullable=True); keywords: Mapped[list]=mapped_column(JSON, default=list)
    faqs: Mapped[list]=mapped_column(JSON, default=list); related_slugs: Mapped[list]=mapped_column(JSON, default=list)
    status: Mapped[str]=mapped_column(String(30), default='draft', index=True)
    failure_reasons: Mapped[list]=mapped_column(JSON, default=list)
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=utcnow)
    __table_args__=(CheckConstraint('price_cents >= 0'),)

class Order(Base):
    __tablename__='orders'
    id: Mapped[int]=mapped_column(primary_key=True)
    stripe_session_id: Mapped[str]=mapped_column(String(255), unique=True, index=True)
    stripe_payment_intent: Mapped[str|None]=mapped_column(String(255), unique=True, nullable=True)
    product_id: Mapped[int]=mapped_column(ForeignKey('products.id'))
    email: Mapped[str]=mapped_column(String(320)); amount_cents: Mapped[int]=mapped_column(Integer)
    currency: Mapped[str]=mapped_column(String(3), default='usd'); status: Mapped[str]=mapped_column(String(30))
    created_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=utcnow)
    product: Mapped[Product]=relationship()
    __table_args__=(CheckConstraint('amount_cents >= 0'),)

class WebhookEvent(Base):
    __tablename__='webhook_events'
    id: Mapped[int]=mapped_column(primary_key=True); stripe_event_id: Mapped[str]=mapped_column(String(255), unique=True, index=True)
    event_type: Mapped[str]=mapped_column(String(100)); processed_at: Mapped[datetime]=mapped_column(DateTime(timezone=True), default=utcnow)

class DownloadToken(Base):
    __tablename__='download_tokens'
    id: Mapped[int]=mapped_column(primary_key=True); token_hash: Mapped[str]=mapped_column(String(64), unique=True, index=True)
    order_id: Mapped[int]=mapped_column(ForeignKey('orders.id'), index=True); product_id: Mapped[int]=mapped_column(ForeignKey('products.id'))
    expires_at: Mapped[datetime]=mapped_column(DateTime(timezone=True)); max_downloads: Mapped[int]=mapped_column(Integer, default=3)
    download_count: Mapped[int]=mapped_column(Integer, default=0); revoked: Mapped[bool]=mapped_column(Boolean, default=False)

class Metric(Base):
    __tablename__='metrics'
    id: Mapped[int]=mapped_column(primary_key=True); product_id: Mapped[int]=mapped_column(ForeignKey('products.id'))
    date: Mapped[date]=mapped_column(Date, default=date.today); views: Mapped[int]=mapped_column(Integer, default=0)
    checkout_starts: Mapped[int]=mapped_column(Integer, default=0); sales: Mapped[int]=mapped_column(Integer, default=0)
    revenue_cents: Mapped[int]=mapped_column(Integer, default=0)
    __table_args__=(UniqueConstraint('product_id','date',name='uq_metric_product_date'),)

class DailyGeneration(Base):
    __tablename__='daily_generation'
    date: Mapped[date]=mapped_column(Date, primary_key=True); products_created: Mapped[int]=mapped_column(Integer, default=0)
    llm_cost_cents: Mapped[int]=mapped_column(Integer, default=0)
