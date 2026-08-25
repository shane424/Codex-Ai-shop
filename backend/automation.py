from dataclasses import dataclass
from sqlalchemy import func
from sqlalchemy.orm import Session
from backend.models import Metric, Product


@dataclass(frozen=True)
class ProductDecision:
    action: str
    reason: str


def decide_product(views: int, sales: int) -> ProductDecision:
    conversion = sales / views if views else 0
    if views >= 500 and sales == 0:
        return ProductDecision("archive", "500 or more views without a sale")
    if views >= 1000 and conversion < .0025:
        return ProductDecision("archive", "conversion below 0.25% after 1,000 views")
    if views > 200 and sales == 0:
        return ProductDecision("improve", "listing has traffic but no sales")
    if views > 0 and conversion >= .02:
        return ProductDecision("expand", "conversion is at least 2%")
    return ProductDecision("observe", "not enough evidence")


def analyze_catalog(db: Session) -> dict[str, int]:
    counts = {key: 0 for key in ("archive", "improve", "expand", "observe")}
    products = db.query(Product).filter(Product.status.in_(["approved", "needs_improvement"])).all()
    for product in products:
        views, sales = db.query(func.coalesce(func.sum(Metric.views), 0), func.coalesce(func.sum(Metric.sales), 0)).filter(Metric.product_id == product.id).one()
        decision = decide_product(views, sales)
        counts[decision.action] += 1
        if decision.action == "archive":
            product.status = "archived"
        elif decision.action == "improve":
            product.status = "needs_improvement"
    db.commit()
    return counts

