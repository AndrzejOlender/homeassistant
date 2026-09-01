#!/usr/bin/env python3
"""
Aqua-Sprint eBOK water meter statistic updater for Home Assistant.

Logs into the Wodociagi Siemianowickie Aqua-Sprint customer portal (an Oracle
APEX / ORDS application), reads the water meter's latest cumulative "Stan"
(m3) plus its reading date, and imports the value as the external statistic
aqua_sprint:water_consumption. The utility only publishes a new radio-meter
reading every ~30 days, and the whole delta is attributed to the reading date
rather than spread over the period, so a calendar month containing one reading
totals exactly what that invoice says. Spreading it evenly looks better on a
daily chart but leaves every month a few tenths of a m3 off, because readings
land around the 28th-30th instead of on month boundaries.

An external (colon-id) statistic is used rather than a sensor entity so the
recorder never compiles competing rows for the same statistic_id; this script
owns the whole series. Same technique as tauron_g12w_cost.py in this repo, and
the grid source already proves the Energy dashboard accepts external stats.

The portal side is deliberately plain urllib (stdlib only, no aiohttp): the
login is a fragile, reverse-engineered APEX flow and this is the exact client
it was verified against. The Home Assistant side uses aiohttp over the
websocket API, matching tauron_g12w_cost.py.

Notes on the APEX login, all established empirically - change with care:
  * The login page carries <base href="/ords/">; the form's relative action
    resolves against THAT, not against the page URL (otherwise: 404).
  * In the <form> tag, action= precedes id=, so attribute-order-agnostic
    parsing is required.
  * p_request must be P102_ZALOGUJ, taken from the button's onclick (where
    quotes are &#x27;-escaped); the hidden p_request field is empty.
  * The POST is an XHR, not a navigation: X-Requested-With, Origin,
    Sec-Fetch-* and an application/json Accept are all required.
  * Cookies ORA_WWV_APP_150$P=-1 and cookies_accepted=T are set client-side
    by the portal's own JS and must be added manually.
  * Credentials are NOT flat form fields - they go inside p_json, and "salt"
    is a TOP-LEVEL sibling of "pageItems" (nesting it inside yields
    "Checksum content error"). Protected items need their per-item "ck"
    signature from the matching <input data-for="..."> element.
  * The meter data is a lazily-loaded APEX "Cards" region fetched separately;
    its ajaxIdentifier appears in a JS string literal where "/" is written
    \\u002F and MUST be unescaped (otherwise: "Checksum format error").

Cost is derived from the consumption statistic and imported as a second
external statistic, aqua_sprint:water_cost, which is wired into the water
source's stat_cost (external statistics cannot use entity_energy_price /
number_energy_price - HA rejects that combination). The billed amount is
water + sewage per m3 plus a fixed monthly subscription, all gross, matching
what the utility actually invoices; rates live in input_number helpers so
they stay editable from the UI when the tariff changes.

Usage:
  aqua_sprint_water.py                normal incremental run (used by command_line)
  aqua_sprint_water.py --seed         one-time backfill of the known reading
                                      history; refuses to run if data exists
  aqua_sprint_water.py --rebuild      DESTRUCTIVE: wipe both statistics and
                                      re-seed from scratch
  aqua_sprint_water.py --rebuild-cost DESTRUCTIVE for cost only: recompute the
                                      whole cost series at the current rates,
                                      leaving consumption untouched. Use after
                                      correcting the rate helpers.
"""
import asyncio
import calendar
import html
import http.cookiejar
import json
import os
import re
import ssl
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import date, datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import yaml

try:
    import aiohttp
except ImportError as e:  # pragma: no cover - surfaced via sensor state
    print(json.dumps({"status": "error", "error": f"missing dependency: {e}"}))
    sys.exit(0)

DEFAULT_SECRETS_PATH = "/config/secrets.yaml"
DEFAULT_SESSION_PATH = "/config/.storage/aqua_sprint_session.json"

USERNAME_KEY = "aqua_sprint_username"
PASSWORD_KEY = "aqua_sprint_password"
# Any HA long-lived access token works; fall back to the one that already
# exists in secrets.yaml so no second token has to be created.
TOKEN_KEYS = ("aqua_sprint_ha_token", "tauron_g12w_cost_token")

