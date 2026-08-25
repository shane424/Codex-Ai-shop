# Automated Money Maker — `plan.md`

## Objective

Build and launch a **fully automated digital-product factory** that:

1. Finds small, commercially useful digital-product opportunities.
2. Generates original products automatically.
3. Creates product pages, previews, SEO copy, and promotional content.
4. Sells products through a self-hosted storefront using Stripe.
5. Delivers files automatically after payment.
6. Tracks sales and traffic.
7. Automatically produces more of what sells and stops producing what does not.

**Target:** MVP live by EOD today.

> Important: this is designed for high margins and low operating cost, not guaranteed profit. No legitimate system can guarantee a high rate of return.

---

# 1. Business Model

## Model

**Automated Digital Utility Shop**

Sell small downloadable products that solve boring, specific problems.

Examples:

- Excel / CSV templates
- Checklists
- Printable trackers
- calculators
- business forms
- inventory sheets
- pet-care logs
- gaming trackers
- tournament sheets
- content calendars
- job-search trackers
- budgeting tools
- maintenance logs
- contractor quote templates
- small-business SOP packs
- printable reference sheets
- prompt packs
- simple generators
- lightweight Python utilities

Do **not** build generic AI slop such as:

- generic journals
- random coloring books
- quote posters
- generic planners
- inspirational PDFs

The system should prefer products with clear utility.

---

# 2. Why This Model

## Advantages

- No inventory.
- No shipping.
- No customer-specific work.
- Files can be created automatically.
- Near-zero marginal cost.
- Stripe handles payment.
- The website handles delivery.
- Products can be bundled.
- Products can be generated continuously.
- Products can rank through long-tail search.
- High gross margins.
- Easy to test many niches.

## Revenue Structure

Primary products:

- `$5`
- `$9`
- `$12`
- `$19`
- `$29`

Bundles:

- `$39`
- `$49`
- `$79`

Goal is not one giant product.

Goal is:

```text
many small highly-specific products
        ↓
organic/search/social traffic
        ↓
low-friction purchase
        ↓
automatic delivery
        ↓
bundle upsells
```

---

# 3. Initial Product Niches

Start with areas where the product is easy to generate and usefulness is obvious.

## Tier 1

### Small Business Operations

Examples:

- contractor job-cost tracker
- equipment maintenance log
- invoice tracker
- mileage tracker
- estimate follow-up tracker
- employee onboarding checklist
- inventory reorder spreadsheet
- service call tracker
- quote comparison spreadsheet
- business expense categorizer

### Pet Businesses

Examples:

- dog daycare daily report
- pet sitter intake form
- dog medication tracker
- pet food inventory tracker
- grooming appointment tracker
- breeder litter tracker
- kennel cleaning checklist
- reptile feeding tracker
- reptile weight log
- pet enrichment calendar

### Gaming / Hobby

Examples:

- MMO loot tracker
- clan attendance tracker
- raid loot spreadsheet
- TCG collection tracker
- tournament bracket sheets
- RPG campaign tracker
- crafting profit calculator
- farming route tracker
- achievement tracker

### Job Search / Freelancing

Examples:

- job application tracker
- recruiter contact CRM
- interview question tracker
- freelance lead tracker
- proposal tracker
- client onboarding checklist
- project profitability calculator

---

# 4. MVP Product Type

For EOD launch, only support:

```text
CSV
XLSX
PDF
ZIP bundles
```

Do not build image-heavy products today.

The easiest automated products are spreadsheets and documents with obvious utility.

---

# 5. System Architecture

```text
                 ┌───────────────────┐
                 │ Opportunity Agent │
                 └─────────┬─────────┘
                           │
                           ▼
                 ┌───────────────────┐
                 │ Product Scorer    │
                 └─────────┬─────────┘
                           │
                           ▼
                 ┌───────────────────┐
                 │ Product Generator │
                 └─────────┬─────────┘
                           │
                           ▼
                 ┌───────────────────┐
                 │ QA / Validator    │
                 └─────────┬─────────┘
                           │
                           ▼
                 ┌───────────────────┐
                 │ Listing Generator │
                 └─────────┬─────────┘
                           │
                           ▼
┌──────────────┐ ┌───────────────────┐ ┌──────────────┐
│ Product File │ │     Storefront    │ │ Stripe       │
│ Storage      │◀┤                   ├▶│ Checkout      │
└──────────────┘ └─────────┬─────────┘ └──────────────┘
                           │
                           ▼
                 ┌───────────────────┐
                 │ Analytics Engine  │
                 └─────────┬─────────┘
                           │
                           ▼
                 ┌───────────────────┐
                 │ Scale / Kill Agent│
                 └───────────────────┘
```

