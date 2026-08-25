# TODO

## Before production launch
- [ ] Configure managed PostgreSQL and Alembic migration execution.
- [ ] Replace local artifact volumes with authenticated private object storage and signed delivery streaming.
- [ ] Put `/admin` behind organizational SSO and implement detailed top/worst/niche charts.
- [ ] Add transactional email delivery and customer support/contact policy.
- [ ] Run a real Stripe test-mode end-to-end purchase against the deployed HTTPS webhook.
- [ ] Add browser E2E tests and accessibility auditing in CI.
- [ ] Add a dedicated scheduler deployment and durable distributed lock.
- [ ] Establish jurisdiction-specific privacy, refund, tax, retention, and deletion policies with counsel.
- [ ] Keep external promotion publishing disabled until human/platform review is implemented.

## Definition-of-done evidence gaps
Locally implemented: runnable site/API, deployment containers, test/mock checkout and signed webhook processing, secure grants, idempotent 20+5 catalog generation, five calculators, generated pages, locked factory, deterministic QA, view analytics, protected aggregate admin API. Production credentials, hosted infrastructure, email delivery, and real payment evidence remain operator tasks and are not claimed complete.