STAT_ID = "aqua_sprint:water_consumption"
STAT_SOURCE = "aqua_sprint"
STAT_NAME = "Aqua-Sprint Water Consumption"
STAT_UNIT = "m³"  # U+00B3, matching HA's UnitOfVolume.CUBIC_METERS

COST_STAT_ID = "aqua_sprint:water_cost"
COST_NAME = "Aqua-Sprint Water Cost"
COST_UNIT = "PLN"

# Rates are read live from helpers so the tariff stays editable from the UI.
# Values are NET, exactly as printed on the tariff/invoice; VAT is applied
# here (water and sewage are both 8% in Poland).
WATER_RATE_ENTITY = "input_number.aqua_sprint_water_rate"
SEWAGE_RATE_ENTITY = "input_number.aqua_sprint_sewage_rate"
MONTHLY_FEE_ENTITY = "input_number.aqua_sprint_monthly_fee"
VAT_RATE_ENTITY = "input_number.aqua_sprint_vat_rate"

BASE_URL = "https://e-bok.aqua-sprint.pl"
LOGIN_PATH = "/ords/r/ebok/e/logowanie"
WODOMIERZE_PATH = "/ords/r/ebok/e/wodomierze"
METER_NUMBER = "26BA079935"

WARSAW = ZoneInfo("Europe/Warsaw")

UA = ("Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 "
      "(KHTML, like Gecko) Version/26.5 Safari/605.1.15")

# Reading history transcribed from the portal on 2026-09-01, used only by
# --seed. The meter was installed reading 0.00, so the statistic's cumulative
# sum and the meter's absolute Stan coincide - no offset is ever needed.
SEED_HISTORY = [
    (date(2026, 4, 14), 0.0),
    (date(2026, 4, 29), 5.0),
    (date(2026, 5, 28), 13.0),
    (date(2026, 6, 29), 24.0),
    (date(2026, 7, 30), 32.0),
    (date(2026, 8, 28), 40.0),
]


# --------------------------------------------------------------------------
# configuration
# --------------------------------------------------------------------------

def load_secrets() -> dict:
    path = os.environ.get("HA_SECRETS_PATH", DEFAULT_SECRETS_PATH)
    with open(path) as f:
        return yaml.safe_load(f) or {}


def resolve_credentials(secrets: dict) -> tuple[str, str]:
    """Portal credentials. Env wins for manual runs, else secrets.yaml -
    command_line sensors cannot interpolate !secret into a command string."""
    username = os.environ.get("AQUA_SPRINT_USERNAME") or secrets.get(USERNAME_KEY)
    password = os.environ.get("AQUA_SPRINT_PASSWORD") or secrets.get(PASSWORD_KEY)
    if not username or not password:
        raise RuntimeError(f"{USERNAME_KEY}/{PASSWORD_KEY} missing from secrets.yaml")
    return str(username), str(password)


def resolve_connection(secrets: dict) -> tuple[str, str]:
    """Return (base_url, token) for Home Assistant itself."""
    env_server = os.environ.get("HASS_SERVER")
    env_token = os.environ.get("HASS_TOKEN")
    if env_server and env_token:
        return env_server.rstrip("/"), env_token

    for key in TOKEN_KEYS:
        token = secrets.get(key)
        if token:
            return "http://localhost:8123", token
    raise RuntimeError(f"no HA token in secrets.yaml (tried: {', '.join(TOKEN_KEYS)})")


def session_path() -> str:
    return os.environ.get("AQUA_SPRINT_SESSION_PATH", DEFAULT_SESSION_PATH)


# --------------------------------------------------------------------------
# portal: HTML helpers
# --------------------------------------------------------------------------

def _unescape_js(value: str) -> str:
    """Decode \\uXXXX escapes found inside JS string literals."""
    return re.sub(r"\\u([0-9A-Fa-f]{4})", lambda m: chr(int(m.group(1), 16)), value)


def input_by_name(page: str, name: str) -> str:
    for pattern in (
        r'<input\b[^>]*\bname="%s"[^>]*\bvalue="([^"]*)"' % re.escape(name),
        r'<input\b[^>]*\bvalue="([^"]*)"[^>]*\bname="%s"' % re.escape(name),
    ):
        m = re.search(pattern, page)
        if m:
            return html.unescape(m.group(1))
    return ""


