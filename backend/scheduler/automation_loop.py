import os
from contextlib import contextmanager
from pathlib import Path
from sqlalchemy import func, select
from backend.agents.opportunity_agent import discover_opportunities, reserve_generation
from backend.config import get_settings
from backend.database import SessionLocal
from backend.models import Metric, Product

@contextmanager
def factory_lock(path=Path('data/factory.lock')):
    path.parent.mkdir(parents=True,exist_ok=True)
    try:
        fd=os.open(path,os.O_CREAT|os.O_EXCL|os.O_WRONLY); os.write(fd,str(os.getpid()).encode()); yield
    finally:
        if 'fd' in locals(): os.close(fd); path.unlink(missing_ok=True)
def action_for(views,sales):
    rate=sales/views if views else 0
    if (views>=500 and sales==0) or (views>=1000 and rate<.0025): return 'kill'
    if views>200 and sales==0: return 'improve'
    if views>=100 and rate>=.02: return 'scale'
    return 'observe'
def run_factory():
    with factory_lock():
        db=SessionLocal(); cfg=get_settings(); ideas=discover_opportunities('small business',cfg.max_new_products_per_day)
        winners=[x for x in ideas if x['overall_score']>=cfg.min_product_score]
        for idea in winners:
            try: reserve_generation(db,0,cfg)
            except RuntimeError: break
        products=db.scalars(select(Product)).all()
        for p in products:
            views,sales=db.execute(select(func.coalesce(func.sum(Metric.views),0),func.coalesce(func.sum(Metric.sales),0)).where(Metric.product_id==p.id)).one()
            action=action_for(views,sales)
            if action=='kill': p.status='archived'
        db.commit(); db.close(); return {'opportunities':len(winners)}
