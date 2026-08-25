from pathlib import Path
from backend.config import get_settings
from backend.database import SessionLocal, init_db
from backend.factory import BUNDLES, CATALOG, ProductSpec, generate_artifact, generate_bundle
from backend.models import Product


def generate_catalog() -> int:
    settings = get_settings()
    init_db()
    created = 0
    with SessionLocal() as db:
        for spec in CATALOG:
            path = generate_artifact(spec, settings.product_storage_path)
            if not db.query(Product).filter_by(slug=spec.slug).first():
                db.add(Product(slug=spec.slug, name=spec.name, description=f"A practical {spec.name.lower()} designed for clear, repeatable record keeping. Includes instructions and ready-to-use fields.", niche=spec.niche, product_type=spec.kind, price_cents=spec.price_cents, file_path=str(path), keywords=f"{spec.niche}, tracker, template"))
                created += 1
        db.flush()
        for name, price, indexes in BUNDLES:
            path = generate_bundle(name, indexes, settings.product_storage_path)
            spec = ProductSpec(name, "Bundles", "zip", price)
            if not db.query(Product).filter_by(slug=spec.slug).first():
                db.add(Product(slug=spec.slug, name=name, description="A discounted collection of related, ready-to-use utility templates.", niche="Bundles", product_type="zip", price_cents=price, file_path=str(path), keywords="bundle, templates"))
                created += 1
        db.commit()
    return created


if __name__ == "__main__":
    print(f"Created {generate_catalog()} catalog records")