def input_by_id(page: str, element_id: str) -> str:
    """Several APEX state fields carry id= but no name=; apex.submit reads
    them by id and sends them under that id."""
    for pattern in (
        r'<input\b[^>]*\bid="%s"[^>]*\bvalue="([^"]*)"' % re.escape(element_id),
        r'<input\b[^>]*\bvalue="([^"]*)"[^>]*\bid="%s"' % re.escape(element_id),
    ):
        m = re.search(pattern, page)
        if m:
            return html.unescape(m.group(1))
    return ""


def checksum_for(page: str, item_name: str) -> str | None:
    """Per-item checksum of a protected page item, held in a sibling
    <input data-for="ITEM_NAME" value="...">."""
    for pattern in (
        r'<input\b[^>]*\bdata-for="%s"[^>]*\bvalue="([^"]*)"' % re.escape(item_name),
        r'<input\b[^>]*\bvalue="([^"]*)"[^>]*\bdata-for="%s"' % re.escape(item_name),
    ):
        m = re.search(pattern, page)
        if m:
            return html.unescape(m.group(1))
    return None


def page_items(page: str) -> list[dict]:
    """Every P<n>_* item on the page with its value and, when protected, its
    checksum - what apex.submit serialises into p_json."""
    items, seen = [], set()
    for m in re.finditer(r"<input\b[^>]*>", page):
        tag = m.group(0)
        name_match = re.search(r'\bname="(P\d+_[A-Z0-9_]+)"', tag)
        if not name_match or name_match.group(1) in seen:
            continue
        name = name_match.group(1)
        seen.add(name)
        value_match = re.search(r'\bvalue="([^"]*)"', tag)
        item = {"n": name, "v": html.unescape(value_match.group(1)) if value_match else ""}
        checksum = checksum_for(page, name)
        if checksum is not None:
            item["ck"] = checksum
        items.append(item)
    return items


def form_region_checksums(page: str) -> list:
    try:
        return json.loads(input_by_id(page, "pPageFormRegionChecksums") or "[]")
    except json.JSONDecodeError:
        return []


# --------------------------------------------------------------------------
# portal: HTTP
# --------------------------------------------------------------------------

def build_opener(jar: http.cookiejar.CookieJar) -> urllib.request.OpenerDirector:
    return urllib.request.build_opener(
        urllib.request.HTTPSHandler(context=ssl.create_default_context()),
        urllib.request.HTTPCookieProcessor(jar),
    )


def add_client_cookies(jar: http.cookiejar.CookieJar) -> None:
    """Two cookies the portal's own JS sets client-side; the server never
    Set-Cookie's them, but the real browser always sends them."""
    for name, value in (("ORA_WWV_APP_150$P", "-1"), ("cookies_accepted", "T")):
        jar.set_cookie(http.cookiejar.Cookie(
            version=0, name=name, value=value, port=None, port_specified=False,
            domain="e-bok.aqua-sprint.pl", domain_specified=True,
            domain_initial_dot=False, path="/", path_specified=True,
            secure=True, expires=None, discard=True,
            comment=None, comment_url=None, rest={},
        ))


def fetch(opener, url: str, data: bytes | None = None, referer: str | None = None,
          ajax: bool = False) -> tuple[int, str, str]:
    headers = {"User-Agent": UA, "Accept-Language": "pl-PL,pl;q=0.9,en-US;q=0.8,en;q=0.7"}
    if referer:
        headers["Referer"] = referer
    if data is None:
        headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        request = urllib.request.Request(url, headers=headers)
    else:
        headers["Content-Type"] = "application/x-www-form-urlencoded; charset=UTF-8"
        if ajax:
            headers.update({
                "Accept": "application/json, text/javascript, */*; q=0.01",
                "X-Requested-With": "XMLHttpRequest",
                "Origin": BASE_URL,
                "Sec-Fetch-Dest": "empty",
                "Sec-Fetch-Mode": "cors",
                "Sec-Fetch-Site": "same-origin",
            })
        else:
            headers["Accept"] = "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8"
        request = urllib.request.Request(url, data=data, headers=headers, method="POST")
    try:
        response = opener.open(request, timeout=30)
        return response.status, response.geturl(), response.read().decode("utf-8", errors="replace")
    except urllib.error.HTTPError as e:
        return e.code, url, e.read().decode("utf-8", errors="replace")


def is_logged_out(page: str) -> bool:
    return 'name="P102_USERNAME"' in page or 'name="P102_PASSWORD"' in page


