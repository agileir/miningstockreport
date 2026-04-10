# Mining Stock Report — Deployment Plan

**Domain:** miningstockreport.com  
**DNS:** ns1.tsunami.ca / ns2.tsunami.ca  
**Server:** DigitalOcean Droplet  
**Stack:** Django 5 · PostgreSQL · Gunicorn · Nginx · Ubuntu 24.04 LTS

---

## Phase 1 — DigitalOcean Droplet

### 1.1 Create the Droplet

1. Log into [cloud.digitalocean.com](https://cloud.digitalocean.com)
2. Click **Create → Droplets**
3. Configure:

| Setting | Value |
|---|---|
| Region | **Toronto** (closest to Surrey BC) |
| OS | Ubuntu 24.04 LTS x64 |
| Plan | Basic — **Regular** |
| Size | **2 vCPU / 2GB RAM / 60GB SSD** ($18/mo) — upgrade to 4GB when traffic grows |
| Authentication | SSH Key (add your public key) |
| Hostname | `msr-prod-01` |
| Backups | Enable ($3.60/mo — worth it) |

4. Once created, note the **Droplet IP address** — you'll need it for DNS.

### 1.2 Initial server hardening

```bash
# SSH in as root first
ssh root@YOUR_DROPLET_IP

# Create deploy user
adduser deploy
usermod -aG sudo deploy
rsync --archive --chown=deploy:deploy ~/.ssh /home/deploy

# Lock down SSH
nano /etc/ssh/sshd_config
# Change these lines:
#   PermitRootLogin no
#   PasswordAuthentication no
systemctl restart sshd

# Firewall — allow SSH, HTTP, HTTPS only
ufw allow OpenSSH
ufw allow 'Nginx Full'
ufw enable
ufw status

# Exit and re-login as deploy from now on
exit
ssh deploy@YOUR_DROPLET_IP
```

### 1.3 Install system dependencies

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y \
  python3 python3-pip python3-venv python3-dev \
  postgresql postgresql-contrib \
  nginx certbot python3-certbot-nginx \
  git build-essential libpq-dev \
  supervisor
```

---

## Phase 2 — DNS configuration at Tsunami.ca

> You need the Droplet IP from Phase 1 before doing this.

### 2.1 Log into Tsunami.ca control panel

Navigate to the DNS management section for **miningstockreport.com**.

### 2.2 DNS records to create/update

| Type | Host | Value | TTL |
|---|---|---|---|
| A | `@` | `YOUR_DROPLET_IP` | 300 |
| A | `www` | `YOUR_DROPLET_IP` | 300 |
| CNAME | `miningstockreport.com` | — | (A record handles root) |

**Set TTL to 300 (5 minutes)** before making changes so propagation is fast. You can raise it to 3600 after the site is confirmed live.

### 2.3 Verify nameservers

Confirm the domain is using Tsunami's nameservers. In the Tsunami control panel, the nameservers should show:

```
ns1.tsunami.ca
ns2.tsunami.ca
```

If they're not set, update them under **Domain → Nameservers**.

### 2.4 Check propagation

DNS propagation takes 5–30 minutes with TTL 300. Check with:

```bash
# From your local machine
dig miningstockreport.com A
dig www.miningstockreport.com A

# Or use: https://dnschecker.org — search miningstockreport.com
```

Both should return your Droplet IP before proceeding to Phase 3.

---

## Phase 3 — PostgreSQL database

```bash
# On the Droplet as deploy
sudo -u postgres psql

-- Inside psql:
CREATE DATABASE miningstockreport;
CREATE USER msr_user WITH PASSWORD 'GENERATE_A_STRONG_PASSWORD';
ALTER ROLE msr_user SET client_encoding TO 'utf8';
ALTER ROLE msr_user SET default_transaction_isolation TO 'read committed';
ALTER ROLE msr_user SET timezone TO 'America/Vancouver';
GRANT ALL PRIVILEGES ON DATABASE miningstockreport TO msr_user;
\q
```

Generate a strong password locally:
```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

---

## Phase 4 — Application deployment

### 4.1 Clone the repository

```bash
# On the Droplet as deploy
git clone https://github.com/YOUR_ORG/miningstock.git /home/deploy/miningstock
cd /home/deploy/miningstock

python3 -m venv venv
source venv/bin/activate
pip install -r requirements/production.txt
```

### 4.2 Environment file

```bash
cp .env.example .env
nano .env
```

Fill in every value:

```env
# Django
SECRET_KEY=<run: python3 -c "import secrets; print(secrets.token_urlsafe(50))">
DEBUG=False
ALLOWED_HOSTS=miningstockreport.com,www.miningstockreport.com
DJANGO_SETTINGS_MODULE=config.settings.production

# Database
DATABASE_URL=postgres://msr_user:YOUR_DB_PASSWORD@localhost:5432/miningstockreport

# Site
SITE_URL=https://miningstockreport.com
YOUTUBE_CHANNEL_URL=https://www.youtube.com/@YourChannelHandle
TWITTER_URL=https://twitter.com/yourhandle

# Email (use SendGrid free tier to start)
DEFAULT_FROM_EMAIL=noreply@miningstockreport.com
SERVER_EMAIL=noreply@miningstockreport.com
EMAIL_HOST=smtp.sendgrid.net
EMAIL_PORT=587
EMAIL_HOST_USER=apikey
EMAIL_HOST_PASSWORD=YOUR_SENDGRID_API_KEY

# Mailchimp (add when ready)
MAILCHIMP_API_KEY=
MAILCHIMP_LIST_ID=

# CORS (mobile app — add when ready)
CORS_ALLOWED_ORIGINS=

# Sentry (add when ready)
SENTRY_DSN=
```

### 4.3 Run migrations and collect static

```bash
source venv/bin/activate
python manage.py migrate --settings=config.settings.production
python manage.py collectstatic --noinput --settings=config.settings.production
python manage.py createsuperuser --settings=config.settings.production
```

---

## Phase 5 — Gunicorn service (via Supervisor)

### 5.1 Create Supervisor config

```bash
sudo nano /etc/supervisor/conf.d/miningstock.conf
```

Paste:

```ini
[program:miningstock]
command=/home/deploy/miningstock/venv/bin/gunicorn config.wsgi:application \
    --workers 3 \
    --threads 2 \
    --worker-class gthread \
    --bind unix:/run/miningstock.sock \
    --timeout 60 \
    --log-level info \
    --access-logfile /var/log/miningstock/access.log \
    --error-logfile /var/log/miningstock/error.log
directory=/home/deploy/miningstock
user=deploy
autostart=true
autorestart=true
stopasgroup=true
killasgroup=true
environment=DJANGO_SETTINGS_MODULE="config.settings.production"
```

```bash
# Create log directory
sudo mkdir -p /var/log/miningstock
sudo chown deploy:deploy /var/log/miningstock

# Start Gunicorn
sudo supervisorctl reread
sudo supervisorctl update
sudo supervisorctl start miningstock
sudo supervisorctl status
```

---

## Phase 6 — Nginx configuration

```bash
sudo nano /etc/nginx/sites-available/miningstock
```

Paste:

```nginx
server {
    listen 80;
    server_name miningstockreport.com www.miningstockreport.com;

    # Redirect www to non-www
    if ($host = www.miningstockreport.com) {
        return 301 https://miningstockreport.com$request_uri;
    }

    location / {
        return 301 https://$host$request_uri;
    }
}

server {
    listen 443 ssl http2;
    server_name miningstockreport.com;

    # SSL (filled in by Certbot in Phase 7)
    ssl_certificate     /etc/letsencrypt/live/miningstockreport.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/miningstockreport.com/privkey.pem;
    include             /etc/letsencrypt/options-ssl-nginx.conf;
    ssl_dhparam         /etc/letsencrypt/ssl-dhparams.pem;

    # Security headers
    add_header X-Frame-Options           "SAMEORIGIN"   always;
    add_header X-Content-Type-Options    "nosniff"      always;
    add_header Referrer-Policy           "strict-origin-when-cross-origin" always;
    add_header X-XSS-Protection          "1; mode=block" always;
    add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

    client_max_body_size 20M;

    # Static files (served directly by Nginx — faster than Django)
    location /static/ {
        alias /home/deploy/miningstock/staticfiles/;
        expires 1y;
        add_header Cache-Control "public, immutable";
        access_log off;
    }

    # Media files
    location /media/ {
        alias /home/deploy/miningstock/media/;
        expires 30d;
        add_header Cache-Control "public";
        access_log off;
    }

    # robots.txt and llms.txt — no logging
    location = /robots.txt  { access_log off; }
    location = /llms.txt    { access_log off; }
    location = /favicon.ico { access_log off; }

    # Proxy to Gunicorn
    location / {
        proxy_pass         http://unix:/run/miningstock.sock;
        proxy_set_header   Host              $host;
        proxy_set_header   X-Real-IP         $remote_addr;
        proxy_set_header   X-Forwarded-For   $proxy_add_x_forwarded_for;
        proxy_set_header   X-Forwarded-Proto $scheme;
        proxy_redirect     off;
        proxy_read_timeout 60s;
    }
}
```

```bash
# Enable site
sudo ln -s /etc/nginx/sites-available/miningstock /etc/nginx/sites-enabled/
sudo nginx -t
sudo systemctl reload nginx
```

---

## Phase 7 — SSL certificate (Let's Encrypt)

> DNS must be propagated before this step.

```bash
sudo certbot --nginx -d miningstockreport.com -d www.miningstockreport.com

# Test auto-renewal
sudo certbot renew --dry-run
```

Certbot auto-renews via a systemd timer — no manual action needed after this.

---

## Phase 8 — Smoke test

Work through this checklist after Phase 7:

```bash
# 1. Site loads over HTTPS
curl -I https://miningstockreport.com

# 2. www redirects to non-www
curl -I https://www.miningstockreport.com

# 3. Admin is accessible
open https://miningstockreport.com/admin/

# 4. robots.txt is live
curl https://miningstockreport.com/robots.txt

# 5. llms.txt is live
curl https://miningstockreport.com/llms.txt

# 6. sitemap.xml is live
curl https://miningstockreport.com/sitemap.xml

# 7. Static files load (check browser network tab for 200s on CSS/JS)

# 8. Email works — trigger a subscribe from the homepage and check inbox

# 9. Admin login works — log in at /admin/

# 10. Accredited investor form submits and appears in admin
```

---

## Phase 9 — Deploy script (for future updates)

Create `/home/deploy/deploy.sh`:

```bash
#!/bin/bash
set -e

echo "==> Pulling latest code"
cd /home/deploy/miningstock
git pull origin main

echo "==> Activating virtualenv"
source venv/bin/activate

echo "==> Installing dependencies"
pip install -r requirements/production.txt --quiet

echo "==> Running migrations"
python manage.py migrate --settings=config.settings.production

echo "==> Collecting static files"
python manage.py collectstatic --noinput --settings=config.settings.production

echo "==> Restarting Gunicorn"
sudo supervisorctl restart miningstock

echo "==> Done. Site is live."
```

```bash
chmod +x /home/deploy/deploy.sh
```

Future deploys are then a single command:
```bash
./deploy.sh
```

---

## Phase 10 — Post-launch checklist

### Search & AI indexing
- [ ] Submit `https://miningstockreport.com/sitemap.xml` to Google Search Console
- [ ] Submit sitemap to Bing Webmaster Tools
- [ ] Verify `robots.txt` and `llms.txt` are accessible
- [ ] Replace `static/img/og-default.svg` with a real 1200×630px PNG

### Admin setup
- [ ] Log into `/admin/` and create first blog post (even a placeholder — gets the sitemap populated)
- [ ] Add at least one Company and one VerdictScorecard so the Verdict Framework page renders
- [ ] Add at least one WatchlistItem so the watchlist page is not empty

### Email
- [ ] Confirm SendGrid is sending — subscribe from the homepage and verify delivery
- [ ] Set up a SendGrid sender identity for `noreply@miningstockreport.com`

### Monitoring
- [ ] Set up DigitalOcean Droplet monitoring alerts (CPU > 80%, disk > 80%)
- [ ] Add Sentry DSN to `.env` for production error tracking (free tier is sufficient)

---

## Architecture diagram

```
Browser / Mobile App
        │
        ▼
  Cloudflare (optional CDN — add later)
        │
        ▼
  Nginx (port 443, SSL)
  ├── /static/  → serve directly from disk
  ├── /media/   → serve directly from disk
  └── /         → proxy_pass → Gunicorn (unix socket)
                        │
                        ▼
                  Django 5 (config.settings.production)
                        │
                        ▼
                  PostgreSQL (localhost:5432)
```

---

## Cost estimate (monthly)

| Service | Cost |
|---|---|
| DigitalOcean Droplet (2GB) | $18/mo |
| DigitalOcean Backups | $3.60/mo |
| Domain (miningstockreport.com) | ~$1.50/mo (amortised) |
| SendGrid (up to 100 emails/day) | Free |
| Let's Encrypt SSL | Free |
| **Total** | **~$23/mo** |

Scales to $48/mo when you upgrade the Droplet to 4GB for newsletter launch traffic.

