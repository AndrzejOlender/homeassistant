"""Aqara Vibration Sensor T1 (DJT12LM) - lumi.vibration.agl01.

Community quirk from https://github.com/zigpy/zha-device-handlers/issues/4137
(comment by nachtaap, 2026-01-31). Upstream PR (not yet merged):
https://github.com/zigpy/zha-device-handlers/pull/4972

Built with zhaquirks.builder.QuirkBuilder (the replacement for the old
signature/replacement dict style, which is deprecated in zha-quirks 2.2.2).

Protocol details cross-checked 2026-09-17 against zigbee-herdsman-converters'
own device definition and shared lumi library (Koenkk/zigbee-herdsman-converters,
`src/devices/lumi.ts` model DJT12LM, `src/lib/lumi.ts` lumiVibration /
lumiSensitivityAdjustment / lumiReportInterval):
- Vibration: cluster 'manuSpecificLumi' (0xFCC0), attribute 0x0118, endpoint 2.
  Z2M calls this event "movement" - same attribute, different label; kept as
  "vibration" here since existing automations already key off that name.
- Triple-tap: cluster 'genMultistateInput', presentValue 1, endpoint 2. Z2M
  calls this "triple_strike".
- Shake: standard 'ssIasZone' cluster, NON-standard attribute 45, value 1.
  NOT independently verified against a live device in this house - sourced
  only from Z2M's converter. If it never fires, or fires on the wrong
  physical trigger, this is the first place to check. Wired on both
  endpoint 1 and 2 (unverified which one the device actually uses).
- Sensitivity: cluster 'manuSpecificLumi', attribute 0x010E, endpoint 2,
  manufacturer code 0x115F (4447), values 1=high, 2=medium, 3=low. Write-only.
- Report interval: cluster 'manuSpecificLumi', attribute 0x0110, endpoint 2,
  same manufacturer code, values 1=1s, 2=5s, 3=10s. Also write-only.

Delivery of those two config writes is the hard part. This is a battery
"sleepy end device": no Poll Control cluster, radio off except just after it
transmits, and a parent may only hold a message for it for ~7.68 s. A write
issued at an arbitrary moment therefore fails with
`zigpy.exceptions.DeliveryError: ZIGBEE_NO_APS_ACK` essentially every time.

zigbee-herdsman (Zigbee2MQTT) solves this and zigpy has no equivalent, so the
mechanism is reimplemented here (see VibrationAGL01Device):
- `Endpoint.sendRequest` catches a failed transaction and queues the request
  instead of dropping it ("the device is likely sleeping").
- `Device.implicitCheckin()` flushes that queue whenever the device sends
  anything, i.e. while its radio is briefly awake.
- The queue entry lives for one check-in interval; Z2M's definition for this
  model sets `quirkCheckinInterval("1_HOUR")`, mirrored by PENDING_WRITE_TTL.
- Z2M reports success to the UI as soon as a write is queued, so the value
  appears set immediately; the same is done here via _update_attribute().
"""

from __future__ import annotations

import asyncio
import dataclasses
import logging
import time
from typing import Any, Final

import zigpy.types as t
from zigpy.exceptions import DeliveryError
from zigpy.typing import UNDEFINED, UndefinedType
from zigpy.zcl import foundation
from zigpy.zcl.clusters.general import MultistateInput
from zigpy.zcl.clusters.security import IasZone
from zigpy.zcl.foundation import ZCLAttributeDef

from zhaquirks import EventableCluster
from zhaquirks.builder import QuirkBuilder
from zhaquirks.clusters import CustomCluster
from zhaquirks.const import ZHA_SEND_EVENT
from zhaquirks.device import CustomZigpyDevice
from zhaquirks.xiaomi import (
    LUMI,
    BasicCluster,
    XiaomiAqaraE1Cluster,
    XiaomiPowerConfiguration,
)

# Cluster.debug()/info() log under the `zigpy.zcl` logger, so they are invisible
# with `logger: default: error`. Use a module logger instead - custom quirks are
# imported under their bare filename, so this is `vibration_agl01` and can be
# raised at runtime with:
#   hass-cli service call logger.set_level --arguments vibration_agl01=debug
_LOGGER = logging.getLogger(__name__)

# Event / action names
VIBRATION = "vibration"
TRIPLE_TAP = "triple_tap"
SHAKE = "shake"

