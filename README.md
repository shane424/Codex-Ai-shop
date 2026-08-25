# Automated Digital Utility Shop

A FastAPI + Next.js storefront that discovers, scores, generates, validates, lists, sells, and securely delivers focused digital utility products. The project makes no income guarantee.

## Architecture

FastAPI owns authoritative catalog prices, Stripe sessions/webhooks, hashed download grants, analytics, and SQLAlchemy persistence. Generator and QA modules produce XLSX/PDF/ZIP artifacts, then publish only validated files. Next.js renders the public catalog, product structured data, five calculators, checkout UX, and a non-public-data admin shell. The provider interface keeps opportunity/review logic independent of any LLM vendor; absent credentials use deterministic mock behavior.

## Prerequisites

- Docker Engine with Compose v2 (recommended), or Python 3.12 and Node.js 20
- A Stripe test-mode account and Stripe CLI only when testing real payment fulfillment

## Environment setup

```bash
cp .env.example .env
```

Change `ADMIN_TOKEN`. Origins are a comma-separated allowlist. Never commit `.env`, database files, generated/private artifacts, customer records, Stripe secrets, or API keys. See `.env.example` for limits and optional settings.

## One-command local startup

```bash
docker compose up --build
```

Open <http://localhost:3000>; API docs are at <http://localhost:8000/docs>. Compose waits for backend health and persists development database/product data in named volumes. Without Stripe credentials, development checkout is visibly marked mock and cannot simulate paid fulfillment.

For host development:

```bash
python3.12 -m venv .venv && . .venv/bin/activate
pip install -r requirements.txt
python scripts/generate_initial_catalog.py
uvicorn backend.main:app --reload
# another terminal
cd frontend && npm install && npm run dev
```

## Stripe test setup

Use test-mode keys only. Set `STRIPE_SECRET_KEY`, `STRIPE_WEBHOOK_SECRET`, and public key, restart, then forward raw events:

```bash
stripe listen --forward-to localhost:8000/api/webhooks/stripe
```

Complete a Checkout session with Stripe's documented test card. The server uses database cents, stable product metadata, raw-body signature verification, payment status/amount checks, event uniqueness, and hashed expiring download tokens. Do not use live keys locally.

## Catalog and automation

```bash
python scripts/generate_initial_catalog.py  # idempotent 20 items + 5 bundles
python scripts/run_factory.py
```

Every XLSX/PDF is opened by deterministic QA. Bundles accept only approved-root files. The factory uses an exclusive lock and configured daily limits. Scheduler execution is opt-in (`ENABLE_SCHEDULER=false`); run one dedicated scheduler in a scaled deployment.

## Tests and builds

```bash
pytest
cd frontend && npm run typecheck && npm test && npm run build
```

## Deployment

Build the supplied production-stage containers, inject secrets through the platform, terminate TLS at a trusted proxy, restrict CORS, replace the default admin token, configure Stripe's HTTPS webhook, and provide durable object storage. Containers run unprivileged and expose health checks. SQLite and local product volumes are development/single-instance choices: **use PostgreSQL, migrations, and private S3-compatible object storage before running multiple instances**. Back up and retention-test both systems.

## Privacy and retention

Public endpoints never return order email addresses. The minimum fulfillment email/order metadata is retained until the operator's documented accounting/refund window expires, then should be deleted or anonymized under applicable law. Stripe remains an independent processor. Logs must exclude secrets, raw webhook bodies, tokens, customer emails, and filesystem paths. Protect `/admin` using an identity-aware proxy plus the server-side bearer secret; generated tools should not collect inputs.
