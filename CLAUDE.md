# CLAUDE.md — Mining Stock Report

This file is read by Claude Code at the start of every session.
Update it as the project evolves.

---

## What this project is

**MiningStockReport.com** — a junior mining stock analysis platform built around a YouTube channel brand.

The site serves two distinct audiences:
1. **Retail investors** (free + paid newsletter) — the "Self-Directed Digger": 35–58, Canada/AU/UK, $25K–$150K in speculative mining, burned by newsletter pumps before
2. **Accredited investors** — deal flow, private placements, management introductions

The core IP is the **Verdict Framework** — a 5-factor scoring system that outputs BUY / WATCH / AVOID on any junior mining company.

---

## Tech stack

| Layer | Technology |
|---|---|
| Framework | Django 5.0.6 |
| Database | PostgreSQL (via `DATABASE_URL` env var) |
| Auth | Custom `User` model (`apps.accounts`) with membership tiers |
| API | Django REST Framework + JWT (for future mobile app) |
| Static files | WhiteNoise (served by Django in prod, Nginx handles directly) |
| Process manager | Supervisor + Gunicorn |
| Web server | Nginx (reverse proxy) |
| SSL | Let's Encrypt via Certbot |
| Server | DigitalOcean Droplet — Ubuntu 24.04 LTS |
| DNS | ns1.tsunami.ca / ns2.tsunami.ca |
| Email | SendGrid (SMTP) |
| Error tracking | Sentry (DSN in `.env`) |

---

## Project layout

```
miningstock/
├── apps/
│   ├── accounts/     # Custom User — FREE/FOUNDING/STANDARD/DISCORD tiers
│   ├── blog/         # Posts — 4 content pillars, premium gating, FAQ/key_takeaways
│   ├── core/         # Home, about, robots.txt, llms.txt, sitemap, context processor
│   ├── investors/    # Accredited investor registration + CRM admin
│   ├── leads/        # Retail email capture + lead magnet delivery
│   ├── verdict/      # Company scorecards — 5-factor Verdict Framework
│   ├── videos/       # YouTube video archive
│   └── watchlist/    # Stock watchlist — thesis, price, catalyst tracking
├── config/
│   ├── settings/
│   │   ├── base.py         # Shared settings
│   │   ├── development.py  # Local dev (SQLite, console email, debug toolbar)
│   │   └── production.py   # Production (PostgreSQL, SMTP, Sentry, HSTS)
│   ├── urls.py       # Main URL routing
│   ├── api_urls.py   # DRF API v1 endpoints
│   └── wsgi.py
├── static/
│   ├── css/main.css  # Dark gold theme — #0d0d0d bg, #ffc107 accent
│   ├── js/main.js    # AJAX subscribe, nav highlight, alert auto-dismiss
│   └── img/          # og-default.svg (replace with 1200×630px PNG before launch)
├── templates/        # All HTML templates
├── requirements/
│   ├── base.txt
│   ├── development.txt
│   └── production.txt
├── .env              # Never commit — copy from .env.example
├── .env.example      # Template for all env vars
├── manage.py
├── Procfile
├── DEPLOYMENT.md     # Full step-by-step deploy guide
└── README.md         # Project overview, API docs, SEO/GEO notes
```

---

## Environment setup (local dev)

```bash
python3 -m venv venv && source venv/bin/activate
pip install -r requirements/development.txt
cp .env.example .env        # Fill in SECRET_KEY at minimum
python manage.py migrate
python manage.py createsuperuser
python manage.py runserver
```

Settings module for development:
```
DJANGO_SETTINGS_MODULE=config.settings.development
```

This is the default in `manage.py`. No need to set it manually for local work.

---

## Environment setup (production — DigitalOcean)

```bash
source venv/bin/activate
pip install -r requirements/production.txt
python manage.py migrate --settings=config.settings.production
python manage.py collectstatic --noinput --settings=config.settings.production
```

Deploy user: `deploy`
App directory: `/home/deploy/miningstock/`
Virtualenv: `/home/deploy/miningstock/venv/`
Gunicorn socket: `/run/miningstock.sock`
Logs: `/var/log/miningstock/`
Deploy script: `/home/deploy/deploy.sh` (git pull → migrate → collectstatic → restart)

---

## Running tests

```bash
# No test suite yet — this is the first thing to build (see Next Steps)
pytest
```

---

## Key models

### `apps.accounts.User`
Custom user extending `AbstractUser`. Email is the username field.
```python
class MembershipTier(TextChoices):
    FREE      = "free"
    FOUNDING  = "founding"   # $19/mo — locked in for founding members
    STANDARD  = "standard"   # $35/mo — post-launch price
    DISCORD   = "discord"    # $49/mo — community tier
```
`user.is_premium` → `True` for any paid tier with a valid `membership_expires`.