# Xiaomi manufacturer attribute IDs (cluster 'manuSpecificLumi', 0xFCC0, endpoint 2)
XIAOMI_VIBRATION_ATTR = 0x0118  # Decimal 280
XIAOMI_SENSITIVITY_ATTR = 0x010E  # Decimal 270, write-only
XIAOMI_REPORT_INTERVAL_ATTR = 0x0110  # Decimal 272, write-only

# Non-standard attribute on the standard IasZone cluster (0x0500) - see
# module docstring re: "shake", unverified.
SHAKE_OR_STRIKE_ATTR = 45

# Manufacturer code required to read/write manuSpecificLumi attributes.
LUMI_MANUFACTURER_CODE = 0x115F  # 4447

# Mirrors Z2M's quirkCheckinInterval("1_HOUR") -> pendingRequestTimeout.
PENDING_WRITE_TTL: Final = 3600.0  # seconds

# One shot per wake window: zigpy's default for an end device is retries=2 with
# an 8 s bellows timeout each, which would burn ~24 s of a window that is over
# in about a second, and the blind retries land in the same dead window anyway.
# A miss is retried on the device's *next* wake instead.
FLUSH_RETRIES: Final = 0
FLUSH_PRIORITY: Final = t.PacketPriority.HIGH

# zigpy hard-codes a 28 s reply timeout for end devices (APS_REPLY_TIMEOUT_EXTENDED,
# device.py), overwriting any timeout passed in - so the flush imposes its own from
# the outside. The wake window is about a second; waiting 28 s would only hold the
# single-flight guard shut through every later packet of the same wake burst.
# An awake device answers in well under a second. Applied to the first attempt too,
# so clicking the select fails over to the queue in seconds instead of hanging 28 s
# (long enough that the HTTP call in front of it can time out first).
WRITE_TIMEOUT: Final = 5

# A failed write means two very different things, and telling them apart is what
# makes this work at all (confirmed from raw frames, 2026-09-17):
#
# - DeliveryError (ZIGBEE_NO_APS_ACK): the frame never reached the device. It is
#   asleep. Queue it and retry on its next wake.
# - TimeoutError: zigpy.device.request only starts waiting for the reply *after*
#   send_request() returned, i.e. after the APS acknowledgement - so the frame WAS
#   delivered. This device simply never answers a manufacturer-specific write with
#   a Write Attributes Response; the write is applied silently. Treat as success.
#
# Waiting for a response that this hardware never sends is what made every earlier
# attempt look like a failure.


class SensitivityAdjustment(t.enum8):
    """Values for XIAOMI_SENSITIVITY_ATTR."""

    High = 1
    Medium = 2
    Low = 3


class ReportInterval(t.enum8):
    """Values for XIAOMI_REPORT_INTERVAL_ATTR."""

    OneSecond = 1
    FiveSeconds = 2
    TenSeconds = 3


@dataclasses.dataclass(slots=True)
class PendingWrite:
    """One attribute write waiting for the device to wake up."""

    attr_def: ZCLAttributeDef
    value: Any
    manufacturer: int | UndefinedType | None
    generation: int
    queued_at: float
    expires_at: float
    attempts: int = 0


# (endpoint_id, cluster_id, attribute_id)
PendingKey = tuple[int, int, int]


