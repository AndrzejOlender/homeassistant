#!/usr/bin/env python3
"""
Tauron G12W cost statistic updater for Home Assistant.

Reads the Tauron grid consumption external statistic (whatever the Energy
dashboard currently points at), and for every complete day it hasn't
processed yet, multiplies each hour's consumption by the G12W day/night
rate applicable to that hour, then imports the running total as its own
external cost statistic (tauron_g12w:cost). That statistic is wired into
the Energy dashboard via stat_cost, because external statistics cannot use
entity_energy_price/number_energy_price - HA rejects that combination.

Rates are read live from input_number.tauron_g12w_day_rate / _night_rate,
so they stay editable from the UI. The fixed monthly charge
(input_number.tauron_g12w_monthly_fee) is spread evenly across the days of
each month, so the resulting statistic is a bill estimate, not pure energy
cost.

NOTE: the same G12W zone schedule is also implemented in the template sensor
"Tauron G12W Price" in config/template.yaml (for live display). If the tariff
hours ever change, update zone_rate() here AND that template, or the displayed
price will silently disagree with the billed cost.

Idempotent: safe to run repeatedly. Only days strictly after the last
imported point are processed, and a day is skipped until its hourly rows
cover the whole day (so partial/laggy days are never priced).

Usage:
  tauron_g12w_cost.py              normal incremental run (used by command_line)
  tauron_g12w_cost.py --rebuild    DESTRUCTIVE: wipe tauron_g12w:cost and
                                   recompute all history at current rates.
                                   Use after correcting the rate helpers.
"""
import asyncio
import calendar
import json
import os
import sys
from datetime import datetime, timedelta, timezone
from zoneinfo import ZoneInfo

import yaml

try:
    import aiohttp
except ImportError as e:  # pragma: no cover - surfaced via sensor state
    print(json.dumps({"status": "error", "error": f"missing dependency: {e}"}))
    sys.exit(0)

TOKEN_KEY = "tauron_g12w_cost_token"
DEFAULT_SECRETS_PATH = "/config/secrets.yaml"

COST_STAT_ID = "tauron_g12w:cost"
COST_SOURCE = "tauron_g12w"
COST_NAME = "Tauron G12W Cost"

DAY_RATE_ENTITY = "input_number.tauron_g12w_day_rate"
NIGHT_RATE_ENTITY = "input_number.tauron_g12w_night_rate"
MONTHLY_FEE_ENTITY = "input_number.tauron_g12w_monthly_fee"

WARSAW = ZoneInfo("Europe/Warsaw")

# Cap work per run so a large backlog (e.g. after --rebuild) drains over
# successive runs instead of blowing through the command_line timeout.
MAX_DAYS_PER_RUN = 40


def resolve_connection() -> tuple[str, str]:
    """Return (base_url, token). Prefers HASS_SERVER/HASS_TOKEN env (manual
    runs); falls back to secrets.yaml + localhost (in-container runs)."""
    env_server = os.environ.get("HASS_SERVER")
    env_token = os.environ.get("HASS_TOKEN")
    if env_server and env_token:
        return env_server.rstrip("/"), env_token

    secrets_path = os.environ.get("HA_SECRETS_PATH", DEFAULT_SECRETS_PATH)
    with open(secrets_path) as f:
        secrets = yaml.safe_load(f)
    token = secrets.get(TOKEN_KEY)
    if not token:
        raise RuntimeError(f"{TOKEN_KEY} missing from {secrets_path}")
    return "http://localhost:8123", token


def zone_rate(dt_utc: datetime, day_rate: float, night_rate: float) -> float:
    """G12W: weekends entirely night rate; weekdays day rate 6-13 and 15-22."""
    local = dt_utc.astimezone(WARSAW)
    if local.isoweekday() >= 6:
        return night_rate
    h = local.hour
    if (6 <= h < 13) or (15 <= h < 22):
        return day_rate
    return night_rate


