import stripe
from sqlalchemy.exc import IntegrityError
from sqlalchemy.orm import Session
from backend.config import get_settings
from backend.models import Order, Product, WebhookEvent
from backend.services.analytics_service import record
from backend.services.delivery_service import issue_token

def verify_event(payload: bytes, signature: str):
    secret=get_settings().stripe_webhook_secret
    if not secret: raise ValueError('webhook secret is not configured')
    return stripe.Webhook.construct_event(payload,signature,secret)
def process_event(db: Session,event):
    event_id=event['id']
    if db.query(WebhookEvent).filter_by(stripe_event_id=event_id).first(): return None
    db.add(WebhookEvent(stripe_event_id=event_id,event_type=event['type']))
    if event['type']!='checkout.session.completed': db.commit(); return None
    session=event['data']['object']; product=db.get(Product,int(session.get('metadata',{}).get('product_id',0)))
    if not product or session.get('payment_status')!='paid' or session.get('amount_total')!=product.price_cents: db.rollback(); raise ValueError('payment verification failed')
    order=Order(stripe_session_id=session['id'],stripe_payment_intent=session.get('payment_intent'),product_id=product.id,email=session.get('customer_details',{}).get('email','unknown@example.invalid'),amount_cents=product.price_cents,status='paid')
    db.add(order); db.commit(); token=issue_token(db,order.id,product.id); record(db,product.id,'sales',product.price_cents); return token