---

# 6. Recommended Stack

## Backend

```text
Python 3.12
FastAPI
SQLAlchemy
SQLite initially
Postgres later
```

## Frontend

```text
Next.js
TypeScript
Tailwind
```

## Payments

```text
Stripe Checkout
Stripe Webhooks
```

## Storage

MVP:

```text
local /products directory
```

Production:

```text
Cloudflare R2
or
AWS S3
```

## Generation

Use an LLM provider through a clean abstraction.

```text
OpenAI API
```

Optional later:

```text
Claude
Gemini
local models
```

## Scheduling

MVP:

```text
APScheduler
```

Production:

```text
GitHub Actions cron
or
Celery
or
Cloudflare Cron
```

---

# 7. Repository Structure

```text
automated-money-maker/
│
├── README.md
├── plan.md
├── .env.example
├── docker-compose.yml
├── requirements.txt
│
├── backend/
│   ├── main.py
│   ├── config.py
│   ├── database.py
│   │
│   ├── models/
│   │   ├── product.py
│   │   ├── opportunity.py
│   │   ├── order.py
│   │   └── metric.py
│   │
│   ├── agents/
│   │   ├── opportunity_agent.py
│   │   ├── product_agent.py
│   │   ├── qa_agent.py
│   │   ├── listing_agent.py
│   │   └── optimization_agent.py
│   │
│   ├── generation/
│   │   ├── spreadsheet_generator.py
│   │   ├── pdf_generator.py
│   │   └── bundle_generator.py
│   │
│   ├── payments/
│   │   ├── stripe_checkout.py
│   │   └── webhook.py
│   │
│   ├── services/
│   │   ├── product_service.py
│   │   ├── delivery_service.py
│   │   ├── analytics_service.py
│   │   └── pricing_service.py
│   │
│   └── scheduler/
│       └── automation_loop.py
│
├── frontend/
│   ├── app/
│   ├── components/
│   └── lib/
│
├── products/
│   ├── generated/
│   ├── approved/
│   └── rejected/
│
├── data/
│   ├── opportunities.json
│   └── niches.json
│
├── scripts/
│   ├── generate_initial_catalog.py
│   ├── seed_database.py
│   └── run_factory.py
│
└── tests/
```

---

# 8. Database Models

## Opportunity

```text
id
niche
problem
product_type
keywords
estimated_demand
competition_score
creation_cost
selling_price
margin_score
automation_score
overall_score
status
created_at
```

## Product

```text
id
slug
name
description
niche
product_type
price
file_path
preview_path
keywords
status
created_at
sales
views
conversion_rate
revenue
```

## Order

```text
id
stripe_session_id
stripe_payment_intent
product_id
email
amount
status
created_at
```

## Metric

```text
id
product_id
date
views
checkout_starts
sales
revenue
```

---

# 9. Opportunity Agent

The opportunity agent produces product ideas.

For MVP it does **not** need a complicated scraping system.

Start with predefined niches and generate highly specific pain points.

Prompt concept:

```text
You are a digital-product market researcher.

Generate useful downloadable products for:

NICHE: {niche}

Products must:

- solve one narrow problem
- require no customer customization
- be deliverable as XLSX, CSV, PDF, or ZIP
- have obvious practical value
- be understandable from the product title
- avoid copyrighted brands
- avoid regulated advice
- avoid generic journals/planners
- be possible to create automatically

Return JSON only.
```

Generate:

```text
50 opportunities
```

---

# 10. Product Scoring

Every opportunity receives a score.

```python
score = (
    utility * 0.30
    + purchase_intent * 0.25
    + automation * 0.20
    + margin * 0.15
    + niche_specificity * 0.10
)
```

Score:

```text
0-100
```

Only produce products with:

```text
score >= 75
```

---

# 11. Product Generator

The product generator receives:

```text
problem
target customer
product type
required fields
instructions
```

It creates the actual product.

---

# 12. Spreadsheet Generator

Use:

```text
openpyxl
```

Automatically create:

- title
- instructions tab
- data-entry tab
- summary tab
- calculations
- formulas
- filters
- frozen headers
- readable widths
- validation where appropriate

Example:

```text
Contractor Job Profit Tracker.xlsx
```

Tabs:

```text
Instructions
Jobs
Expenses
Dashboard
```

Dashboard:

```text
Revenue
Material Cost
Labor Cost
Profit
Profit Margin
```

