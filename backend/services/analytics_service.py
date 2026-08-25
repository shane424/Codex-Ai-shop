from datetime import date
from sqlalchemy import select
from sqlalchemy.orm import Session
from backend.models import Metric

def record(db: Session, product_id: int, field: str, amount_cents=0):
    if field not in {'views','checkout_starts','sales'}: raise ValueError('invalid metric')
    metric=db.execute(select(Metric).where(Metric.product_id==product_id,Metric.date==date.today()).with_for_update()).scalar_one_or_none()
    if not metric: metric=Metric(product_id=product_id,date=date.today()); db.add(metric)
    setattr(metric,field,getattr(metric,field)+1)
    if field=='sales': metric.revenue_cents += amount_cents
    db.commit()