class VibrationAGL01Device(CustomZigpyDevice):
    """Device that retries failed writes the next time the sensor wakes up.

    zigpy/ZHA equivalent of zigbee-herdsman's `Endpoint.pendingRequests` plus
    `Device.implicitCheckin()`.

    Must subclass CustomZigpyDevice, not BaseCustomDevice: the latter leaves
    `replacement` empty, which would build a device with zero endpoints.
    """

    def __init__(self, application, ieee, nwk, replaces) -> None:
        # Set up before super(), which builds the endpoints and clusters.
        self._pending_writes: dict[PendingKey, PendingWrite] = {}
        self._pending_generation: int = 0
        self._flush_in_progress: bool = False
        super().__init__(application, ieee, nwk, replaces)

    # --- wake hook (Z2M: Device.implicitCheckin) ---

    def packet_received(self, packet: t.ZigbeePacket) -> None:
        # Always dispatch first: vibration / triple_tap events must fire even
        # if everything below is broken.
        super().packet_received(packet)

        try:
            if not self._pending_writes or self._flush_in_progress:
                return
            if self.initializing or self.reinterviewing:
                return
            _LOGGER.debug("scheduling flush of %d pending write(s)", len(self._pending_writes))
            self.create_task(self._flush_pending_writes(), name="flush_pending_writes")
        except Exception:  # noqa: BLE001 - must never break packet intake
            _LOGGER.debug("Failed to schedule pending write flush", exc_info=True)

    # --- queue management ---

    def queue_pending_write(
        self,
        cluster,
        attr_def: ZCLAttributeDef,
        value: Any,
        manufacturer: int | UndefinedType | None,
    ) -> None:
        """Queue (or supersede) a write for delivery on the next wake."""
        key: PendingKey = (cluster.endpoint.endpoint_id, cluster.cluster_id, attr_def.id)
        now = time.monotonic()
        self._expire_pending_writes(now)

        previous = self._pending_writes.get(key)
        self._pending_generation += 1
        self._pending_writes[key] = PendingWrite(
            attr_def=attr_def,
            value=value,
            manufacturer=manufacturer,
            generation=self._pending_generation,
            queued_at=now,
            expires_at=now + PENDING_WRITE_TTL,
        )
        _LOGGER.info(
            "%s: queued %s=%s for delivery on next wake (TTL %.0f min)%s",
            self.ieee,
            attr_def.name,
            value,
            PENDING_WRITE_TTL / 60,
            f", superseding pending {previous.value!r}" if previous else "",
        )

    def drop_pending_writes(self, keys) -> None:
        """Drop queued writes made obsolete by a write that just succeeded."""
        for key in keys:
            if self._pending_writes.pop(key, None) is not None:
                _LOGGER.debug("%s: dropped superseded pending write %r", self.ieee, key)

    def _expire_pending_writes(self, now: float) -> None:
        for key, entry in list(self._pending_writes.items()):
            if entry.expires_at <= now:
                del self._pending_writes[key]
                _LOGGER.warning(
                    "%s: pending write %s=%s expired undelivered after %.0f min (%d attempts)",
                    self.ieee,
                    entry.attr_def.name,
                    entry.value,
                    (now - entry.queued_at) / 60,
                    entry.attempts,
                )

    def _discard_if_unchanged(self, key: PendingKey, entry: PendingWrite) -> None:
        """Remove an entry only if it was not superseded while in flight."""
        current = self._pending_writes.get(key)
        if current is not None and current.generation == entry.generation:
            del self._pending_writes[key]

    # --- flush (Z2M: Endpoint.sendPendingRequests) ---

    async def _flush_pending_writes(self) -> None:
        if self._flush_in_progress:
            return
        self._flush_in_progress = True  # set before the first await
        try:
            now = time.monotonic()
            self._expire_pending_writes(now)
            if not self._pending_writes:
                return

            # Group so attributes sharing a cluster go out in one ZCL frame.
            groups: dict[tuple, list[tuple[PendingKey, PendingWrite]]] = {}
            for key, entry in self._pending_writes.items():
                groups.setdefault((key[0], key[1], entry.manufacturer), []).append(
                    (key, entry)
                )

            for (ep_id, cluster_id, manufacturer), items in groups.items():
                try:
                    cluster = self.endpoints[ep_id].in_clusters[cluster_id]
                except KeyError:
                    for key, entry in items:
                        self._discard_if_unchanged(key, entry)
                    continue

                attributes = {e.attr_def.name: e.value for _, e in items}
                for _, entry in items:
                    entry.attempts += 1

                try:
                    async with asyncio.timeout(WRITE_TIMEOUT):
                        result = await cluster.write_attributes_no_queue(
                            attributes,
                            manufacturer=manufacturer,
                            retries=FLUSH_RETRIES,
                            priority=FLUSH_PRIORITY,
                        )
                except DeliveryError as err:
                    # Never left the coordinator: still asleep. Stay queued, and
                    # do not extend the deadline.
                    _LOGGER.info(
                        "%s: flush of %s not delivered (%s), staying queued",
                        self.ieee,
                        attributes,
                        err,
                    )
                    continue
                except TimeoutError:
                    # APS-acked, so it arrived; this device just never answers a
                    # manufacturer-specific write. Done.
                    _LOGGER.info(
                        "%s: DELIVERED queued write %s after %.0fs and %d attempt(s)"
                        " (no response expected from this device)",
                        self.ieee,
                        attributes,
                        time.monotonic() - items[0][1].queued_at,
                        items[0][1].attempts,
                    )
                    # Best moment there is to check whether it stuck: the device
                    # just took delivery, so it is demonstrably awake.
                    cluster.schedule_read_back(
                        [e.attr_def.id for _, e in items], manufacturer
                    )
                    for key, entry in items:
                        self._discard_if_unchanged(key, entry)
                    continue
                except Exception:  # noqa: BLE001 - never let one entry poison the queue
                    _LOGGER.exception(
                        "%s: unexpected error flushing %s, dropping",
                        self.ieee,
                        attributes,
                    )
                    for key, entry in items:
                        self._discard_if_unchanged(key, entry)
                    continue

                statuses = {r.attrid: r.status for r in result[0]}
                for key, entry in items:
                    status = statuses.get(entry.attr_def.id)
                    if status == foundation.Status.SUCCESS:
                        _LOGGER.info(
                            "%s: DELIVERED queued write %s=%s after %.0fs and %d attempt(s)",
                            self.ieee,
                            entry.attr_def.name,
                            entry.value,
                            time.monotonic() - entry.queued_at,
                            entry.attempts,
                        )
                    else:
                        # It arrived and was refused - retrying for an hour
                        # would only hide a real problem.
                        _LOGGER.warning(
                            "%s: device rejected queued write %s=%s: %s (dropping)",
                            self.ieee,
                            entry.attr_def.name,
                            entry.value,
                            status,
                        )
                    self._discard_if_unchanged(key, entry)
        finally:
            self._flush_in_progress = False