---

# 13. PDF Generator

Use:

```text
ReportLab
```

PDF products should be:

- printable
- clean
- functional
- low graphics
- black-and-white friendly

Examples:

```text
Vehicle Maintenance Checklist
Kennel Cleaning Checklist
Client Onboarding Checklist
```

---

# 14. Bundle Generator

Automatically group related products.

Example:

```text
Contractor Operations Bundle
```

Contains:

```text
Job Cost Tracker
Invoice Tracker
Mileage Tracker
Equipment Maintenance Log
Estimate Follow-Up Tracker
```

Individual total:

```text
$55
```

Bundle:

```text
$39
```

---

# 15. Automated QA Agent

Every generated product must be tested.

## XLSX Tests

Verify:

```text
file opens
required sheets exist
formulas exist
headers exist
no formula errors
reasonable dimensions
no empty required sections
```

## PDF Tests

Verify:

```text
file opens
page count > 0
text exists
no blank pages
```

## Content QA

LLM reviews:

```text
Does this solve the promised problem?
Is anything misleading?
Is it commercially useful?
Does it contain copyrighted content?
Does it provide unsafe regulated advice?
```

Products that fail:

```text
products/rejected/
```

Products that pass:

```text
products/approved/
```

---

# 16. Automatic Pricing

Initial pricing algorithm:

```text
single simple PDF             = $5
simple tracker                = $9
advanced spreadsheet          = $12
calculator/dashboard          = $19
small bundle                  = $29
large business bundle         = $39-$79
```

Optimization agent may later raise prices.

---

# 17. Storefront

Build a simple storefront.

Pages:

```text
/
 /products
 /product/[slug]
 /success
 /download/[token]
```

Homepage sections:

```text
Utility Downloads
Popular Products
Business Tools
Pet Business Tools
Gaming Tools
Job Search Tools
Bundles
```

---

# 18. Product Page

Each product page contains:

```text
Product Name

One sentence outcome

Who this is for

What it does

What's included

File format

Instant download

Preview images

Price

Buy button
```

Do not use exaggerated income claims.

---

# 19. Stripe Flow

```text
Customer
    ↓
Product page
    ↓
Stripe Checkout
    ↓
Payment
    ↓
Stripe webhook
    ↓
Order recorded
    ↓
Unique download token
    ↓
Download page
```

Download URLs expire.

Example:

```text
/download/f3c541...
```

---

# 20. Automatic Delivery

Webhook:

```text
checkout.session.completed
```

Actions:

```text
1. Verify payment.
2. Create order.
3. Generate secure download token.
4. Associate token with product.
5. Display download link.
```

Optional later:

```text
email download link
```

---

# 21. Initial Catalog

Codex should generate **20 products today**.

## Small Business

1. Contractor Job Profit Tracker
2. Small Business Expense Tracker
3. Equipment Maintenance Log
4. Customer Follow-Up CRM
5. Quote Comparison Spreadsheet
6. Invoice Payment Tracker
7. Inventory Reorder Calculator
8. Mileage Log
9. Vendor Comparison Sheet
10. Simple Project Profitability Calculator

## Pet

11. Pet Medication Tracker
12. Dog Daycare Daily Report
13. Kennel Cleaning Checklist
14. Pet Sitter Client Intake Pack
15. Reptile Feeding Tracker

## Job / Freelance

16. Job Application Tracker
17. Recruiter CRM
18. Freelance Lead Tracker
19. Client Profitability Calculator
20. Proposal Follow-Up Tracker

---

# 22. Bundle Catalog

Automatically create:

## Small Business Operations Pack

```text
$39
```

## Contractor Starter Pack

```text
$29
```

## Pet Business Operations Pack

```text
$29
```

## Job Search Command Center

```text
$19
```

## Freelancer Operations Pack

```text
$29
```

---

# 23. Automated Factory Loop

Run daily.

```python
def factory_loop():

    opportunities = discover_opportunities()

    ranked = score_opportunities(opportunities)

    winners = select_top(ranked, count=5)

    for opportunity in winners:

        product = generate_product(opportunity)

        if not qa_product(product):
            reject(product)
            continue

        listing = generate_listing(product)

        publish_product(product, listing)

    analyze_existing_products()

    optimize_prices()

    generate_bundles()

    archive_failures()
```

---

# 24. Scale / Kill Logic

Products should be evaluated automatically.

## Kill

Archive if:

```text
500 views
AND
0 sales
```

or:

```text
conversion rate < 0.25%
after 1,000 views
```

## Improve

