# Home Assistant Configuration Files

Configuration for a Home Assistant instance running on a Kubernetes cluster (Intel NUC, Ubuntu Server), deployed via Helm charts from a separate [infrastructure repo](https://gitlab.olender.io/andrzej/infrastructure). See `CLAUDE.md` for the full technical breakdown (entity IDs, automation conventions, deployment details).

## Platform

* Home Assistant on Kubernetes ([Helm Charts](https://gitlab.olender.io/andrzej/infrastructure/-/tree/master/nuc/helm))
* [PostgreSQL](https://www.home-assistant.io/integrations/recorder/) recorder backend
* [Prometheus](https://www.home-assistant.io/integrations/prometheus/) metrics export

## Zigbee & Matter/Thread

* [ZHA](https://www.home-assistant.io/integrations/zha/) (native Zigbee integration) with a network-attached CC2652P coordinator
* [Matter](https://www.home-assistant.io/integrations/matter/) over [Thread](https://www.home-assistant.io/integrations/thread/), with a self-hosted [OpenThread Border Router](https://www.home-assistant.io/integrations/otbr/) on the cluster
* [Aqara Smart Lock U200](https://www.aqara.com/) (Matter/Thread) on the front door
* Zigbee bulbs, switches and sensors across the house

## Local WiFi Relays

* [Shelly Gen4](https://www.shelly.com/) 1PM/2PM relays (local API, no cloud) driving most wired switches
* [Govee](https://www.govee.com/) lights via the local API integration
* [Adaptive Lighting](https://github.com/basnijholt/adaptive-lighting) for circadian desk lighting

## Media & Entertainment

* LG OLED TV via [webOS](https://www.home-assistant.io/integrations/webostv/) and a dedicated HomeKit bridge
* [Apple TV](https://www.home-assistant.io/integrations/apple_tv/)
* Satellite TV box via DLNA
* [Sonos](https://www.home-assistant.io/integrations/sonos/) multi-room audio, orchestrated through [Music Assistant](https://www.music-assistant.io/), plus Spotify

## Voice & AI

* Local voice pipeline ([Wyoming](https://www.home-assistant.io/integrations/wyoming/)): openWakeWord, faster-whisper, Piper, running on a Home Assistant Voice Preview Edition device
* [ElevenLabs](https://elevenlabs.io/) text-to-speech for Polish announcements
* Google Generative AI conversation agent for Assist
* Home Assistant exposed as an [MCP server](https://www.home-assistant.io/integrations/mcp_server/), so AI assistants (Claude included) can query and control the house directly

## Vacuum

* [Roborock](https://www.home-assistant.io/integrations/roborock/) robot vacuum, with [Xiaomi Cloud Map Extractor](https://github.com/PiotrMachowski/Home-Assistant-custom-components-Xiaomi-Cloud-Map-Extractor) for cleaning maps

## Energy & Utilities

* [Tauron AmiPlus](https://github.com/PiotrMachowski/homeassistant-tauron-amiplus) smart meter integration
* Custom G12W day/night tariff cost tracking (`scripts/tauron_g12w_cost.py`), importing a priced statistic into the Energy dashboard

## Weather & Air Quality

* [Met.no](https://www.home-assistant.io/integrations/met/) weather
* ESA NASK hyperlocal air quality (custom component)
* [Burze.dzis.net](https://github.com/PiotrMachowski/Home-Assistant-custom-components-Burze.dzis.net) Polish storm warnings

## Network & Security

* [UniFi Network](https://www.home-assistant.io/integrations/unifi/) (U6-Pro / U7-Pro-XG access points) and [UniFi Protect](https://www.home-assistant.io/integrations/unifiprotect/) cameras
* [AdGuard Home](https://www.home-assistant.io/integrations/adguard/) for network-wide DNS filtering

## Presence & Access

* iOS and Android companion apps for household members
* [HomeKit](https://www.home-assistant.io/integrations/homekit/) bridge for the Apple ecosystem
* Amazon Alexa (Echo Dot) via [Alexa Media Player](https://github.com/custom-components/alexa_media_player)

## Waste & Household

* Local calendars per waste stream (mixed, plastic/metal, paper, glass, bio, textiles) driving pickup reminders
* Shared shopping list

## Dashboard

* [Lovelace](https://www.home-assistant.io/dashboards/) UI built with [Mushroom cards](https://github.com/piitaya/lovelace-mushroom) (`ui-lovelace-mushroom.yaml`)
* Google Dark OLED theme by default