# --------------------------------------------------------------------------
# portal: session persistence
# --------------------------------------------------------------------------

def load_session() -> dict:
    """Any problem at all (missing, corrupt, wrong shape) means cold start."""
    try:
        with open(session_path()) as f:
            stored = json.load(f)
        return {
            "cookies": dict(stored["cookies"]),
            "session_id": str(stored["session_id"]),
        }
    except (OSError, json.JSONDecodeError, KeyError, TypeError, ValueError):
        return {"cookies": {}, "session_id": None}


def save_session(jar: http.cookiejar.CookieJar, session_id: str) -> None:
    cookies = {c.name: c.value for c in jar if "aqua-sprint.pl" in (c.domain or "")}
    payload = {
        "cookies": cookies,
        "session_id": session_id,
        "saved_at": datetime.now(timezone.utc).isoformat(),
    }
    path = session_path()
    try:
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w") as f:
            json.dump(payload, f)
    except OSError:
        # A stale session only costs one extra login next run - never fatal.
        pass


def restore_cookies(jar: http.cookiejar.CookieJar, cookies: dict) -> None:
    for name, value in cookies.items():
        jar.set_cookie(http.cookiejar.Cookie(
            version=0, name=name, value=value, port=None, port_specified=False,
            domain="e-bok.aqua-sprint.pl", domain_specified=True,
            domain_initial_dot=False, path="/", path_specified=True,
            secure=True, expires=None, discard=True,
            comment=None, comment_url=None, rest={},
        ))


# --------------------------------------------------------------------------
# portal: login and reading
# --------------------------------------------------------------------------

def login(opener, username: str, password: str) -> str:
    """Perform the APEX login; return the authenticated session id."""
    status, url, page = fetch(opener, BASE_URL + LOGIN_PATH)
    if status != 200:
        raise RuntimeError(f"login page returned HTTP {status}")

    form_tag_match = re.search(r'<form\b[^>]*\bid="wwvFlowForm"[^>]*>', page)
    if form_tag_match is None:
        raise RuntimeError("login form not found - portal markup changed")
    action_match = re.search(r'\baction="([^"]*)"', form_tag_match.group(0))
    if action_match is None:
        raise RuntimeError("login form has no action - portal markup changed")

    base_match = re.search(r'<base\b[^>]*href="([^"]*)"', page, re.I)
    resolve_base = urllib.parse.urljoin(url, base_match.group(1)) if base_match else url
    post_url = urllib.parse.urljoin(resolve_base, html.unescape(action_match.group(1)))

    request_match = re.search(r"apex\.submit\(\{request:&#x27;([^&']+)&#x27;", page)
    if request_match is None:
        raise RuntimeError("login button request value not found - portal markup changed")

    items = [
        {"n": "P102_CZY_KONTRAST", "v": input_by_name(page, "P102_CZY_KONTRAST")},
        {"n": "P102_AUTENTI_STATUS", "v": input_by_name(page, "P102_AUTENTI_STATUS"),
         "ck": checksum_for(page, "P102_AUTENTI_STATUS")},
        {"n": "P102_HTTP", "v": "https:"},
        {"n": "P102_IP", "v": ""},  # audit-only; verified accepted as empty
        {"n": "P102_NAZWA", "v": input_by_name(page, "P102_NAZWA"),
         "ck": checksum_for(page, "P102_NAZWA")},
        {"n": "P102_WLASCICIEL", "v": input_by_name(page, "P102_WLASCICIEL"),
         "ck": checksum_for(page, "P102_WLASCICIEL")},
        {"n": "P102_USERNAME", "v": username},
        {"n": "P102_PASSWORD", "v": password},
    ]
    for item in items:
        if item.get("ck") is None:
            item.pop("ck", None)

    p_json = {
        "pageItems": {
            "itemsToSubmit": items,
            "protected": input_by_id(page, "pPageItemsProtected"),
            "rowVersion": input_by_id(page, "pPageItemsRowVersion"),
            "formRegionChecksums": form_region_checksums(page),
        },
        "salt": input_by_id(page, "pSalt"),
    }
    payload = {
        "p_flow_id": input_by_name(page, "p_flow_id"),
        "p_flow_step_id": input_by_name(page, "p_flow_step_id"),
        "p_instance": input_by_name(page, "p_instance"),
        "p_debug": "",
        "p_request": request_match.group(1),
        "p_reload_on_submit": input_by_name(page, "p_reload_on_submit"),
        "p_page_submission_id": input_by_name(page, "p_page_submission_id"),
        "p_json": json.dumps(p_json, separators=(",", ":"), ensure_ascii=False),
    }

    status, _, body = fetch(
        opener, post_url, data=urllib.parse.urlencode(payload).encode(),
        referer=url, ajax=True)
    if status != 200:
        raise RuntimeError(f"login POST returned HTTP {status}")

    redirect_match = re.search(r'"redirectURL":"([^"]*)"', body)
    if redirect_match is None:
        if '"error"' in body:
            error = json.loads(body).get("error", "unknown")
            raise RuntimeError(f"login rejected by portal: {error}")
        raise RuntimeError("unexpected login response - portal behaviour changed")

    redirect = json.loads(f'"{redirect_match.group(1)}"')
    if "notification_msg" in redirect:
        # The portal signals bad credentials by redirecting back to the login
        # page with a signed, base64 message.
        raise RuntimeError("login failed - portal reports invalid credentials")

    session_match = re.search(r"[?&]session=(\d+)", redirect)
    if session_match is None:
        raise RuntimeError("logged in but no session id in redirect")
    return session_match.group(1)


