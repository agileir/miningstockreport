# Mining Stock Report — Django Project

Full-stack Django 5 project for **MiningStockReport.com** — a junior mining stock
analysis platform built around the YouTube brand.

---

## Project Structure

```
miningstock/
├── apps/
│   ├── accounts/       # Custom User model + membership tiers
│   ├── blog/           # Posts with 4 content pillars + premium gating
│   ├── core/           # Home, about, context processor, sitemap
│   ├── leads/          # Email capture + lead magnet delivery
│   ├── verdict/        # Company scorecards — the 5-factor Verdict Framework
│   ├── videos/         # YouTube video archive
│   └── watchlist/      # Stock watchlist with thesis + price tracking
├── config/
│   ├── settings/
│   │   ├── base.py
│   │   ├── development.py
│   │   └── production.py
│   ├── urls.py         # Frontend routes
│   └── api_urls.py     # DRF API v1 routes
├── static/
│   ├── css/main.css
│   └── js/main.js
├── templates/          # All HTML templates (Bootstrap 5, dark theme)
├── requirements/
│   ├── base.txt
│   ├── development.txt
│   └── production.txt
├── .env.example
├── manage.py
└── Procfile
```

---

## Quick Start (Local Development)

### 1. Clone and set up environment

```bash
git clone <your-repo>
cd miningstock
python -m venv venv
source venv/bin/activate          # Windows: venv\Scripts\activate
pip install -r requirements/development.txt
```

### 2. Configure environment

```bash
cp .env.example .env
# Edit .env — at minimum set SECRET_KEY and DATABASE_URL
```

Generate a secret key:
```bash
python -c "import secrets; print(secrets.token_urlsafe(50))"
```

### 3. Run migrations and create superuser

```bash
python manage.py migrate
python manage.py createsuperuser
```

### 4. Start the dev server

```bash
python manage.py runserver
```

Visit `http://127.0.0.1:8000` — admin at `http://127.0.0.1:8000/admin/`

---

## API

REST API is at `/api/v1/`. JWT auth for mobile app.

| Endpoint | Description |
|---|---|
| `GET /api/v1/posts/` | Blog posts (filter: `?pillar=due-diligence`) |
| `GET /api/v1/videos/` | YouTube archive (filter: `?featured=1`) |
| `GET /api/v1/companies/` | Companies with latest verdict |
| `GET /api/v1/verdicts/` | Published scorecards (filter: `?verdict=BUY`) |
| `GET /api/v1/watchlist/` | Active watchlist items |
| `POST /api/v1/subscribe/` | Email capture |
| `POST /api/v1/auth/token/` | Obtain JWT token |
| `POST /api/v1/auth/token/refresh/` | Refresh JWT token |

---

## Production Deployment

### Environment variables required in production

```
SECRET_KEY=
DEBUG=False
ALLOWED_HOSTS=miningstockreport.com,www.miningstockreport.com
DATABASE_URL=postgres://...
SITE_URL=https://miningstockreport.com
DEFAULT_FROM_EMAIL=
EMAIL_HOST=
EMAIL_PORT=587
EMAIL_HOST_USER=
EMAIL_HOST_PASSWORD=
```

### Deploy to Railway / Render / Heroku

```bash
# Set DJANGO_SETTINGS_MODULE
DJANGO_SETTINGS_MODULE=config.settings.production

# The Procfile handles migrations + collectstatic automatically on deploy:
# release: python manage.py migrate --noinput && python manage.py collectstatic --noinput
# web: gunicorn config.wsgi --workers 2 --threads 4
```

### Deploy to VPS (Ubuntu + Nginx + Gunicorn)

```bash
# Install deps
pip install -r requirements/production.txt

# Collect static files
python manage.py collectstatic --noinput

# Run with gunicorn (use systemd service in production)
gunicorn config.wsgi:application --bind 0.0.0.0:8000 --workers 3

# Nginx — proxy_pass to gunicorn, serve /static/ from staticfiles/
```

---

## Content Pillars

| Pillar | Slug | Purpose |
|---|---|---|
| Due Diligence | `due-diligence` | How to evaluate juniors from first principles |
| Company Verdicts | `company-verdicts` | Deep dives with BUY / WATCH / AVOID verdict |
| Market Intelligence | `market-intelligence` | Macro context, catalyst calendar, sector |
| Accountability | `accountability` | Portfolio tracking, loss post-mortems, Q&A |

---