### `apps.blog.Post`
- `pillar` — one of: `due-diligence`, `company-verdicts`, `market-intelligence`, `accountability`
- `key_takeaways` — JSONField list of strings, rendered at top of post + Article schema
- `faq_items` — JSONField list of `{question, answer}` dicts, rendered as FAQ accordion + FAQPage JSON-LD
- `is_premium` — gates full body behind `user.is_premium` check
- `word_count` — auto-calculated on save (strips HTML tags)
- `reading_time` — computed property (word_count / 200)
- Inherits `SEOMixin` from `apps.core.seo` — adds `meta_title`, `meta_description`, `og_image`, `og_image_alt`

### `apps.verdict.Company` + `apps.verdict.VerdictScorecard`
The core IP. `VerdictScorecard` has 5 integer fields (1–5 each):
- `management_score` — insider ownership and alignment
- `geology_score` — resource classification and grade
- `capital_score` — share structure and warrant overhang
- `catalyst_score` — proximity of next material news event
- `acquisition_score` — P/NAV vs comparable transactions
`composite_score` is a property (sum of all 5). `verdict` is BUY / WATCH / AVOID (set manually).
`p_nav_multiple` auto-calculates from `current_price / nav_per_share` on save.
Both inherit `SEOMixin`.

### `apps.investors.AccreditedInvestor`
CRM-ready model for accredited investor registrations.
- `confirmed_accredited` + `consent_contact` — stored with `consent_timestamp` + `consent_ip` for compliance
- `status` — Pending → Approved → Contacted → Declined → Inactive
- `assigned_to`, `last_contacted`, `internal_notes` — manual CRM fields until integration is built
Admin has bulk actions: Mark Approved, Mark Contacted, Mark Declined.

### `apps.watchlist.WatchlistItem`
- `status` — Watching / In Position / Sold / Dropped
- `thesis`, `entry_price`, `target_price`, `stop_loss` — public accountability fields
- `next_catalyst`, `catalyst_date` — displayed on watchlist page
- `public_notes` vs `private_notes` — only public_notes renders on site

### `apps.leads.Subscriber`
- `source` — tracks which page/magnet drove the signup
- `lead_magnet` — FK to `LeadMagnet` model for file delivery
- `mailchimp_synced` — flag for sync management command (not yet built)

---

## URL structure

| URL prefix | App | Notes |
|---|---|---|
| `/` | core | Homepage |
| `/analysis/` | blog | Stronger SEO signal than `/blog/` — do not change |
| `/companies/` | verdict | Entity-match for search — do not change |
| `/watchlist/` | watchlist | |
| `/videos/` | videos | |
| `/investors/` | investors | `noindex` — accredited investor registration |
| `/subscribe/` | leads | Email capture + lead magnet download |
| `/accounts/` | accounts | Login, logout, password change |
| `/admin/` | Django admin | Staff only |
| `/api/v1/` | DRF | JWT auth, all content endpoints |
| `/sitemap.xml` | core | Django sitemaps framework |
| `/robots.txt` | core | Dynamic view — blocks /admin/, /api/ |
| `/llms.txt` | core | AI crawler guidance (Perplexity, ChatGPT, etc.) |

---

## API endpoints

Base: `/api/v1/`

| Method | Endpoint | Description |
|---|---|---|
| POST | `auth/token/` | Obtain JWT (email + password) |
| POST | `auth/token/refresh/` | Refresh JWT |
| GET | `posts/` | Blog posts — filter: `?pillar=due-diligence` |
| GET | `posts/<id>/` | Post detail — body gated for premium |
| GET | `videos/` | Video archive — filter: `?featured=1` |
| GET | `companies/` | Companies with latest verdict |
| GET | `verdicts/` | Scorecards — filter: `?verdict=BUY&company=slv-v` |
| GET | `watchlist/` | Active watchlist items |
| POST | `subscribe/` | Email capture |
| POST | `investors/` | Accredited investor registration |

All read endpoints are public (`AllowAny`). Write endpoints require JWT.

---

## SEO / GEO implementation

Every content model inherits `SEOMixin` (`apps/core/seo.py`):
- `meta_title` (max 70 chars) — falls back to model title
- `meta_description` (max 160 chars) — falls back to excerpt
- `og_image` (1200×630px) — falls back to `static/img/og-default.svg`

`base.html` outputs:
- Full Open Graph + Twitter Card meta tags
- JSON-LD `Organization` schema (site-wide)

Per-page schema blocks:
- `Article` + optional `FAQPage` — `templates/blog/post_detail.html`
- `Review` (verdict scorecard) — `templates/verdict/scorecard_detail.html`
- `BreadcrumbList` — post detail + scorecard detail

Dynamic views:
- `/robots.txt` — blocks /admin/, /api/, references sitemap
- `/llms.txt` — structured description for AI crawlers

**Do not change `/analysis/` or `/companies/` URL prefixes** — they are set before first indexing for a reason.

---

## Content pillars

| Pillar | Slug | Purpose |
|---|---|---|
| Due Diligence | `due-diligence` | How to evaluate juniors: reading technical reports, NI 43-101, geology |
| Company Verdicts | `company-verdicts` | Deep dives with scored verdicts |
| Market Intelligence | `market-intelligence` | Macro, catalyst calendar, M&A analysis |
| Accountability | `accountability` | Portfolio tracking, position updates, loss post-mortems |

---

## Brand guidelines