def fetch_reading(opener, session_id: str) -> tuple[date, float]:
    """Return (reading_date, stan_m3) for the configured meter."""
    url = f"{BASE_URL}{WODOMIERZE_PATH}?session={session_id}"
    status, page_url, page = fetch(opener, url)
    if status != 200:
        raise RuntimeError(f"wodomierze page returned HTTP {status}")
    if is_logged_out(page):
        raise RuntimeError("session not authenticated")

    region_match = re.search(
        r'"regionStaticId":"R_AKTYWNE_WODOMIERZE_20","regionType":"Cards",'
        r'"ajaxIdentifier":"([^"]+)"', page)
    region_id_match = re.search(
        r'apex\.widget\.templateReportRegionInit\(\{"regionId":"(\d+)"', page)
    if region_match is None or region_id_match is None:
        raise RuntimeError("meter region not found - portal markup changed")

    p_json = {
        "pageItems": {
            "itemsToSubmit": page_items(page),
            "protected": input_by_id(page, "pPageItemsProtected"),
            "rowVersion": input_by_id(page, "pPageItemsRowVersion"),
            "formRegionChecksums": form_region_checksums(page),
        },
        "salt": input_by_id(page, "pSalt"),
        "regions": [{
            "id": region_id_match.group(1),
            "fetchData": {"version": 1, "firstRow": 1, "maxRows": 100},
        }],
    }
    payload = {
        "p_flow_id": input_by_name(page, "p_flow_id"),
        "p_flow_step_id": input_by_name(page, "p_flow_step_id"),
        "p_instance": input_by_name(page, "p_instance"),
        "p_debug": "",
        # The identifier sits in a JS literal with / for "/" - sending it
        # escaped yields "Checksum format error".
        "p_request": "PLUGIN=" + _unescape_js(region_match.group(1)),
        "p_json": json.dumps(p_json, separators=(",", ":"), ensure_ascii=False),
    }

    status, _, body = fetch(
        opener, BASE_URL + "/ords/wwv_flow.ajax",
        data=urllib.parse.urlencode(payload).encode(), referer=page_url, ajax=True)
    if status != 200:
        raise RuntimeError(f"meter region fetch returned HTTP {status}")

    try:
        fetched = json.loads("{" + body.strip().rstrip(",") + "}")["fetchedData"]
    except (json.JSONDecodeError, KeyError):
        snippet = body.strip()[:200]
        raise RuntimeError(f"unexpected meter region response: {snippet}")

    fields = _field_indexes(page)
    rows = fetched.get("values") or []
    if not rows:
        raise RuntimeError("meter region returned no rows")

    for row in rows:
        if _cell(row, fields, "GZKWODOMIERZ_NRFABR") == METER_NUMBER:
            raw_date = _cell(row, fields, "DATA_OSTATNIEGO_STANU")
            raw_stan = _cell(row, fields, "STAN")
            if not raw_date or not raw_stan:
                raise RuntimeError("meter row is missing Stan or reading date")
            return _parse_date(raw_date), _parse_decimal(raw_stan)
    raise RuntimeError(f"meter {METER_NUMBER} not present in portal response")