class XiaomiVibrationCluster(XiaomiAqaraE1Cluster):
    """Xiaomi manufacturer cluster on endpoint 2: vibration, sensitivity, report interval."""

    # Only these may be queued on failure; anything else keeps raising.
    QUEUEABLE_ATTRIBUTE_IDS: Final = frozenset(
        {XIAOMI_SENSITIVITY_ATTR, XIAOMI_REPORT_INTERVAL_ATTR}
    )

    class AttributeDefs(XiaomiAqaraE1Cluster.AttributeDefs):
        """Manufacturer-specific attributes used by this device."""

        vibration_detected: Final = ZCLAttributeDef(
            id=XIAOMI_VIBRATION_ATTR,
            type=t.uint8_t,
            access="rp",
            manufacturer_code=LUMI_MANUFACTURER_CODE,
        )
        sensitivity_adjustment: Final = ZCLAttributeDef(
            id=XIAOMI_SENSITIVITY_ATTR,
            type=SensitivityAdjustment,
            access="w",
            manufacturer_code=LUMI_MANUFACTURER_CODE,
        )
        report_interval: Final = ZCLAttributeDef(
            id=XIAOMI_REPORT_INTERVAL_ATTR,
            type=ReportInterval,
            access="w",
            manufacturer_code=LUMI_MANUFACTURER_CODE,
        )

    def _update_attribute(self, attrid, value):
        """Parse Xiaomi manufacturer attributes for vibration."""
        super()._update_attribute(attrid, value)

        self.debug(f"XiaomiVibrationCluster: attribute {attrid:#06x} = {value}")

        if attrid == self.AttributeDefs.vibration_detected.id and value == 1:
            self.info("Vibration detected via Xiaomi attribute 0x0118")
            self.listener_event(ZHA_SEND_EVENT, VIBRATION, {"value": value})

    async def write_attributes_no_queue(
        self, attributes, manufacturer=UNDEFINED, *, update_cache: bool = True, **kwargs
    ):
        """Write without the queue-on-failure fallback. Used by the flush."""
        return await super().write_attributes(
            attributes, manufacturer=manufacturer, update_cache=update_cache, **kwargs
        )

    async def write_attributes(
        self, attributes, manufacturer=UNDEFINED, *, update_cache: bool = True, **kwargs
    ):
        """Write; if the device is asleep, queue for its next wake."""
        try:
            async with asyncio.timeout(WRITE_TIMEOUT):
                result = await super().write_attributes(
                    attributes,
                    manufacturer=manufacturer,
                    update_cache=update_cache,
                    **kwargs,
                )
        except DeliveryError as err:
            # Never reached the device: it is asleep. Queue for the next wake.
            queued = self._queue_failed_write(
                attributes, manufacturer, update_cache, err
            )
            if queued is None:
                raise
            return queued
        except TimeoutError:
            # Delivered, but this device never sends a Write Attributes Response.
            accepted = self._accept_silent_write(attributes, manufacturer, update_cache)
            if accepted is None:
                raise
            return accepted
        else:
            self._drop_superseded_pending(attributes, manufacturer)
            return result

    def _resolve(self, attributes, manufacturer):
        """Resolve attribute defs the same way zigpy's write_attributes does."""
        return [
            (self.find_attribute(attr, manufacturer_code=manufacturer), value)
            for attr, value in attributes.items()
        ]

    def _drop_superseded_pending(self, attributes, manufacturer) -> None:
        device = self.endpoint.device
        if not hasattr(device, "drop_pending_writes"):
            return
        try:
            resolved = self._resolve(attributes, manufacturer)
        except (KeyError, TypeError):
            return
        device.drop_pending_writes(
            (self.endpoint.endpoint_id, self.cluster_id, attr_def.id)
            for attr_def, _ in resolved
        )

    def _prepare_queueable(self, attributes, manufacturer):
        """Resolve and coerce a batch, or None if it must not be intercepted.

        All-or-nothing: a batch touching anything outside the two write-only
        config attributes keeps its original failure behaviour.
        """
        try:
            resolved = self._resolve(attributes, manufacturer)
        except (KeyError, TypeError):
            return None
        if not resolved:
            return None
        if any(d.id not in self.QUEUEABLE_ATTRIBUTE_IDS for d, _ in resolved):
            return None
        try:
            return [(d, d.type(v)) for d, v in resolved]
        except (ValueError, TypeError):
            return None

    def _success_records(self, coerced, update_cache):
        """Fake the SUCCESS records zigpy would have returned, updating the cache."""
        records = []
        for attr_def, value in coerced:
            if update_cache:
                # The select entity reads its value from the attribute cache, so a
                # SUCCESS record alone would leave it showing "unknown".
                self._update_attribute(attr_def.id, value)
            records.append(
                foundation.WriteAttributesStatusRecord(
                    status=foundation.Status.SUCCESS, attrid=attr_def.id
                )
            )
        return [records]

    def _accept_silent_write(self, attributes, manufacturer, update_cache):
        """Accept a delivered-but-unanswered write, or None to re-raise."""
        coerced = self._prepare_queueable(attributes, manufacturer)
        if coerced is None:
            return None

        _LOGGER.info(
            "%s: %s delivered; no Write Attributes Response (normal for this device), accepting",
            self.endpoint.device.ieee,
            {d.name: v for d, v in coerced},
        )
        # It is applied now, so any older queued copy is obsolete.
        self._drop_superseded_pending(attributes, manufacturer)
        self.schedule_read_back([d.id for d, _ in coerced], manufacturer)
        return self._success_records(coerced, update_cache)

    def schedule_read_back(self, attr_ids, manufacturer) -> None:
        """Read the attributes back while the device is still awake.

        The write is never acknowledged, so this is the only way to find out
        whether the device actually stored the value. Runs as a background task
        so it never delays the write path, and is best-effort by design.
        """
        device = self.endpoint.device
        try:
            device.create_task(
                self._read_back(attr_ids, manufacturer), name="verify_write"
            )
        except Exception:  # noqa: BLE001 - diagnostics must never break a write
            _LOGGER.debug("Could not schedule read-back", exc_info=True)

    async def _read_back(self, attr_ids, manufacturer) -> None:
        try:
            async with asyncio.timeout(WRITE_TIMEOUT):
                success, failure = await self.read_attributes(
                    attr_ids,
                    allow_cache=False,
                    only_cache=False,
                    manufacturer=manufacturer,
                    retries=FLUSH_RETRIES,
                    priority=FLUSH_PRIORITY,
                )
        except (DeliveryError, TimeoutError) as err:
            _LOGGER.info(
                "%s: read-back of %s unanswered (%s) - this device does not answer"
                " reads either, so the write cannot be confirmed from software",
                self.endpoint.device.ieee,
                attr_ids,
                err if str(err) else type(err).__name__,
            )
        except Exception:  # noqa: BLE001
            _LOGGER.exception(
                "%s: read-back of %s failed unexpectedly",
                self.endpoint.device.ieee,
                attr_ids,
            )
        else:
            _LOGGER.warning(
                "%s: READ-BACK answered: success=%s failure=%s",
                self.endpoint.device.ieee,
                success,
                failure,
            )

    def _queue_failed_write(self, attributes, manufacturer, update_cache, err):
        """Queue the batch and fake SUCCESS records, or return None to re-raise."""
        device = self.endpoint.device
        if not hasattr(device, "queue_pending_write"):
            return None

        coerced = self._prepare_queueable(attributes, manufacturer)
        if coerced is None:
            return None

        _LOGGER.info(
            "%s: write of %s failed (%s); device is asleep, queueing",
            device.ieee,
            list(attributes),
            err if str(err) else type(err).__name__,
        )

        for attr_def, value in coerced:
            device.queue_pending_write(self, attr_def, value, manufacturer)
        # Optimistic UI, as Z2M does: report success as soon as it is queued.
        return self._success_records(coerced, update_cache)