- **Primary colour:** `#ffc107` (gold) — buttons, accents, verdict badges
- **Background:** `#0d0d0d` (near-black)
- **Card background:** `#141414`
- **Border:** `#2a2a2a`
- **Secondary text:** `#888888`
- **Accredited investor accent:** `#e2c97e` (distinct from retail gold)
- **Verdict colours:** BUY `#4ade80` (green), WATCH `#ffc107` (gold), AVOID `#f87171` (red)
- **Font:** System UI stack — `system-ui, -apple-system, sans-serif`
- **Tone:** Precise, direct, no hype, show your work. Never "smash the bell."
- **Tagline:** "The research desk for retail investors who want to find junior miners before the newsletter crowd does."

---

## What's NOT built yet (prioritised backlog)

### High priority — build before content launch
1. **Price sync management command** — `python manage.py sync_prices`
   - Fetch current price + % change into `watchlist.PriceCache`
   - Use Yahoo Finance (`yfinance` library) or Alpha Vantage free tier
   - Run via cron: `*/30 * * * * /home/deploy/deploy.sh sync_prices`

2. **Mailchimp sync command** — `python manage.py sync_mailchimp`
   - Push new `leads.Subscriber` records to Mailchimp list
   - Flag `mailchimp_synced=True` after successful push
   - Check `MAILCHIMP_API_KEY` and `MAILCHIMP_LIST_ID` in `.env`

3. **Test suite** — `pytest-django` + `factory-boy`
   - Model factories are in `requirements/development.txt` already
   - Priority: Verdict Framework composite score logic, premium gating, form honeypots

### Medium priority — before newsletter launch (Day 91)
4. **Stripe webhook handler** — membership upgrades
   - Set `user.membership_tier` and `user.membership_expires` from Stripe events
   - Endpoints: `checkout.session.completed`, `customer.subscription.deleted`

5. **Accredited investor CRM export** — CSV download action in admin
   - One bulk action: "Export selected to CSV"
   - Fields: name, email, country, capital_range, status, registered_at

6. **Author profile page** — E-E-A-T signal for Google + GEO
   - Simple `Person` schema with YouTube channel, Twitter, bio
   - Linked from every post byline

### Lower priority — post-launch
7. **VideoObject JSON-LD** on video detail pages
8. **Full-text search** — `django-watson` or PostgreSQL `SearchVector`
9. **Social auth** — Google login via `django-allauth`
10. **Discord community tier** — gate access to a Discord server invite link

---

## Deployment checklist (run before going live)

```
[ ] Droplet created on DigitalOcean (Toronto region, 2GB RAM)
[ ] DNS A record for @ and www pointing to Droplet IP at Tsunami.ca
[ ] DNS propagated — verify with: dig miningstockreport.com A
[ ] .env filled in — SECRET_KEY, DATABASE_URL, SITE_URL, email settings
[ ] python manage.py migrate --settings=config.settings.production
[ ] python manage.py collectstatic --noinput
[ ] python manage.py createsuperuser
[ ] Supervisor running — sudo supervisorctl status miningstock
[ ] Nginx config tested — sudo nginx -t
[ ] SSL cert issued — sudo certbot --nginx -d miningstockreport.com -d www.miningstockreport.com
[ ] https://miningstockreport.com loads without errors
[ ] /admin/ accessible and login works
[ ] /robots.txt returns correct content
[ ] /llms.txt returns correct content
[ ] /sitemap.xml returns XML
[ ] Static files load (CSS/JS 200 in browser network tab)
[ ] Subscribe form submits and email arrives
[ ] Accredited investor form submits and appears in /admin/investors/
[ ] og-default.svg replaced with real 1200x630px PNG
[ ] Sitemap submitted to Google Search Console
[ ] DigitalOcean monitoring alerts enabled
```

---

## Common Claude Code tasks

When asked to work on this project, here are the most common task types and how to approach them:

**Adding a new field to a model:**
1. Add the field to the model in `apps/<app>/models.py`
2. Run `python manage.py makemigrations`
3. Run `python manage.py migrate`
4. Update the admin `fieldsets` in `apps/<app>/admin.py`
5. Update the relevant API serializer in `apps/<app>/api.py`
6. Update the template if the field should render

**Adding a new page:**
1. Add the view to `apps/<app>/views.py`
2. Add the URL to `apps/<app>/urls.py`
3. Create the template in `templates/<app>/`
4. Add to sitemap in `apps/core/sitemaps.py` if it's a public page

**Changing a URL prefix:**
- Only change URLs that have no indexed content yet
- Update `apps/<app>/urls.py`
- Update `config/urls.py` prefix
- Update any `{% url %}` tags in templates
- Update sitemap and llms.txt references

**Deploying an update:**
```bash
cd /home/deploy/miningstock
./deploy.sh
```

**Checking logs:**
```bash
tail -f /var/log/miningstock/error.log
sudo supervisorctl status miningstock
sudo journalctl -u nginx -f
```

**Database access:**
```bash
source venv/bin/activate
python manage.py dbshell
# or
psql -U msr_user -d miningstockreport
```