Rewrite listing if:

```text
views > 200
AND
sales == 0
```

## Scale

If:

```text
conversion rate >= 2%
```

Then:

```text
create adjacent products
create bundle
create premium version
create related calculator
```

Example:

```text
Contractor Job Cost Tracker sells
```

Generate:

```text
Roofing Job Cost Tracker
HVAC Job Cost Tracker
Plumbing Job Cost Tracker
Electrical Job Cost Tracker
Landscaping Job Cost Tracker
```

---

# 25. SEO Automation

Each listing automatically generates:

```text
title
slug
meta title
meta description
H1
product description
FAQ
keywords
structured data
```

Target long-tail phrases.

Bad:

```text
Business Spreadsheet
```

Good:

```text
Contractor Job Cost and Profit Tracker Spreadsheet
```

---

# 26. Free Tool Funnel

This is the primary traffic strategy.

Codex should build free browser tools around the products.

Examples:

```text
Contractor Profit Margin Calculator
Freelance Hourly Rate Calculator
Pet Medication Schedule Generator
Inventory Reorder Calculator
Mileage Cost Calculator
Job Application Follow-Up Calculator
```

Each free tool links to a related paid template.

Example:

```text
Free Contractor Margin Calculator
               ↓
Want to track every job?
               ↓
Contractor Job Profit Tracker — $12
```

This gives the site actual search value instead of relying entirely on ads.

---

# 27. Programmatic SEO

Automatically create useful landing pages.

Example:

```text
/tools/contractor-profit-margin-calculator
/tools/hvac-profit-margin-calculator
/tools/plumbing-profit-margin-calculator
/tools/landscaping-profit-margin-calculator
```

Do **not** create doorway pages containing only rewritten AI text.

Every page must contain a functioning tool or useful downloadable resource.

---

# 28. Promotion Engine

MVP should generate promotional assets automatically.

For each product generate:

```text
3 Pinterest-style post concepts
3 short social posts
1 Reddit-style educational post draft
1 blog/tutorial
1 free-tool CTA
```

Do not automatically spam communities.

Store generated copy under:

```text
marketing/generated/
```

Automated external posting should only be enabled for platforms where API access and automation are permitted.

---

# 29. Analytics

Track:

```text
page views
product views
checkout clicks
sales
revenue
conversion rate
revenue per visitor
```

Dashboard:

```text
/admin
```

Show:

```text
Revenue Today
Revenue 7 Days
Revenue 30 Days
Top Products
Worst Products
Conversion Rate
Top Niches
```

---

# 30. Automation Rules

The system should require no routine human decisions.

Agents make decisions according to rules.

Humans only intervene for:

```text
API credentials
payment disputes
legal complaints
customer support exceptions
major infrastructure failure
```

---

# 31. Safety / Legal Guardrails

Never automatically generate:

```text
copyrighted game assets
trademarked logos
celebrity likeness merchandise
medical treatment guides
legal advice forms
tax advice
investment recommendations
gambling systems
fake certifications
forged documents
academic cheating products
```

Prefer generic utility products.

---

# 32. Cost Controls

Hard limits:

```text
MAX_NEW_PRODUCTS_PER_DAY=5
MAX_LLM_COST_PER_DAY=5
MAX_REGENERATIONS_PER_PRODUCT=2
MIN_PRODUCT_SCORE=75
```

If the daily budget is exceeded:

```text
stop generation
```

Sales continue normally.

---

# 33. EOD Build Order

## Phase 1 — Skeleton

Codex:

```text
[ ] Create repository
[ ] Create FastAPI backend
[ ] Create SQLite database
[ ] Create Next.js frontend
[ ] Add Docker Compose
[ ] Add environment configuration
```

---

## Phase 2 — Product Engine

```text
[ ] Create Opportunity model
[ ] Create Product model
[ ] Implement opportunity agent
[ ] Implement scoring
[ ] Implement spreadsheet generator
[ ] Implement PDF generator
[ ] Implement QA
```

---

## Phase 3 — Generate Catalog

```text
[ ] Generate 20 initial products
[ ] Validate files
[ ] Save approved products
[ ] Generate metadata
[ ] Generate bundles
```

---

## Phase 4 — Store

```text
[ ] Product catalog
[ ] Product pages
[ ] Stripe Checkout
[ ] Stripe webhook
[ ] Secure downloads
[ ] Success page
```

---

## Phase 5 — Free Tools

Build these first:

```text
[ ] Contractor Profit Calculator
[ ] Freelance Rate Calculator
[ ] Inventory Reorder Calculator
[ ] Mileage Cost Calculator
[ ] Job Follow-Up Calculator
```

