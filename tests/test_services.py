from datetime import date
from backend.automation import decide_product
from backend.models import Metric, Product
from backend.services import authorize_download, fulfill_order, record_metric


def make_product(db):
    product = Product(slug="test", name="Test", description="Useful", niche="Test", product_type="pdf", price_cents=900, file_path="test.pdf")
    db.add(product); db.commit()
    return product


def test_fulfillment_is_idempotent_and_token_authorizes(db):
    product = make_product(db)
    first, token = fulfill_order(db, "session_1", product, "buyer@example.com")
    second, duplicate_token = fulfill_order(db, "session_1", product)
    assert first.id == second.id
    assert duplicate_token == ""
    assert authorize_download(db, token).id == product.id
    metric = db.query(Metric).filter_by(product_id=product.id, date=date.today()).one()
    assert (metric.sales, metric.revenue_cents) == (1, 900)


def test_metrics(db):
    product = make_product(db)
    record_metric(db, product.id, "views")
    record_metric(db, product.id, "views", 2)
    assert db.query(Metric).one().views == 3


def test_scale_kill_decisions():
    assert decide_product(500, 0).action == "archive"
    assert decide_product(250, 0).action == "improve"
    assert decide_product(100, 2).action == "expand"
    assert decide_product(20, 0).action == "observe"

