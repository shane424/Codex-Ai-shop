# Practical Kit Shop

A self-hosted MVP for selling focused digital utility products: spreadsheets, printable checklists, calculators, and bundles for small businesses, pet businesses, job seekers, and freelancers.

The store intentionally starts as a standalone site rather than Etsy or Shopify. This keeps the catalog factory, secure delivery, analytics, and automation under one roof with no platform subscription. Marketplace expansion should happen only after a product shows demand.

## Included

- 20 usable products and five ZIP bundles generated deterministically.
- XLSX files with instructions, filters, formulas, and summaries; printable PDFs; automated QA.
- Responsive storefront, catalog filtering, product pages, and five free calculators.
- Stripe Checkout and signed webhook support, plus an obvious local demo mode when Stripe is absent.
- Idempotent fulfillment with expiring, hashed, download-limited tokens.
- First-party cookieless aggregate analytics and a token-protected admin report.
- Performance rules for improving, archiving, or expanding products.

## Start with Docker

```bash
cp .env.example .env
# Change ADMIN_TOKEN before exposing the app.
docker compose up --build
```

Open <http://localhost:8000>. Persistent Docker volumes retain the database and approved products.

## Start for development

Requires Python 3.12.

```bash
python -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
cp .env.example .env
python scripts/generate_initial_catalog.py
uvicorn backend.main:app --reload
```

Run the factory manually with `python scripts/run_factory.py`. Generation is idempotent: existing catalog records and files are reused.

## Payments

Without `STRIPE_SECRET_KEY`, checkout is explicitly marked as demo mode and creates a simulated paid order so the complete download journey can be tested locally. It must not be treated as a real payment system.

Before launch:

1. Create a Stripe account and copy test-mode credentials into `.env`.
2. Set `STRIPE_SECRET_KEY` and `STRIPE_WEBHOOK_SECRET`.
3. Forward Stripe events to `POST /webhooks/stripe` and subscribe to `checkout.session.completed`.
4. Set `BASE_URL` to the HTTPS public origin.
5. Test successful, cancelled, altered-amount, invalid-signature, and repeated webhook scenarios.
6. Switch to live credentials only after the business identity and customer policies are published.

The backend builds line items from database prices. Fulfillment verifies payment status and amount, and repeated session IDs do not create duplicate orders.

## Admin

Set a long random `ADMIN_TOKEN`, then visit `/admin?token=YOUR_TOKEN`. The query-string form is convenient for the MVP but can appear in browser history; the endpoint also accepts `Authorization: Bearer YOUR_TOKEN`, which is preferred for tooling. “Admin identity” means the shop owner—not necessarily a Gmail account. A hosted identity provider is unnecessary for this single-owner MVP.

## Data and privacy

Analytics are first-party and cookieless: the application records aggregate product views, checkout starts, sales, and revenue. It does not fingerprint visitors. Paid orders may contain the email returned by Stripe for fulfillment/support. Establish a retention policy and customer-facing privacy notice before launch.

SQLite and local product storage are the lowest-cost single-VPS setup. Back up both `data/` and `products/approved/`. Do not horizontally scale this configuration; migrate to PostgreSQL and object storage first.

## Product generation

The launch catalog is deterministic and does not need an OpenAI or Claude key. This makes output repeatable and eliminates generation spend. `OPENAI_API_KEY` and `LLM_PROVIDER` are reserved for a future provider adapter; do not add keys until a specific LLM-assisted feature passes a review gate.

Safety constraints exclude professional advice, copyrighted assets, credential-like documents, and exaggerated income claims. Generated artifacts must pass structural QA before publication.

## Testing

```bash
pytest -q
python scripts/generate_initial_catalog.py
python scripts/run_factory.py
```

## Deployment checklist

- Choose a final name and domain; point DNS to an inexpensive Docker-capable VPS.
- Put the container behind an HTTPS reverse proxy such as Caddy.
- Change the admin secret and configure Stripe.
- Add a real support address, seller identity, privacy policy, terms, and reviewed digital-download refund policy.
- Configure daily encrypted backups and test restoration.
- Keep demo checkout disabled in public production by supplying Stripe credentials.

See [`TODO.md`](TODO.md) for owner-dependent launch work and [`plan(9).md`](plan(9).md) for the original product brief.