class VibrationMultistateInput(EventableCluster, MultistateInput):
    """Multistate input for triple-tap detection.

    From Z2M logs: cluster 'genMultistateInput', data '{"presentValue":1}' from endpoint 2
    """

    def _update_attribute(self, attrid, value):
        """Process MultistateInput for triple-tap."""
        super()._update_attribute(attrid, value)

        self.debug(f"MultistateInput: attribute {attrid:#06x} = {value}")

        if attrid == MultistateInput.AttributeDefs.present_value.id and value == 1:
            self.info("Triple-tap detected")
            self.listener_event(ZHA_SEND_EVENT, TRIPLE_TAP, {"value": value})


class VibrationIasZone(CustomCluster, IasZone):
    """Standard IasZone cluster, repurposed for this device's non-standard
    attribute 45 report (shake / a second triple-strike path).

    Unverified against a live device - see module docstring.
    """

    class AttributeDefs(IasZone.AttributeDefs):
        shake_or_strike: Final = ZCLAttributeDef(
            id=SHAKE_OR_STRIKE_ATTR,
            type=t.uint8_t,
            access="rp",
            manufacturer_code=None,
        )

    _SHAKE_LOOKUP = {1: SHAKE, 2: TRIPLE_TAP}

    def _update_attribute(self, attrid, value):
        super()._update_attribute(attrid, value)

        if attrid == self.AttributeDefs.shake_or_strike.id and value in self._SHAKE_LOOKUP:
            command = self._SHAKE_LOOKUP[value]
            self.info(f"{command!r} detected via IasZone attribute 45")
            self.listener_event(ZHA_SEND_EVENT, command, {"value": value})


