"""
StockWatch authentication: login programmatically, persist cookies to disk,
refresh on demand.

Usage:
    from auth import get_session, ensure_logged_in
    session = get_session()                    # auto-logs in if no cached cookies
    pdf_bytes = ensure_logged_in(session, lambda s: s.get(url).content)
"""
import json
import os
import re
import sys
from pathlib import Path

import requests
from dotenv import load_dotenv

ROOT = Path(__file__).resolve().parent
COOKIE_FILE = ROOT / 'cookies.json'
load_dotenv(ROOT / '.env')

BASE = 'https://www.stockwatch.com'
LOGIN_URL = f'{BASE}/Old/Login'
USER_AGENT = (
    'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 '
    '(KHTML, like Gecko) Chrome/120.0 Safari/537.36'
)

# When logged out, requests for protected docs return an HTML form that
# auto-submits to /User/NotLoggedIn. Use this signature to detect it.
LOGGED_OUT_SIGNATURE = b'/User/NotLoggedIn'


class AuthError(RuntimeError):
    pass


def _new_session():
    s = requests.Session()
    s.headers.update({'User-Agent': USER_AGENT})
    return s


def _save_cookies(session):
    jar = [
        {'name': c.name, 'value': c.value, 'domain': c.domain, 'path': c.path}
        for c in session.cookies
    ]
    COOKIE_FILE.write_text(json.dumps(jar))
    os.chmod(COOKIE_FILE, 0o600)


def _load_cookies(session):
    if not COOKIE_FILE.exists():
        return False
    try:
        for c in json.loads(COOKIE_FILE.read_text()):
            session.cookies.set(c['name'], c['value'], domain=c['domain'], path=c['path'])
        return True
    except Exception:
        return False


def login(session=None):
    """Perform a fresh login. Returns the session."""
    user = os.getenv('STOCKWATCH_USER')
    pw   = os.getenv('STOCKWATCH_PASS')
    if not user or not pw:
        raise AuthError('STOCKWATCH_USER / STOCKWATCH_PASS not set in .env')

    session = session or _new_session()

    r = session.get(LOGIN_URL, timeout=15)
    r.raise_for_status()
    vs    = re.search(r'__VIEWSTATE"[^>]*value="([^"]+)"', r.text)
    vsgen = re.search(r'__VIEWSTATEGENERATOR"[^>]*value="([^"]+)"', r.text)
    if not vs or not vsgen:
        raise AuthError('Could not extract __VIEWSTATE from login page')

    form = {
        '__EVENTTARGET': '',
        '__EVENTARGUMENT': '',
        '__VIEWSTATE': vs.group(1),
        '__VIEWSTATEGENERATOR': vsgen.group(1),
        'ctl00$MainContent$tId': user,
        'ctl00$MainContent$tPw': pw,
        'ctl00$MainContent$bLogin': 'Then click HERE to log in',
    }
    r = session.post(LOGIN_URL, data=form, timeout=15, allow_redirects=False)
    if r.status_code != 302:
        raise AuthError(f'Login POST returned {r.status_code}, expected 302')
    # Trust the 302 — actual auth-state is verified on the first protected fetch.
    _save_cookies(session)
    return session


def get_session(force=False):
    """Return a session, reusing cached cookies when possible. Re-login if forced."""
    session = _new_session()
    if not force and _load_cookies(session):
        return session
    return login(session)


def is_logged_out_response(content):
    """True if the response body is the auto-submit-to-NotLoggedIn form."""
    return LOGGED_OUT_SIGNATURE in content[:512] if content else False


def authed_get(session, url, **kwargs):
    """GET with auto re-login if we get the logged-out marker. Returns Response."""
    r = session.get(url, **kwargs)
    if is_logged_out_response(r.content):
        login(session)
        r = session.get(url, **kwargs)
    return r


if __name__ == '__main__':
    force = '--force' in sys.argv
    s = get_session(force=force)
    print('Session ready. Cookies:', sorted(s.cookies.keys()))
    # Sanity check: try fetching a known auth-gated URL.
    test_url = f'{BASE}/News/Item/Z-C!AMX-3809307/C/AMX'
    r = authed_get(s, test_url, timeout=30)
    starts = r.content[:5]
    print(f'Test fetch: {r.status_code}, content-type={r.headers.get("Content-Type")}, starts={starts!r}')
    print('Authenticated:', starts == b'%PDF-')
