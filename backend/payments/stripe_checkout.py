import secrets
import stripe
from backend.config import get_settings

def create_checkout(product):
    cfg=get_settings()
    if not cfg.stripe_secret_key:
        if cfg.environment!='development': raise RuntimeError('Stripe is not configured')
        return {'id':'mock_'+secrets.token_urlsafe(12),'url':f'{cfg.base_url}/success?mock=1&product={product.slug}','mock':True}
    stripe.api_key=cfg.stripe_secret_key
    session=stripe.checkout.Session.create(mode='payment',line_items=[{'price_data':{'currency':'usd','unit_amount':product.price_cents,'product_data':{'name':product.name}},'quantity':1}],success_url=f'{cfg.base_url}/success?session_id={{CHECKOUT_SESSION_ID}}',cancel_url=f'{cfg.base_url}/product/{product.slug}',metadata={'product_id':str(product.id),'product_slug':product.slug})
    return {'id':session.id,'url':session.url,'mock':False}
