"""Python Package for controlling Alexa devices (echo dot, etc) programmatically.

SPDX-License-Identifier: Apache-2.0

Websocket library.

This library is based on MIT code from https://github.com/Apollon77/alexa-remote.

For more details about this api, please refer to the documentation at
https://gitlab.com/keatontaylor/alexapy
"""
import asyncio
import base64
import math
import random
import time
import uuid
import json
import datetime
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding

import logging
from alexapy.aiohttp.http_websocket import ALLOWED_CLOSE_CODES, WSCloseCode
from typing import Any, Coroutine, Dict, Text, Union, cast
from typing import Callable  # noqa pylint: disable=unused-import

from alexapy import aiohttp

from .alexalogin import AlexaLogin  # noqa pylint

_LOGGER = logging.getLogger(__name__)


class Content:
    # pylint: disable=too-few-public-methods, too-many-instance-attributes
    """Content Data Class."""

    def __init__(self) -> None:
        """Init for data."""
        self.message_type: Text = ""
        self.protocol_version: Text = ""
        self.connection_uuid: Text = ""
        self.established: int = 0
        self.timestamp_ini: int = 0
        self.timestamp_ack: int = 0
        self.submessage_type: Text = ""
        self.channel: int = 0
        self.dest_id_urn: Text = ""
        self.device_id_urn: Text = ""
        self.payload: Text = ""
        self.payload_data: bytearray = bytearray()


class Message:
    # pylint: disable=too-few-public-methods, too-many-instance-attributes
    """Message Data Class."""

    def __init__(self, data: bytes) -> None:
        # pylint: disable=too-many-nested-blocks
        """Init for data."""
        self.service: Text = ""
        self.content: Content = Content()
        self.content_tune: Text = ""
        self.message_type: Text = ""
        self.channel: int = 0
        self.checksum: int = 0
        self.message_id: int = 0
        self.more_flag: Text = ""
        self.seq: int = 0
        self.json_payload: Dict[Text, Union[Text, Dict[Text, Text]]] = {}

        def read_hex(index: int, length: int) -> int:
            return int(data[index : index + length], 16)

        def read_string(index: int, length: int) -> Text:
            return data[index : index + length].decode("ascii")

        idx = 0
        self.service = read_string(len(data) - 4, 4)

        if self.service == "TUNE":
            self.checksum = read_hex(idx, 10)
            idx += 11
            # 10 + delimiter
            content_length = read_hex(idx, 10)
            idx += 11
            # 10 + delimiter
            self.content = read_string(idx, content_length - 4 - idx)
            if self.content.startswith("{") and self.content.endswith("}"):
                try:
                    self.content = json.loads(self.content)
                except json.decoder.JSONDecodeError:
                    pass
        elif self.service == "FABE":
            self.message_type = read_string(0, 3)
            self.channel = int.from_bytes(data[3:7], "big")
            self.message_id = int.from_bytes(data[7:11], "big")
            self.more_flag = data[11]
            self.seq = int.from_bytes(data[12:16], "big")
            self.checksum = int.from_bytes(data[16:20], "big")

            content_length = int.from_bytes(data[20:24], "big")

            self.content.message_type = read_string(24, 3)
            idx = 28

            if self.channel == 0x361:  # // GW_HANDSHAKE_CHANNEL
                if self.content.message_type == "ACK":
                    length = read_hex(idx, 10)
                    idx += 11  # 10 + delimiter;
                    self.content.protocol_version = read_string(idx, length)
                    idx += length + 1
                    length = read_hex(idx, 10)
                    idx += 11  # 10 + delimiter;
                    self.content.connection_uuid = read_string(idx, length)
                    idx += length + 1
                    self.content.established = read_hex(idx, 10)
                    idx += 11  # 10 + delimiter;
                    self.content.timestamp_ini = read_hex(idx, 18)
                    idx += 19  # 18 + delimiter;
                    self.content.timestamp_ack = read_hex(idx, 18)
                    idx += 19  # 18 + delimiter;
            elif self.channel == 0x362:  # // GW_CHANNEL
                if self.content.message_type == "GWM":
                    self.content.submessage_type = read_string(idx, 3)
                    idx += 4
                    self.content.channel = read_hex(idx, 10)
                    idx += 11  # 10 + delimiter

                    if self.content.channel == 0xB479:  # // DEE_WEBSITE_MESSAGING
                        length = read_hex(idx, 10)
                        idx += 11  # 10 + delimiter
                        self.content.dest_id_urn = read_string(idx, length)
                        idx += length + 1

                        length = read_hex(idx, 10)
                        idx += 11
                        # 10 + delimiter
                        id_data = read_string(idx, length)
                        idx += length + 1

                        id_data = id_data.split(" ")
                        self.content.device_id_urn = id_data[0]
                        if len(id_data) > 1:
                            self.content.payload = id_data[1]
                        else:
                            self.content.payload = read_string(idx, len(data) - 4 - idx)
                        if self.content.payload.startswith(
                            "{"
                        ) and self.content.payload.endswith("}"):
                            try:
                                self.json_payload = json.loads(self.content.payload)
                                self.json_payload["payload"] = json.loads(
                                    self.json_payload["payload"]  # type: ignore
                                )
                            except json.decoder.JSONDecodeError:
                                pass
            elif self.channel == 0x65:  # CHANNEL_FOR_HEARTBEAT
                self.content.payload_data = data[idx : len(data) - 4]