(
    QuirkBuilder(LUMI, "lumi.vibration.agl01")
    .friendly_name(manufacturer="Aqara", model="Vibration Sensor T1")
    .zigpy_device_class(VibrationAGL01Device)
    .replaces(BasicCluster, endpoint_id=1)
    .replaces(XiaomiPowerConfiguration, endpoint_id=1)
    # The device also reports on the Lumi manufacturer cluster from endpoint 1
    # (attribute 0x00F7 carries battery voltage and friends). Without this,
    # zigpy logs "Ignoring message on unknown cluster: 0xfcc0" and drops them.
    # It carries the full cluster class, not the plain base, because the config
    # writes below target endpoint 1 - see the note on those.
    .replaces(XiaomiVibrationCluster, endpoint_id=1)
    .replaces(VibrationIasZone, endpoint_id=1)
    .replaces(VibrationMultistateInput, endpoint_id=2)
    .replaces(XiaomiVibrationCluster, endpoint_id=2)
    .replaces(VibrationIasZone, endpoint_id=2)
    # Endpoint 2 by convention (the community quirk's choice). Tested 2026-09-17:
    # endpoint 1 - which is what Zigbee2MQTT's determineEndpoint() would pick,
    # being the first endpoint advertising 0xFCC0 - behaves identically, so the
    # endpoint is not what stops these writes from taking effect.
    .enum(
        XiaomiVibrationCluster.AttributeDefs.sensitivity_adjustment.name,
        SensitivityAdjustment,
        XiaomiVibrationCluster.cluster_id,
        endpoint_id=2,
        translation_key="sensitivity_adjustment",
        fallback_name="Sensitivity",
    )
    .enum(
        XiaomiVibrationCluster.AttributeDefs.report_interval.name,
        ReportInterval,
        XiaomiVibrationCluster.cluster_id,
        endpoint_id=2,
        translation_key="report_interval",
        fallback_name="Report interval",
    )
    .device_automation_triggers({
        (VIBRATION, VIBRATION): {"type": VIBRATION, "subtype": VIBRATION},
        (TRIPLE_TAP, TRIPLE_TAP): {"type": TRIPLE_TAP, "subtype": TRIPLE_TAP},
        (SHAKE, SHAKE): {"type": SHAKE, "subtype": SHAKE},
    })
    .add_to_registry()
)