def _field_indexes(page: str) -> dict:
    """Map the region's column names to positions, so the parsing does not
    depend on hardcoded column offsets."""
    m = re.search(r'\{"INFSIECINSTAL_ID":\{"index":\d+\}.*?\}\}', page)
    if m is None:
        raise RuntimeError("region field map not found - portal markup changed")
    return {name: meta["index"] for name, meta in json.loads(m.group(0)).items()}


def _cell(row: list, fields: dict, name: str):
    index = fields.get(name)
    if index is None or index >= len(row):
        return None
    return row[index]


def _parse_date(value: str) -> date:
    for fmt in ("%Y-%m-%d", "%d-%m-%Y", "%d.%m.%Y"):
        try:
            return datetime.strptime(value.strip(), fmt).date()
        except ValueError:
            continue
    raise RuntimeError(f"unrecognised reading date format: {value!r}")


def _parse_decimal(value: str) -> float:
    try:
        return float(str(value).strip().replace("\xa0", "").replace(" ", "").replace(",", "."))
    except ValueError:
        raise RuntimeError(f"unrecognised Stan value: {value!r}")


def get_reading() -> tuple[date, float, str]:
    """Reuse the stored session when it is still alive, else log in.
    Returns (reading_date, stan_m3, "reused"|"refreshed")."""
    secrets = load_secrets()
    username, password = resolve_credentials(secrets)

    stored = load_session()
    if stored["session_id"] and stored["cookies"]:
        jar = http.cookiejar.CookieJar()
        restore_cookies(jar, stored["cookies"])
        opener = build_opener(jar)
        try:
            reading = fetch_reading(opener, stored["session_id"])
            save_session(jar, stored["session_id"])
            return reading[0], reading[1], "reused"
        except RuntimeError:
            pass  # expired or changed - fall through to a fresh login

    jar = http.cookiejar.CookieJar()
    opener = build_opener(jar)
    fetch(opener, BASE_URL + LOGIN_PATH)  # obtain the server-issued cookie
    add_client_cookies(jar)
    session_id = login(opener, username, password)
    reading_date, stan = fetch_reading(opener, session_id)
    save_session(jar, session_id)
    return reading_date, stan, "refreshed"


# --------------------------------------------------------------------------
# statistics
# --------------------------------------------------------------------------

def local_midnight_utc(day: date) -> datetime:
    return datetime.combine(day, datetime.min.time(), tzinfo=WARSAW).astimezone(timezone.utc)


def step_points(start_day: date, start_sum: float, end_day: date, end_sum: float,
                include_start: bool) -> list[dict]:
    """Daily cumulative points that stay flat between readings and jump by the
    whole delta on the reading date.

    The utility bills the entire delta against the reading, so attributing it
    to that single day makes a calendar month containing one reading total
    exactly what the invoice says. Spreading it evenly instead would look
    nicer on a daily chart but leaves every month a few tenths of a m3 off,
    because readings fall around the 28th-30th rather than on month
    boundaries."""
    if end_day <= start_day:
        return []

    points = []
    if include_start:
        points.append({"start": local_midnight_utc(start_day).isoformat(),
                       "sum": round(start_sum, 4)})
    day = start_day + timedelta(days=1)
    while day < end_day:
        points.append({"start": local_midnight_utc(day).isoformat(),
                       "sum": round(start_sum, 4)})
        day += timedelta(days=1)
    points.append({"start": local_midnight_utc(end_day).isoformat(),
                   "sum": round(end_sum, 4)})
    return points


def build_seed_points() -> list[dict]:
    """Piecewise interpolation across the known readings - each real reading
    stays an exact anchor instead of one straight line across the whole span."""
    points = []
    for i in range(len(SEED_HISTORY) - 1):
        (day0, sum0), (day1, sum1) = SEED_HISTORY[i], SEED_HISTORY[i + 1]
        points.extend(step_points(day0, sum0, day1, sum1, include_start=(i == 0)))
    return points


