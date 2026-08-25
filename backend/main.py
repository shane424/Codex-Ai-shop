from contextlib import asynccontextmanager
from pathlib import Path
from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse
from sqlalchemy import func, select
from sqlalchemy.orm import Session
from backend.config import get_settings
from backend.database import get_db, init_db
from backend.models import Metric, Order, Product
from backend.payments.stripe_checkout import create_checkout
from backend.payments.webhook import process_event, verify_event
from backend.services.analytics_service import record
from backend.services.delivery_service import redeem
from backend.generation.sanitize import within

@asynccontextmanager
async def lifespan(app): init_db(); yield
app=FastAPI(title='Utility Shop API',version='1.0.0',lifespan=lifespan)
cfg=get_settings(); app.add_middleware(CORSMiddleware,allow_origins=cfg.cors_origins,allow_credentials=False,allow_methods=['GET','POST'],allow_headers=['Content-Type','Stripe-Signature','Authorization'])
def product_json(p): return {'slug':p.slug,'name':p.name,'description':p.description,'niche':p.niche,'product_type':p.product_type,'price_cents':p.price_cents,'keywords':p.keywords,'faqs':p.faqs,'related_slugs':p.related_slugs}
@app.get('/health')
def health(): return {'status':'ok'}
@app.get('/api/products')
def catalog(niche:str|None=None,db:Session=Depends(get_db)):
    q=select(Product).where(Product.status=='published'); q=q.where(Product.niche==niche) if niche else q
    return [product_json(p) for p in db.scalars(q).all()]
@app.get('/api/products/{slug}')
def detail(slug:str,db:Session=Depends(get_db)):
    p=db.scalar(select(Product).where(Product.slug==slug,Product.status=='published'))
    if not p: raise HTTPException(404,'Product not found')
    record(db,p.id,'views'); return product_json(p)
@app.post('/api/products/{slug}/checkout')
def checkout(slug:str,db:Session=Depends(get_db)):
    p=db.scalar(select(Product).where(Product.slug==slug,Product.status=='published'))
    if not p: raise HTTPException(404,'Product not found')
    record(db,p.id,'checkout_starts')
    try: return create_checkout(p)
    except RuntimeError as exc: raise HTTPException(503,str(exc))
@app.post('/api/webhooks/stripe')
async def webhook(request:Request,stripe_signature:str=Header('',alias='Stripe-Signature'),db:Session=Depends(get_db)):
    try: event=verify_event(await request.body(),stripe_signature); token=process_event(db,event); return {'received':True,'download_token':token}
    except (ValueError,stripe.error.SignatureVerificationError): raise HTTPException(400,'Invalid webhook')
@app.get('/api/download/{token}')
def download(token:str,db:Session=Depends(get_db)):
    if len(token)>200: raise HTTPException(404,'Download unavailable')
    row=redeem(db,token)
    if not row: raise HTTPException(404,'Download unavailable')
    product=db.get(Product,row.product_id); path=Path(product.file_path); root=cfg.product_storage_path
    if not within(root,path) or not path.is_file(): raise HTTPException(404,'Download unavailable')
    return FileResponse(path,filename=path.name,media_type='application/octet-stream')
@app.get('/api/admin/summary')
def admin(authorization:str=Header(''),db:Session=Depends(get_db)):
    if authorization!=f'Bearer {cfg.admin_token}' or cfg.admin_token=='change-me': raise HTTPException(401,'Unauthorized')
    totals=db.execute(select(func.coalesce(func.sum(Metric.revenue_cents),0),func.coalesce(func.sum(Metric.sales),0),func.coalesce(func.sum(Metric.views),0))).one()
    return {'revenue_cents':totals[0],'sales':totals[1],'views':totals[2],'conversion_rate':totals[1]/totals[2] if totals[2] else 0}