class WebsocketEchoClient:
    # pylint: disable=too-many-instance-attributes
    """WebSocket Client Class for Echo Devices.

    Based on code from openHAB:
    https://github.com/openhab/openhab2-addons/blob/master/addons/binding/org.openhab.binding.amazonechocontrol/src/main/java/org/openhab/binding/amazonechocontrol/internal/WebSocketConnection.java
    which is further based on:
    https://github.com/Apollon77/alexa-remote/blob/master/alexa-wsmqtt.js
    """

    def __init__(
        self,
        login: AlexaLogin,
        msg_callback: Callable[[Message], Coroutine[Any, Any, None]],
        open_callback: Callable[[], Coroutine[Any, Any, None]],
        close_callback: Callable[[], Coroutine[Any, Any, None]],
        error_callback: Callable[[Text], Coroutine[Any, Any, None]],
    ) -> None:
        # pylint: disable=too-many-arguments
        """Init for threading and WebSocket Connection."""
        if login.url.lower() == "amazon.com":
            subdomain = "dp-gw-na-js"  # type: Text
        else:
            subdomain = "dp-gw-na"
        url = f"wss://{subdomain}.{login.url}/tcomm/"
        assert login.session is not None
        self._session = login.session
        self._mac_dms = login.mac_dms
        self._cookies: Dict[Text, Text] = (
            login.session._cookie_jar if login.session._cookie_jar else {}
        )
        self._headers = {}  # login._headers
        self._ssl = login._ssl
        self._message_id = math.floor(1e9 * random.random())
        self._message_count = 0
        cookies = ""  # type: Text
        # assert self._cookies is not None
        for key, cookie in self._cookies.filter_cookies(login.url).items():
            cookies += f"{key}={cookie.value}; "
        self._headers["Cookie"] = cookies
        # the old websocket-client auto populates origin, which
        # aiohttp does not and is necessary for Amazon to accept a login
        self._headers["Origin"] = "https://alexa." + login.url
        self._headers["Host"] = f"dp-gw-na.{login.url}"
        if self._mac_dms:
            self._headers.update(
                {
                    "Connection": "keep-alive, Upgrade",
                    "Upgrade": "websocket",
                    "Pragma": "no-cache",
                    "Cache-Control": "no-cache",
                    "x-dp-comm-tuning": "A:F;A:H",
                    "x-dp-reason": "ClientInitiated;1",
                    "x-dp-tcomm-purpose": "Regular",
                    # 'x-dp-deviceVersion': 'motorola/osprey_reteu_2gb/osprey_u2:6.0.1/MPI24.107-55/33:user/release-keys',
                    # 'x-dp-networkType': 'WIFI',
                    # 'x-dp-tcomm-versionCode': '894920010',
                    # 'x-dp-oui': 'dca632',
                    "x-dp-obfuscatedBssid": "-2019514039",
                    "x-dp-tcomm-versionName": "2.2.443692.0",
                    "x-adp-signature": self._create_request_signature(
                        "GET", "/tcomm/", ""
                    ),
                    "x-adp-token": self._mac_dms["adp_token"],
                    "x-adp-alg": "SHA256WithRSA:1.0",
                }
            )
        else:
            _LOGGER.warning("mac_dms not detected; websocket likely won't connect")
        # url_array: List[Text] = login.url.split(".")
        # ubid_id: Text = f"ubid-acb{url_array[len(url_array)-1]}"
        # if ubid_id in self._cookies:
        #     url += str(self._cookies[ubid_id])
        # elif "ubid-main" in self._cookies:
        #     url += str(self._cookies["ubid-main"])
        # else:
        #     _LOGGER.warning(
        #         "Websocket is missing ubid-main and %s cookies;"
        #         " please report this if anything isn't working.",
        #         ubid_id,
        #     )
        # url += "-" + str(int(time.time())) + "000"
        # url = "ws://localhost:8080/ws"
        self.open_callback: Callable[[], Coroutine[Any, Any, None]] = open_callback
        self.msg_callback: Callable[[Message], Coroutine[Any, Any, None]] = msg_callback
        self.close_callback: Callable[[], Coroutine[Any, Any, None]] = close_callback
        self.error_callback: Callable[
            [Text], Coroutine[Any, Any, None]
        ] = error_callback
        self._wsurl: Text = url
        self.websocket: aiohttp.ClientWebSocketResponse
        self._loop: asyncio.AbstractEventLoop

    async def async_run(self) -> None:
        """Start Async WebSocket Listener."""
        _LOGGER.debug("Connecting to %s with %s", self._wsurl, self._headers)
        self.websocket = await self._session.ws_connect(
            self._wsurl, headers=self._headers, heartbeat=180, ssl=self._ssl
        )
        loop = asyncio.get_event_loop()
        self._loop = loop
        task = loop.create_task(self.process_messages())
        task.add_done_callback(self.on_close)
        await self.async_on_open()

    async def process_messages(self) -> None:
        """Start Async WebSocket Listener."""
        _LOGGER.debug("Starting message parsing loop.")
        async for msg in self.websocket:
            # _LOGGER.debug("msg: %s", msg)
            if msg.type == aiohttp.WSMsgType.BINARY:
                await self.on_message(cast(bytes, msg.data))
            elif msg.type == aiohttp.WSMsgType.ERROR:
                self.on_error("WSMsgType error")
                break
            self._message_count += 1

    async def on_message(self, message: bytes) -> None:
        # pylint: disable=too-many-statements
        """Handle New Message."""
        _LOGGER.debug("Received raw WebSocket: %s", message)
        message_obj: Message = Message(message)
        await self.msg_callback(message_obj)
        if self._message_count == 0:  # initialization
            msg = self._encode_ws_handshake()
            await self.websocket.send_bytes(msg)
            _LOGGER.debug("A:F Initialization Msg 2 sent: %s", msg.hex())
            await asyncio.sleep(0.05)
            msg = self._encode_gw_register()
            await self.websocket.send_bytes(msg)
            _LOGGER.debug(
                "A:F Initialization Msg 3 (Register Connection) sent: %s", msg.hex()
            )
            await asyncio.sleep(0.05)
            msg = self._encode_ping()
            await self.websocket.send_bytes(msg)
            _LOGGER.debug("Send First Ping: %s", msg.hex())
        if self._message_count == 1:
            await asyncio.sleep(0.5)
            msg = self._encode_ping()
            await self.websocket.send_bytes(msg)
            _LOGGER.debug("Send Second Ping: %s", msg.hex())
            await asyncio.sleep(0.5)

    def on_error(self, error: Text = "Unspecified") -> None:
        """Handle WebSocket Error."""
        _LOGGER.debug("WebSocket Error: %s", error)
        asyncio.run_coroutine_threadsafe(self.error_callback(error), self._loop)

    def on_close(self, future="") -> None:
        """Handle WebSocket Close."""
        exception_ = self.websocket.exception()
        if exception_:
            self.on_error(str(type(exception_)))
        _LOGGER.debug(
            "WebSocket Connection Closed. %s",
            WSCloseCode(self.websocket.close_code)
            if self.websocket.close_code in ALLOWED_CLOSE_CODES
            else self.websocket.close_code,
        )
        self._message_count = 0
        asyncio.run_coroutine_threadsafe(self.close_callback(), self._loop)

    async def async_on_open(self) -> None:
        """Handle Async WebSocket Open."""
        if not self.websocket.closed:
            await self.open_callback()

    def _encode_ws_handshake(self) -> bytes:
        # pylint: disable=no-self-use
        _LOGGER.debug("Encoding WebSocket Handshake MSG.")
        msg = "0xa6f6a951 " if not self._mac_dms else "0xfe88bc52 "
        msg += "0x0000009c "
        msg += (
            '{"protocolName":"A:H","parameters":'
            if not self._mac_dms
            else '{"protocolName":"A:F","parameters":'
        )
        msg += '{"AlphaProtocolHandler.receiveWindowSize":"16","'
        msg += 'AlphaProtocolHandler.maxFragmentSize":"16000"}}TUNE'
        _LOGGER.debug(msg)
        return bytes(msg, "utf-8")

    def _encode_gw_handshake(self, messageid=None) -> bytes:
        # pylint: disable=no-self-use
        _LOGGER.debug("Encoding Gateway Handshake MSG.")
        if messageid:
            self._message_id = messageid
        else:
            self._message_id += 1
        msg = "MSG 0x00000361 "  # MSG channel
        msg += f"0x{hex(self._message_id)[2:].zfill(8)} f 0x00000001 "  # Message number with no cont
        idx = len(msg)
        msg += "0x00000000 "  # Checksum
        idx2 = len(msg)
        msg += "0x0000009b "  # Content Length
        msg += "INI 0x00000003 1.0 0x00000024 "  # Message content
        msg += f"{uuid.uuid4()} "  # Message UUID
        msg += (
            f"0x{hex(round(time.time() * 1000))[2:].zfill(8)} "  # Hex encoded timestamp
        )
        msg += "END FABE"
        complete_buffer = bytearray(msg, "ascii")
        checksum = compute_checksum(complete_buffer, idx, idx2)
        copy_string_to_bytearray(complete_buffer, checksum, 39)
        _LOGGER.debug(complete_buffer)
        return bytes(complete_buffer)

    def _encode_gw_register(self, messageid=None) -> bytes:
        # pylint: disable=no-self-use
        _LOGGER.debug("Encoding Gateway Register MSG.")
        if messageid:
            self._message_id = messageid
        else:
            self._message_id += 1
        complete_buffer = bytearray(0xE4)
        copy_string_to_bytearray(complete_buffer, "MSG", 0)
        copy_int_to_bytearray(complete_buffer, 0x00000362, 3)
        copy_int_to_bytearray(complete_buffer, self._message_id, 7)
        copy_string_to_bytearray(complete_buffer, "f", 11)
        copy_int_to_bytearray(complete_buffer, 0x00000001, 12)
        copy_int_to_bytearray(complete_buffer, 0x00000000, 16)
        copy_int_to_bytearray(complete_buffer, 0x000000E4, 20)
        copy_string_to_bytearray(
            complete_buffer,
            'GWM MSG 0x0000b479 0x0000003b urn:tcomm-endpoint:device:deviceType:0:deviceSerialNumber:0 0x00000041 urn:tcomm-endpoint:service:serviceName:DeeWebsiteMessagingService {"command":"REGISTER_CONNECTION"}FABE',
            24,
        )
        checksum = compute_checksum(complete_buffer, 16, 20)
        copy_int_to_bytearray(complete_buffer, checksum, 16)
        _LOGGER.debug(complete_buffer)
        return bytes(complete_buffer)

    def _encode_ping(self, messageid=None) -> bytes:
        # pylint: disable=no-self-use
        def encode(buffer: bytearray, seed: int, byte_offset: int, length: int) -> None:
            view = memoryview(buffer)[byte_offset : byte_offset + length]
            idx = 0
            while idx < length:
                view[idx] = seed >> 8 * (length - 1 - idx) & 255
                idx += 1

        _LOGGER.debug("Encoding PING.")
        if messageid:
            self._message_id = messageid
        else:
            self._message_id += 1
        complete_buffer = bytearray(0x3D)
        copy_string_to_bytearray(complete_buffer, "MSG", 0)
        copy_int_to_bytearray(complete_buffer, 0x00000065, 3)
        copy_int_to_bytearray(complete_buffer, self._message_id, 7)
        copy_string_to_bytearray(complete_buffer, "f", 11)
        copy_int_to_bytearray(complete_buffer, 0x00000001, 12)
        copy_int_to_bytearray(complete_buffer, 0x00000000, 16)
        copy_int_to_bytearray(complete_buffer, 0x0000003D, 20)

        header = "PIN"
        payload = "Regular"
        buffer = bytearray(len(header) + 4 + 8 + 4 + 2 * len(payload))
        idx = 0
        view = memoryview(buffer)[idx : idx + len(header)]
        zero = 0
        now = round(time.time() * 1000)
        i = 0
        while i < len(header):
            view[i] = int.from_bytes(header[i].encode(), byteorder="big")
            i += 1
        idx += len(header)
        encode(buffer, zero, idx, 4)
        idx += 4
        encode(buffer, now, idx, 8)
        idx += 8
        encode(buffer, len(payload), idx, 4)
        idx += 4
        view = memoryview(buffer)[idx : idx + (len(payload) * 2)]
        i = 0
        while i < len(payload):
            view[i * 2] = 0
            view[i * 2 + 1] = int.from_bytes(payload[i].encode(), byteorder="big")
            i += 1
        copy_array_to_bytearray(complete_buffer, buffer, 24)
        copy_string_to_bytearray(complete_buffer, "FABE", len(buffer) + 24)
        checksum = compute_checksum(complete_buffer, 16, 20)
        copy_int_to_bytearray(complete_buffer, checksum, 16)
        _LOGGER.debug(complete_buffer)
        return bytes(complete_buffer)

    def _create_request_signature(self, method: Text, path: Text, body) -> Text:
        """Create request signature.

        Args:
            method ([type]): The http request method (GET, POST, DELETE, ...).
            path ([type]): The requested http url path and query.
            body ([type]): The http message body.

        Returns:
            Text: [description]
        """
        date = datetime.datetime.utcnow().isoformat("T") + "Z"
        data = f"{method}\n{path}\n{date}\n{body}\n{self._mac_dms['adp_token']}"
        private_key_string = f"-----BEGIN RSA PRIVATE KEY-----\n{self._mac_dms['device_private_key']}\n-----END RSA PRIVATE KEY-----"

        private_key = serialization.load_pem_private_key(
            private_key_string.encode("utf-8"), None
        )
        cipher = private_key.sign(
            data.encode(),
            padding=padding.PKCS1v15(),  # required for Amazon's padding. PSS is not supported and results in disconnects.
            algorithm=hashes.SHA256(),
        )
        signed_encoded = base64.b64encode(cipher)
        signature = f"{signed_encoded.decode()}:{date}"
        # _LOGGER.debug(f"Data {data}\nKey\n{self._mac_dms['device_private_key']}\nSignature {signature}")
        return signature