class Api:
    """Thin websocket wrapper that owns the message id sequence."""

    def __init__(self, ws):
        self._ws = ws
        self._id = 0

    async def call(self, frame: dict) -> dict:
        self._id += 1
        payload = dict(frame)
        payload["id"] = self._id
        await self._ws.send_json(payload)
        return await self._ws.receive_json()

    async def rows(self, statistic_id: str) -> list:
        now = datetime.now(timezone.utc)
        result = await self.call({
            "type": "recorder/statistics_during_period",
            "start_time": (now - timedelta(days=1500)).isoformat(),
            "end_time": now.isoformat(),
            "statistic_ids": [statistic_id],
            "period": "day",
        })
        return result.get("result", {}).get(statistic_id, [])

    async def clear(self, statistic_id: str) -> None:
        cleared = await self.call({
            "type": "recorder/clear_statistics",
            "statistic_ids": [statistic_id],
        })
        if not cleared.get("success", True):
            raise RuntimeError(f"clear_statistics failed: {cleared}")
        # Queued on the recorder thread; let it land before re-reading.
        await asyncio.sleep(2)

    async def import_points(self, statistic_id: str, name: str, unit: str,
                            points: list) -> bool:
        imported = await self.call({
            "type": "recorder/import_statistics",
            "metadata": {
                "has_mean": False,
                "has_sum": True,
                "name": name,
                "source": STAT_SOURCE,
                "statistic_id": statistic_id,
                "unit_of_measurement": unit,
            },
            "stats": points,
        })
        if not imported.get("success", True):
            raise RuntimeError(f"import_statistics failed for {statistic_id}: {imported}")

        # The recorder writes asynchronously, so the ack above only means
        # "queued". Confirm the rows landed, otherwise a lost write would
        # silently look like success and be redone from scratch next run.
        expected_last_ms = datetime.fromisoformat(points[-1]["start"]).timestamp() * 1000
        for _ in range(15):
            await asyncio.sleep(1)
            rows = await self.rows(statistic_id)
            if rows and max(r["start"] for r in rows) >= expected_last_ms:
                return True
        raise RuntimeError(
            f"imported {len(points)} points but they did not appear in "
            f"{statistic_id} within 15s")


async def update_consumption(api: Api, mode: str, reading_date, stan) -> dict:
    rows = await api.rows(STAT_ID)

    if mode in ("seed", "rebuild"):
        if rows:
            raise RuntimeError(
                f"{STAT_ID} already holds data; use --rebuild to wipe and re-seed")
        points = build_seed_points()
        last_date, last_sum = SEED_HISTORY[-1]
    else:
        if not rows:
            raise RuntimeError(
                f"{STAT_ID} is empty; run once with --seed to backfill history first")
        last_row = rows[-1]
        last_start = datetime.fromtimestamp(last_row["start"] / 1000, tz=timezone.utc)
        last_date = last_start.astimezone(WARSAW).date()
        last_sum = last_row["sum"]

        if reading_date <= last_date:
            return {
                "last_reading_date": last_date.isoformat(),
                "last_reading_m3": round(last_sum, 3),
                "days_imported": 0,
                "import_verified": None,
            }
        if stan < last_sum:
            raise RuntimeError(
                f"portal Stan {stan} is below the last imported total {last_sum} - "
                f"refusing to import a decreasing meter")
        points = step_points(last_date, last_sum, reading_date, stan, include_start=False)
        last_date, last_sum = reading_date, stan

    if not points:
        raise RuntimeError("nothing to import after interpolation")
    verified = await api.import_points(STAT_ID, STAT_NAME, STAT_UNIT, points)
    return {
        "last_reading_date": last_date.isoformat(),
        "last_reading_m3": round(last_sum, 3),
        "days_imported": len(points),
        "import_verified": verified,
    }