## The Verdict Framework

Five factors, each scored 1–5. Composite out of 25 drives the verdict.

| # | Factor | 1 (Weak) | 5 (Strong) |
|---|---|---|---|
| 1 | Management skin-in-the-game | No insider ownership | Significant aligned ownership |
| 2 | Project geology quality | Inferred only / poor grade | Measured+Indicated, strong grade |
| 3 | Capital structure health | Highly diluted, warrant overhang | Clean structure, funded |
| 4 | Catalyst proximity | No near-term catalysts | Drill results / feasibility imminent |
| 5 | Comparable acquisition value | Trading at/above peer multiples | Deep discount to peers |

**Composite thresholds (guideline, not hard rule):**
- 18–25 → BUY
- 11–17 → WATCH
- 1–10 → AVOID

---

## Membership Tiers (Future)

| Tier | Price | Access |
|---|---|---|
| Free | $0 | Public posts, watchlist snapshot, all videos |
| Founding Member | $19/mo | Full posts, pre-scored watchlist, scorecard PDF |
| Standard | $35/mo | Same as founding (post-launch price) |
| Discord Community | $49/mo | All of above + Discord access |

---

## Next Steps (Claude Code Tasks)

- [ ] Add `management command` to sync prices into `PriceCache` (Yahoo Finance / Alpha Vantage)
- [ ] Add `management command` to sync subscribers to Mailchimp
- [ ] Wire up sitemap to `config/urls.py`
- [ ] Add social auth (Google) via `django-allauth`
- [ ] Stripe webhook handler for membership upgrades
- [ ] Add full-text search with `django-watson` or PostgreSQL `SearchVector`
- [ ] Write test suite (`pytest-django`, factory-boy fixtures in requirements/development.txt)


---

## SEO / GEO Implementation

### What's included

| Feature | Location | Notes |
|---|---|---|
| `SEOMixin` abstract model | `apps/core/seo.py` | Inherited by Post, Video, Company, VerdictScorecard |
| `meta_title` / `meta_description` / `og_image` | All content models | Managed via admin |
| Full OG + Twitter Card meta | `templates/base.html` | Auto-derived from model fields |
| JSON-LD `Organization` schema | `templates/base.html` | Site-wide |
| JSON-LD `Article` schema | `templates/blog/post_detail.html` | Per post |
| JSON-LD `FAQPage` schema | `templates/blog/post_detail.html` | When `faq_items` populated |
| JSON-LD `Review` schema | `templates/verdict/scorecard_detail.html` | Verdict = structured review |
| JSON-LD `BreadcrumbList` | Post detail + scorecard detail | Blocks in base.html |
| `key_takeaways` field | `Post` model | Rendered at top of post; AI engines excerpt these |
| `faq_items` field | `Post` model | JSON array of {question, answer} — FAQ accordion + FAQPage schema |
| `word_count` + `reading_time` | `Post` model | Auto-calculated on save |
| `/sitemap.xml` | `config/urls.py` | Wired to Django sitemaps framework |
| `/robots.txt` | `apps/core/views.robots_txt` | Dynamic — blocks /admin/, /api/ |
| `/llms.txt` | `apps/core/views.llms_txt` | AI crawler guidance (Perplexity, ChatGPT, etc.) |
| URL structure | `config/urls.py` | `/analysis/`, `/companies/` — topically strong slugs |
| OG default image | `static/img/og-default.svg` | Replace with 1200×630px PNG before launch |

### SEO URL structure

| Section | URL prefix | Rationale |
|---|---|---|
| Blog posts | `/analysis/` | Stronger topical signal than `/blog/` |
| Companies | `/companies/` | Direct entity match for search queries |
| Watchlist | `/watchlist/` | Exact-match keyword |
| Videos | `/videos/` | Standard; YouTube embeds get VideoObject schema opportunity |

### GEO (AI search) checklist before launch

- [ ] Replace `static/img/og-default.svg` with a real 1200×630px PNG
- [ ] Add `key_takeaways` to every published post (3–5 bullets)
- [ ] Add `faq_items` to Due Diligence posts (2–4 Q&A pairs minimum)
- [ ] Verify `/llms.txt` and `/robots.txt` are accessible
- [ ] Submit `sitemap.xml` to Google Search Console and Bing Webmaster Tools
- [ ] Add `author` profile page with social links (signals E-E-A-T)
- [ ] Add `VideoObject` schema to video detail template