# Checksum from https://github.com/Apollon77/alexa-remote/blob/master/alexa-wsmqtt.js#L571-L587
def compute_checksum(text: Union[Text, bytearray], f: int, k: int) -> int:
    # pylint: disable=invalid-name
    """Compute checksum of text or byte array.

    Args:
        text (Text|bytearray): Input text
        f (int): begin of window
        k (int): end of window

    Returns:
        int: [description]
    """

    def b(a: int, b: int) -> int:
        a = c(a)
        while b != 0 and a != 0:
            a = math.floor(a / 2)
            b -= 1
        return a

    def c(a: int) -> int:
        if a < 0:
            a = 4294967295 + a + 1
        return a

    if k < f:
        raise ValueError("Invalid checksum exclusion window!")
    a: bytearray = bytearray(text, "utf-8") if isinstance(text, str) else text
    h: int = 0
    temp_l: int = 0
    e: int = 0
    while e < len(a):
        if e != f:
            temp_l += c(a[e] << ((e & 3 ^ 3) << 3))
            h += b(temp_l, 32)
            temp_l = c(temp_l & 4294967295)
        else:
            e = k - 1
        e += 1
    while h > 0:
        temp_l += h
        h = b(temp_l, 32)
        temp_l &= 4294967295
    return c(temp_l)


def copy_string_to_bytearray(target: bytearray, string: Text, offset: int = 0):
    """Copy string into bytearray.

    Args:
        target (bytearray): Target
        string (Text): String to copy
        offset (int, optional): Offset in target. Defaults to 0.
    """
    view = memoryview(target)[offset : offset + len(string)]
    for idx in range(len(string)):
        view[idx] = int.from_bytes(string[idx].encode(), byteorder="big")


def copy_int_to_bytearray(target: bytearray, number: int, offset: int = 0):
    """Copy int to bytearray.

    Args:
        target (bytearray): Target
        number (int): Int to copy
        offset (int, optional): Offset in target. Defaults to 0.
    """
    string = (number).to_bytes(4, byteorder="big")
    view = memoryview(target)[offset : offset + len(string)]
    for idx in range(len(string)):
        view[idx] = string[idx]


def copy_array_to_bytearray(target: bytearray, source: bytearray, offset: int = 0):
    """Copy array into a bytearray.

    Args:
        target (bytearray): Target
        source (bytearray): Source
        offset (int, optional): Offset in target. Defaults to 0.
    """
    view = memoryview(target)[offset : offset + len(source)]
    for idx in range(len(source)):
        view[idx] = source[idx]