async def update_cost(api: Api, rebuild: bool) -> dict:
    """Price the consumption series: (water + sewage) per m3 plus the fixed
    monthly subscription, all gross - i.e. what the utility actually bills."""
    states = await api.call({"type": "get_states"})
    by_entity = {s["entity_id"]: s for s in states.get("result", [])}

    def helper(entity_id: str) -> float:
        try:
            return float(by_entity[entity_id]["state"])
        except (KeyError, ValueError, TypeError):
            raise RuntimeError(f"could not read rate helper {entity_id}")

    water_rate = helper(WATER_RATE_ENTITY)
    sewage_rate = helper(SEWAGE_RATE_ENTITY)
    monthly_fee = helper(MONTHLY_FEE_ENTITY)
    vat_rate = helper(VAT_RATE_ENTITY)
    if water_rate <= 0 or sewage_rate <= 0:
        raise RuntimeError(
            f"rate helpers not set (water={water_rate}, sewage={sewage_rate})")

    gross = 1 + vat_rate / 100
    per_m3 = (water_rate + sewage_rate) * gross
    fee_gross = monthly_fee * gross

    if rebuild:
        await api.clear(COST_STAT_ID)

    cost_rows = await api.rows(COST_STAT_ID)
    running = cost_rows[-1]["sum"] if cost_rows else 0.0
    resume_after = None
    if cost_rows:
        resume_after = datetime.fromtimestamp(cost_rows[-1]["start"] / 1000, tz=timezone.utc)

    points = []
    for row in await api.rows(STAT_ID):
        start = datetime.fromtimestamp(row["start"] / 1000, tz=timezone.utc)
        if resume_after is not None and start <= resume_after:
            continue
        change = row.get("change")
        if change is None:
            continue
        # Spread the fixed monthly charge evenly over the month it falls in,
        # so the cost curve stays smooth instead of stepping once a month.
        local = start.astimezone(WARSAW)
        days_in_month = calendar.monthrange(local.year, local.month)[1]
        running += change * per_m3 + fee_gross / days_in_month
        points.append({"start": start.isoformat(), "sum": round(running, 4)})

    verified = None
    if points:
        verified = await api.import_points(COST_STAT_ID, COST_NAME, COST_UNIT, points)

    return {
        "cost_days_imported": len(points),
        "cost_total_pln": round(running, 2),
        "cost_verified": verified,
        "rate_per_m3_gross": round(per_m3, 4),
    }


async def ensure_cost_wired(api: Api) -> bool:
    """Point the water source's stat_cost at our cost statistic. External
    statistics cannot use entity_energy_price/number_energy_price, so this is
    the only way the Energy dashboard will show a water cost."""
    prefs = await api.call({"type": "energy/get_prefs"})
    data = prefs.get("result")
    if not data:
        return False

    changed = False
    for source in data.get("energy_sources", []):
        if (source.get("type") == "water"
                and source.get("stat_energy_from") == STAT_ID
                and source.get("stat_cost") != COST_STAT_ID):
            source["stat_cost"] = COST_STAT_ID
            changed = True
    if not changed:
        return False

    # save_prefs replaces the whole preferences object, so this must be a
    # read-modify-write of everything, never a partial frame.
    frame = dict(data)
    frame["type"] = "energy/save_prefs"
    saved = await api.call(frame)
    if not saved.get("success", True):
        raise RuntimeError(f"save_prefs failed: {saved}")
    return True


async def run(mode: str) -> dict:
    secrets = load_secrets()
    base_url, token = resolve_connection(secrets)

    reading_date = stan = session_state = None
    if mode == "normal":
        reading_date, stan, session_state = get_reading()

    async with aiohttp.ClientSession() as http_session:
        async with http_session.ws_connect(base_url + "/api/websocket",
                                           max_msg_size=32 * 1024 * 1024) as ws:
            hello = await ws.receive_json()
            if hello.get("type") != "auth_required":
                raise RuntimeError(f"unexpected hello: {hello}")
            await ws.send_json({"type": "auth", "access_token": token})
            auth = await ws.receive_json()
            if auth.get("type") != "auth_ok":
                raise RuntimeError(f"auth failed: {auth}")

            api = Api(ws)

            if mode == "rebuild":
                await api.clear(STAT_ID)
                await api.clear(COST_STAT_ID)

            consumption = {}
            if mode != "rebuild-cost":
                consumption = await update_consumption(api, mode, reading_date, stan)

            cost = await update_cost(api, rebuild=(mode == "rebuild-cost"))
            wired = await ensure_cost_wired(api)

            return {
                "status": "ok",
                "session": session_state,
                **consumption,
                **cost,
                "cost_source_wired": wired,
            }


def main() -> None:
    args = sys.argv[1:]
    # Check --rebuild-cost before --rebuild: the latter is a prefix of it.
    if "--rebuild-cost" in args:
        mode = "rebuild-cost"
    elif "--rebuild" in args:
        mode = "rebuild"
    elif "--seed" in args:
        mode = "seed"
    else:
        mode = "normal"
    print(json.dumps(asyncio.run(run(mode)), ensure_ascii=False))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # Exit 0 on purpose: command_line discards stdout on a non-zero exit,
        # which would hide this message instead of surfacing it as the sensor
        # state plus its "error" attribute.
        print(json.dumps({"status": "error", "error": str(e)}, ensure_ascii=False))
        sys.exit(0)
