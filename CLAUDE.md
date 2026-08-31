# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

Home Assistant configuration repository for a smart home running on a Kubernetes cluster (Intel NUC, Ubuntu Server). Home Assistant version is tracked in `.HA_VERSION`. Deployed via Helm charts from a separate infrastructure repo (`https://gitlab.olender.io/andrzej/infrastructure`).

- External URL: `https://home.olender.me`
- Internal URL: `http://192.168.1.230:8123`

**This is a pure configuration repo — there are no build, test, or lint commands.** Code lives in `scripts/`: `sui_wallet.py` and `clean-dotfiles.sh` are stdlib/dep-free; `tauron_g12w_cost.py` depends on `pyyaml` and `aiohttp`.

## Architecture

### Config Structure

`configuration.yaml` is the root config and loads everything via `!include` directives:

- `config/automation/` — automations loaded via `!include_dir_merge_list` (each file is a list of automations)
- `config/*.yaml` — individual config domains (homekit, recorder, template, scripts, etc.)
- `ui-lovelace-mushroom.yaml` — main Lovelace dashboard using Mushroom cards
- `secrets.yaml` — all secrets (gitignored), referenced as `!secret key_name`
- `themes/` — UI themes (Google Dark OLED is default)

### Infrastructure Stack

- **PostgreSQL** recorder backend (`postgres-hass.smart-home.svc.cluster.local`)
- **Prometheus** metrics export (namespace: `hass`)
- **Zigbee2MQTT** with TI LAUNCHXL-CC1352P-2 adapter for ZigBee devices
- **MQTT** broker for ZigBee messages
- **HomeKit** bridge (port 21065) + camera (port 21066)
- **Alexa** integration for Echo Dots
- **Sonos** speakers on local network

### Key Entities

| Entity | What |
|--------|------|
| `vacuum.john` | Xiaomi/Roborock vacuum |
| `lock.aqara_smart_lock_u200` | Aqara U200 front door (Matter/Thread) |
| `media_player.office` | Sonos office speaker |
| `media_player.toilet_up` | Sonos toilet speaker |
| `light.desk_led` | Desk LED (adaptive lighting) |
| `person.ania`, `person.gosia`, `person.arsen` | Tracked people |

### Notification System

- iOS push: `notify.mobile_app_iphone`
- TTS: ElevenLabs in Polish via Sonos office speaker
- Triggers: lock state, vacuum, air quality, zones, waste calendar, weather warnings

### Custom Components (gitignored, installed locally)

`adaptive_lighting`, `burze_dzis_net` (Polish storms), `esa_nask` (air quality), `hacs`, `openai_stt`, `openai_tts`, `tauron_amiplus` (energy meter), `xiaomi_cloud_map_extractor`

## Conventions

- Many automation files contain **large blocks of commented-out code** from previous iterations — this is intentional, kept for reference.
- Active automations: `light.yaml`, `music.yaml`, `notification.yaml`, `vacuum.yaml`, `theme.yaml`
- YAML comments and automation aliases are in English; TTS messages and some notification text are in **Polish**.
- Entity customization is in `config/customize.yaml` (icons, device classes).

## Applying Config Changes

After editing YAML config, reload the affected component via `hass-cli` (installed on this host at `/opt/homebrew/bin/hass-cli`). **Never restart Home Assistant** — restart is explicitly excluded. Use targeted reloads only.

| Change | Reload command |
|--------|----------------|
| `config/automation/*.yaml` | `hass-cli service call automation.reload` |
| `config/scripts.yaml` | `hass-cli service call script.reload` |
| `config/template.yaml` | `hass-cli service call template.reload` |
| `config/input_boolean.yaml` | `hass-cli service call input_boolean.reload` |
| `config/homekit.yaml` | `hass-cli service call homekit.reload` |
| `themes/*.yaml` | `hass-cli service call frontend.reload_themes` |
| `configuration.yaml` (core) | `hass-cli service call homeassistant.reload_core_config` |
| Multiple / uncertain | `hass-cli service call homeassistant.reload_all` |

Lovelace dashboards (`ui-lovelace-mushroom.yaml`) reload client-side — tell the user to refresh the browser tab.

If a change genuinely requires a full restart (new integration, custom component swap, Python-level change), **stop and ask the user** — do not run `homeassistant.restart`.

## GitHub Actions

Single workflow: `.github/workflows/build-container-sshd.yaml`
- Triggers on push to `master` with changes in `sshd/`
- Builds and pushes `andrzejolender/sshd` Docker image to DockerHub
- Requires secrets: `DOCKERHUB_USERNAME`, `DOCKERHUB_TOKEN`