async def send(ws, msg_id: int, frame: dict) -> dict:
    frame = dict(frame)
    frame["id"] = msg_id
    await ws.send_json(frame)
    return await ws.receive_json()


async def run(rebuild: bool) -> dict:
    base_url, token = resolve_connection()
    ws_url = base_url + "/api/websocket"

    async with aiohttp.ClientSession() as session:
        async with session.ws_connect(ws_url, max_msg_size=16 * 1024 * 1024) as ws:
            hello = await ws.receive_json()
            if hello.get("type") != "auth_required":
                raise RuntimeError(f"unexpected hello: {hello}")
            await ws.send_json({"type": "auth", "access_token": token})
            auth = await ws.receive_json()
            if auth.get("type") != "auth_ok":
                raise RuntimeError(f"auth failed: {auth}")

            mid = 1

            prefs = await send(ws, mid, {"type": "energy/get_prefs"})
            mid += 1
            grid_source = None
            for src in prefs["result"]["energy_sources"]:
                if src.get("type") == "grid" and src.get("stat_energy_from"):
                    grid_source = src
                    break
            if grid_source is None:
                raise RuntimeError("no grid source with stat_energy_from in energy prefs")
            grid_stat_id = grid_source["stat_energy_from"]

            states = await send(ws, mid, {"type": "get_states"})
            mid += 1
            state_by_id = {s["entity_id"]: s for s in states["result"]}
            try:
                day_rate = float(state_by_id[DAY_RATE_ENTITY]["state"])
                night_rate = float(state_by_id[NIGHT_RATE_ENTITY]["state"])
                monthly_fee = float(state_by_id[MONTHLY_FEE_ENTITY]["state"])
            except (KeyError, ValueError) as e:
                raise RuntimeError(f"could not read rate helpers: {e}")
            if day_rate <= 0 or night_rate <= 0:
                raise RuntimeError(f"rate helpers not set (day={day_rate}, night={night_rate})")

            if rebuild:
                cleared = await send(ws, mid, {
                    "type": "recorder/clear_statistics",
                    "statistic_ids": [COST_STAT_ID],
                })
                mid += 1
                if not cleared.get("success", True):
                    raise RuntimeError(f"clear_statistics failed: {cleared}")

            now = datetime.now(timezone.utc)
            far_back = now - timedelta(days=400)

            existing_rows = []
            if not rebuild:
                existing = await send(ws, mid, {
                    "type": "recorder/statistics_during_period",
                    "start_time": far_back.isoformat(),
                    "end_time": now.isoformat(),
                    "statistic_ids": [COST_STAT_ID],
                    "period": "hour",
                })
                mid += 1
                existing_rows = existing.get("result", {}).get(COST_STAT_ID, [])

            running_sum = existing_rows[-1]["sum"] if existing_rows else 0.0
            last_done_end = None
            if existing_rows:
                last_start = datetime.fromtimestamp(existing_rows[-1]["start"] / 1000, tz=timezone.utc)
                last_done_end = last_start + timedelta(hours=1)

            daily = await send(ws, mid, {
                "type": "recorder/statistics_during_period",
                "start_time": far_back.isoformat(),
                "end_time": now.isoformat(),
                "statistic_ids": [grid_stat_id],
                "period": "day",
            })
            mid += 1
            daily_rows = daily.get("result", {}).get(grid_stat_id, [])

            new_points = []
            processed_days = []
            skipped_incomplete = []
            verified = None
            for day in daily_rows:
                if len(processed_days) >= MAX_DAYS_PER_RUN:
                    break

                day_start = datetime.fromtimestamp(day["start"] / 1000, tz=timezone.utc)
                day_end = datetime.fromtimestamp(day["end"] / 1000, tz=timezone.utc)
                if last_done_end and day_start < last_done_end:
                    continue

                local_day = day_start.astimezone(WARSAW).date().isoformat()
                # A local day is 23h on spring-forward and 25h on fall-back, so
                # derive the expected hour count from the bucket span rather than
                # assuming 24 - otherwise the DST day is skipped forever.
                expected_hours = round((day_end - day_start).total_seconds() / 3600)

                hourly = await send(ws, mid, {
                    "type": "recorder/statistics_during_period",
                    "start_time": day_start.isoformat(),
                    "end_time": day_end.isoformat(),
                    "statistic_ids": [grid_stat_id],
                    "period": "hour",
                })
                mid += 1
                hrows = hourly.get("result", {}).get(grid_stat_id, [])
                if len(hrows) < expected_hours:
                    skipped_incomplete.append(local_day)
                    continue
                if any(hr.get("change") is None for hr in hrows):
                    skipped_incomplete.append(local_day)
                    continue

                # Spread the fixed monthly charge evenly over this month's days,
                # then over this day's actual hours (23/24/25 across DST).
                local_date = day_start.astimezone(WARSAW).date()
                days_in_month = calendar.monthrange(local_date.year, local_date.month)[1]
                per_hour_fee = (monthly_fee / days_in_month) / len(hrows)

                for hr in hrows:
                    hstart = datetime.fromtimestamp(hr["start"] / 1000, tz=timezone.utc)
                    running_sum += hr["change"] * zone_rate(hstart, day_rate, night_rate)
                    running_sum += per_hour_fee
                    new_points.append({"start": hstart.isoformat(), "sum": round(running_sum, 4)})
                processed_days.append(local_day)

            if new_points:
                import_result = await send(ws, mid, {
                    "type": "recorder/import_statistics",
                    "metadata": {
                        "has_mean": False,
                        "has_sum": True,
                        "name": COST_NAME,
                        "source": COST_SOURCE,
                        "statistic_id": COST_STAT_ID,
                        "unit_of_measurement": "PLN",
                    },
                    "stats": new_points,
                })
                mid += 1
                if not import_result.get("success", True):
                    raise RuntimeError(f"import_statistics failed: {import_result}")

                # The recorder writes statistics asynchronously, so the ack above
                # only means "queued". Confirm the rows actually landed: otherwise
                # a lost write stays silent, and the next run reads an empty stat
                # and redoes all the work from zero.
                expected_last_ms = datetime.fromisoformat(new_points[-1]["start"]).timestamp() * 1000
                for _ in range(15):
                    await asyncio.sleep(1)
                    check = await send(ws, mid, {
                        "type": "recorder/statistics_during_period",
                        "start_time": far_back.isoformat(),
                        "end_time": now.isoformat(),
                        "statistic_ids": [COST_STAT_ID],
                        "period": "hour",
                    })
                    mid += 1
                    check_rows = check.get("result", {}).get(COST_STAT_ID, [])
                    if check_rows and max(r["start"] for r in check_rows) >= expected_last_ms:
                        verified = True
                        break
                else:
                    raise RuntimeError(
                        f"imported {len(new_points)} points but they did not appear "
                        f"in {COST_STAT_ID} within 15s"
                    )

            if grid_source.get("stat_cost") != COST_STAT_ID:
                grid_source["stat_cost"] = COST_STAT_ID
                save_frame = dict(prefs["result"])
                save_frame["type"] = "energy/save_prefs"
                save_result = await send(ws, mid, save_frame)
                mid += 1
                if not save_result.get("success", True):
                    raise RuntimeError(f"save_prefs failed: {save_result}")

            return {
                "status": "ok",
                "processed_days": processed_days,
                "skipped_incomplete": skipped_incomplete,
                "hours_imported": len(new_points),
                "import_verified": verified,
                "running_total_pln": round(running_sum, 2),
                "day_rate": day_rate,
                "night_rate": night_rate,
                "monthly_fee": monthly_fee,
            }


def main() -> None:
    rebuild = "--rebuild" in sys.argv[1:]
    print(json.dumps(asyncio.run(run(rebuild))))


if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        # Exit 0 on purpose: command_line discards stdout on a non-zero exit,
        # which would hide this message instead of surfacing it as the sensor
        # state plus its "error" attribute.
        print(json.dumps({"status": "error", "error": str(e)}))
        sys.exit(0)
