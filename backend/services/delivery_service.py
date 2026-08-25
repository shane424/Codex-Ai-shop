import hashlib, secrets
from datetime import datetime, timedelta, timezone
from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.config import get_settings
from backend.models import DownloadToken

def issue_token(db: Session, order_id: int, product_id: int):
    raw=secrets.token_urlsafe(32); cfg=get_settings()
    row=DownloadToken(token_hash=hashlib.sha256(raw.encode()).hexdigest(),order_id=order_id,product_id=product_id,expires_at=datetime.now(timezone.utc)+timedelta(minutes=cfg.download_ttl_minutes),max_downloads=cfg.download_limit)
    db.add(row); db.commit(); return raw

def redeem(db: Session, raw: str):
    digest=hashlib.sha256(raw.encode()).hexdigest(); row=db.execute(select(DownloadToken).where(DownloadToken.token_hash==digest).with_for_update()).scalar_one_or_none()
    now=datetime.now(timezone.utc)
    if not row or row.revoked or row.download_count>=row.max_downloads or row.expires_at.replace(tzinfo=row.expires_at.tzinfo or timezone.utc)<=now: return None
    row.download_count += 1; db.commit(); return row