Each tool must upsell a relevant product.

---

## Phase 6 — Automation

```text
[ ] Daily scheduler
[ ] Generate opportunities
[ ] Score opportunities
[ ] Generate products
[ ] QA products
[ ] Publish approved products
[ ] Analyze metrics
[ ] Kill poor performers
[ ] Expand winners
```

---

# 34. Definition of Done Today

The MVP is complete when:

```text
[ ] Website runs locally
[ ] Website can deploy
[ ] Stripe test checkout works
[ ] Stripe webhook works
[ ] Product purchases create download links
[ ] At least 20 products exist
[ ] At least 5 bundles exist
[ ] At least 5 free calculators exist
[ ] Product pages are generated automatically
[ ] Daily factory task works
[ ] QA rejects broken products
[ ] Analytics records product views
[ ] Admin page shows metrics
```

---

# 35. Codex Master Prompt

Give Codex this prompt after adding this `plan.md` to the repository:

```text
You are the autonomous lead engineer for this repository.

Read plan.md completely before making changes.

OBJECTIVE:

Build the Automated Digital Utility Shop described in plan.md and reach the
"Definition of Done Today."

RULES:

1. Work autonomously.
2. Do not ask me architecture questions unless blocked by credentials.
3. Choose the simplest production-capable implementation.
4. Complete one milestone at a time.
5. Run tests after every milestone.
6. Fix failing tests before continuing.
7. Keep README.md updated.
8. Maintain TODO.md containing incomplete work.
9. Maintain CHANGELOG.md containing completed work.
10. Never commit credentials.
11. Use mocked Stripe configuration when credentials are absent.
12. Generate real usable example products, not placeholder files.
13. Every generated spreadsheet must be opened and validated programmatically.
14. Every generated PDF must be validated programmatically.
15. Do not add unnecessary microservices.
16. Prefer deterministic code over an LLM when deterministic code can perform
    the task.
17. Keep LLM usage behind an interface so providers can be changed.
18. The application must run with one command:

    docker compose up --build

19. Add automated tests for:
    - product creation
    - spreadsheet generation
    - PDF generation
    - QA validation
    - checkout creation
    - webhook processing
    - download authorization
    - opportunity scoring

20. Continue until all locally achievable Definition-of-Done items in plan.md
    are complete.

START WITH:

A. repository structure
B. database models
C. spreadsheet/PDF generators
D. initial product generation
E. storefront
F. Stripe
G. analytics
H. automation loop
I. free calculators

Do not stop after scaffolding.

Implement the working system.
```

---

# 36. `.env.example`

```env
OPENAI_API_KEY=

STRIPE_SECRET_KEY=
STRIPE_WEBHOOK_SECRET=
NEXT_PUBLIC_STRIPE_PUBLISHABLE_KEY=

DATABASE_URL=sqlite:///./money_maker.db

PRODUCT_STORAGE_PATH=./products/approved

MAX_NEW_PRODUCTS_PER_DAY=5
MAX_LLM_COST_PER_DAY=5
MIN_PRODUCT_SCORE=75

BASE_URL=http://localhost:3000
```

---

# 37. First Revenue Goal

Do not optimize for:

```text
$10,000/month
```

initially.

Optimize for proof:

```text
First visitor
↓
First checkout click
↓
First $5-$20 sale
↓
First product with 2+ sales
↓
Create 5 related products
↓
Bundle
↓
Repeat
```

The automation engine should treat an actual sale as the strongest market signal.

---

# 38. North-Star Metric

```text
Revenue per 1,000 Visitors
```

Secondary:

```text
Conversion Rate
Average Order Value
Revenue per Product
Revenue per Niche
```

The system's job is to continuously increase these values.

---

# 39. Later Expansion

Only after sales exist:

```text
Etsy listings
Gumroad
Payhip
Pinterest automation
email capture
affiliate products
subscription template library
business-license versions
white-label packs
API products
micro-SaaS tools
```

Do not build these today.

---

# 40. Final Strategy

The system is:

```text
Discover
   ↓
Score
   ↓
Create
   ↓
Validate
   ↓
Publish
   ↓
Sell
   ↓
Measure
   ↓
Kill losers
   ↓
Clone winners into adjacent niches
   ↓
Bundle winners
   ↓
Repeat
```

The important part is not AI-generated products.

The important part is the **feedback loop**.

The factory should automatically spend more effort on categories where customers actually purchase and progressively stop producing categories that do not sell.
