from backend.automation import analyze_catalog
from backend.database import SessionLocal, init_db
from scripts.generate_initial_catalog import generate_catalog


if __name__ == "__main__":
    init_db()
    print(f"Generated {generate_catalog()} new catalog records")
    with SessionLocal() as db:
        print(f"Analysis: {analyze_catalog(db)}")

