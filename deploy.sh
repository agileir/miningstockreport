#!/bin/bash
# Auto-deploy: if origin/main is ahead of HEAD, pull and restart the app.
# No-op on every tick where nothing changed.
#
# Cron: */5 * * * * /home/deploy/miningstock/deploy.sh >> /var/log/miningstock/deploy.log 2>&1
set -e

cd /home/deploy/miningstock

# Fetch quietly so we know what's on origin without merging
git fetch origin main --quiet

LOCAL=$(git rev-parse HEAD)
REMOTE=$(git rev-parse origin/main)

if [ "$LOCAL" = "$REMOTE" ]; then
    exit 0  # nothing to do; silent
fi

echo "$(date '+%Y-%m-%d %H:%M:%S') Deploy: $LOCAL → $REMOTE"

# Diff lets us skip migrate/collectstatic when nothing relevant changed
CHANGED_FILES=$(git diff --name-only "$LOCAL" "$REMOTE")
NEEDS_MIGRATE=$(echo "$CHANGED_FILES" | grep -E '/migrations/.*\.py$' || true)
NEEDS_STATIC=$(echo "$CHANGED_FILES"  | grep -E '(static/|\.css$|\.js$|\.html$)' || true)
NEEDS_PYTHON=$(echo "$CHANGED_FILES"  | grep -E '\.py$' || true)

git pull origin main --quiet

source venv/bin/activate

if [ -n "$NEEDS_MIGRATE" ]; then
    echo "  running migrate"
    python manage.py migrate --noinput --settings=config.settings.production
fi

if [ -n "$NEEDS_STATIC" ]; then
    echo "  running collectstatic"
    python manage.py collectstatic --noinput --settings=config.settings.production >/dev/null
fi

# Restart only when Python or template changed — script-only commits (.sh, .md) don't need it
if [ -n "$NEEDS_PYTHON" ] || [ -n "$NEEDS_STATIC" ]; then
    echo "  restarting supervisor"
    sudo supervisorctl restart miningstock
fi

echo "$(date '+%Y-%m-%d %H:%M:%S') Deploy complete at $REMOTE"
