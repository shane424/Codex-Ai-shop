from contextlib import asynccontextmanager
from pathlib import Path
import secrets
import stripe
from fastapi import Depends, FastAPI, Header, HTTPException, Request
from fastapi.responses import FileResponse, HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from sqlalchemy import func
from sqlalchemy.orm import Session
from backend.config import get_settings
from backend.database import get_db, init_db
from backend.models import Metric, Product
from backend.services import authorize_download, fulfill_order, record_metric
from scripts.generate_initial_catalog import generate_catalog

settings = get_settings()
templates = Jinja2Templates(directory="templates")


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_db()
    generate_catalog()
    yield


app = FastAPI(title="Practical Kit Shop", lifespan=lifespan)


@app.get("/health")
def health():
    return {"status": "ok"}


@app.get("/", response_class=HTMLResponse)
def home(request: Request, db: Session = Depends(get_db)):
    products = db.query(Product).filter_by(status="approved").limit(8).all()
    return templates.TemplateResponse(request, "home.html", {"products": products})


@app.get("/products", response_class=HTMLResponse)
def products(request: Request, niche: str | None = None, db: Session = Depends(get_db)):
    query = db.query(Product).filter_by(status="approved")
    items = query.filter_by(niche=niche).all() if niche else query.all()
    niches = [row[0] for row in db.query(Product.niche).distinct().all()]
    return templates.TemplateResponse(request, "products.html", {"products": items, "niches": niches, "active_niche": niche})


@app.get("/product/{slug}", response_class=HTMLResponse)
def product_page(slug: str, request: Request, db: Session = Depends(get_db)):
    product = db.query(Product).filter_by(slug=slug, status="approved").first()
    if not product:
        raise HTTPException(404, "Product not found")
    record_metric(db, product.id, "views")
    related = db.query(Product).filter(Product.niche == product.niche, Product.id != product.id).limit(3).all()
    return templates.TemplateResponse(request, "product.html", {"product": product, "related": related, "mock": not bool(settings.stripe_secret_key)})


@app.post("/checkout/{slug}")
def checkout(slug: str, db: Session = Depends(get_db)):
    product = db.query(Product).filter_by(slug=slug, status="approved").first()
    if not product:
        raise HTTPException(404, "Product not found")
    record_metric(db, product.id, "checkout_starts")
    if not settings.stripe_secret_key:
        _, token = fulfill_order(db, f"mock_{secrets.token_hex(12)}", product)
        return RedirectResponse(f"/success?token={token}&mode=demo", status_code=303)
    stripe.api_key = settings.stripe_secret_key
    session = stripe.checkout.Session.create(
        mode="payment",
        line_items=[{"price_data": {"currency": "usd", "unit_amount": product.price_cents, "product_data": {"name": product.name}}, "quantity": 1}],
        metadata={"product_id": str(product.id)},
        success_url=f"{settings.base_url}/success?session_id={{CHECKOUT_SESSION_ID}}",
        cancel_url=f"{settings.base_url}/product/{product.slug}",
    )
    return RedirectResponse(session.url, status_code=303)


@app.post("/webhooks/stripe")
async def stripe_webhook(request: Request, stripe_signature: str = Header(default=""), db: Session = Depends(get_db)):
    if not settings.stripe_webhook_secret:
        raise HTTPException(503, "Stripe webhook is not configured")
    try:
        event = stripe.Webhook.construct_event(await request.body(), stripe_signature, settings.stripe_webhook_secret)
    except (ValueError, stripe.SignatureVerificationError) as exc:
        raise HTTPException(400, "Invalid webhook") from exc
    if event["type"] == "checkout.session.completed":
        session = event["data"]["object"]
        if session.get("payment_status") == "paid":
            product = db.get(Product, int(session["metadata"]["product_id"]))
            if product and session.get("amount_total") == product.price_cents:
                fulfill_order(db, session["id"], product, (session.get("customer_details") or {}).get("email", ""))
    return {"received": True}


@app.get("/success", response_class=HTMLResponse)
def success(request: Request, token: str = "", session_id: str = "", mode: str = "", db: Session = Depends(get_db)):
    if session_id and settings.stripe_secret_key:
        stripe.api_key = settings.stripe_secret_key
        session = stripe.checkout.Session.retrieve(session_id)
        if session.payment_status == "paid":
            product = db.get(Product, int(session.metadata.product_id))
            _, token = fulfill_order(db, session.id, product, (session.customer_details or {}).get("email", ""))
    return templates.TemplateResponse(request, "success.html", {"token": token, "demo": mode == "demo"})


@app.get("/download/{token}")
def download(token: str, db: Session = Depends(get_db)):
    product = authorize_download(db, token)
    if not product:
        raise HTTPException(403, "This download link is invalid, expired, or has reached its limit")
    path = Path(product.file_path).resolve()
    root = settings.product_storage_path.resolve()
    if root not in path.parents or not path.is_file():
        raise HTTPException(404, "File unavailable")
    return FileResponse(path, filename=path.name)


@app.get("/tools", response_class=HTMLResponse)
def tools_page(request: Request):
    return templates.TemplateResponse(request, "tools.html", {})


@app.get("/admin", response_class=HTMLResponse)
def admin(request: Request, token: str = "", authorization: str = Header(default=""), db: Session = Depends(get_db)):
    supplied = token or authorization.removeprefix("Bearer ")
    if not secrets.compare_digest(supplied, settings.admin_token):
        raise HTTPException(401, "Admin token required")
    totals = db.query(func.sum(Metric.revenue_cents), func.sum(Metric.sales), func.sum(Metric.views)).one()
    rows = db.query(Product.name, func.sum(Metric.views), func.sum(Metric.sales), func.sum(Metric.revenue_cents)).outerjoin(Metric).group_by(Product.id).order_by(func.sum(Metric.revenue_cents).desc()).all()
    return templates.TemplateResponse(request, "admin.html", {"totals": totals, "rows": rows})
