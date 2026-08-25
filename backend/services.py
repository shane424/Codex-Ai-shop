import hashlib
import secrets
from datetime import date, datetime, timedelta, timezone
from sqlalchemy.orm import Session
from backend.config import get_settings
from backend.models import DownloadToken, Metric, Order, Product


def record_metric(db: Session, product_id: int, field: str, amount: int = 1) -> None:
    if field not in {"views", "checkout_starts", "sales", "revenue_cents"}:
        raise ValueError("Unknown metric")
    metric = db.query(Metric).filter_by(product_id=product_id, date=date.today()).first()
    if not metric:
        metric = Metric(product_id=product_id, date=date.today())
        db.add(metric)
    setattr(metric, field, getattr(metric, field) + amount)
    db.commit()


def fulfill_order(db: Session, session_id: str, product: Product, email: str = "") -> tuple[Order, str]:
    existing = db.query(Order).filter_by(stripe_session_id=session_id).first()
    if existing:
        return existing, ""
    order = Order(stripe_session_id=session_id, product_id=product.id, email=email, amount_cents=product.price_cents, status="paid")
    db.add(order)
    db.flush()
    raw_token = secrets.token_urlsafe(32)
    token = DownloadToken(token_hash=hashlib.sha256(raw_token.encode()).hexdigest(), order_id=order.id, expires_at=datetime.now(timezone.utc) + timedelta(hours=get_settings().download_token_ttl_hours))
    db.add(token)
    metric = db.query(Metric).filter_by(product_id=product.id, date=date.today()).first() or Metric(product_id=product.id, date=date.today())
    if metric.id is None:
        db.add(metric)
    metric.sales += 1
    metric.revenue_cents += product.price_cents
    db.commit()
    return order, raw_token


def authorize_download(db: Session, raw_token: str) -> Product | None:
    digest = hashlib.sha256(raw_token.encode()).hexdigest()
    token = db.query(DownloadToken).filter_by(token_hash=digest).first()
    now = datetime.now(timezone.utc)
    if not token:
        return None
    expiry = token.expires_at if token.expires_at.tzinfo else token.expires_at.replace(tzinfo=timezone.utc)
    if expiry <= now or token.downloads >= token.max_downloads:
        return None
    order = db.get(Order, token.order_id)
    if not order or order.status != "paid":
        return None
    token.downloads += 1
    db.commit()
    return db.get(Product, order.product_id)

