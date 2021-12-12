"""Python Package for controlling Alexa devices (echo dot, etc) programmatically.

SPDX-License-Identifier: Apache-2.0

API access.

For more details about this api, please refer to the documentation at
https://gitlab.com/keatontaylor/alexapy
"""
import asyncio
import json
from json.decoder import JSONDecodeError
import logging
import math
import time
from typing import Any, Dict, List, Optional, Text

import backoff
from yarl import URL

from alexapy.aiohttp import ClientConnectionError, ClientResponse

from .alexalogin import AlexaLogin
from .errors import (
    AlexapyConnectionError,
    AlexapyLoginCloseRequested,
    AlexapyLoginError,
    AlexapyTooManyRequestsError,
)
from .helpers import _catch_all_exceptions, hide_email

_LOGGER = logging.getLogger(__name__)


class AlexaAPI:
    # pylint: disable=too-many-public-methods
    """Class for accessing a specific Alexa device using rest API.

    Args:
    device (AlexaClient): Instance of an AlexaClient to access
    login (AlexaLogin): Successfully logged in AlexaLogin

    """

    devices: Dict[Text, Any] = {}
    _sequence_queue: Dict[Any, List[Dict[Any, Any]]] = {}
    _sequence_lock: Dict[Any, asyncio.Lock] = {}

    def __init__(self, device, login: AlexaLogin):
        """Initialize Alexa device."""
        self._device = device
        self._login = login
        self._session = login.session
        self._url: Text = "https://alexa." + login.url
        self._login._headers["Referer"] = f"{self._url}/spa/index.html"
        AlexaAPI._sequence_queue[self._login.email] = []
        AlexaAPI._sequence_lock[self._login.email] = asyncio.Lock()
        try:
            csrf = self._login._get_cookies_from_session()["csrf"]
            self._login._headers["csrf"] = csrf.value
        except KeyError as ex:
            _LOGGER.warning(
                (
                    "AlexaLogin session is missing required token: %s "
                    "This may result in authorization errors, please report if unable to login"
                ),
                ex,
            )

    def update_login(self, login: AlexaLogin) -> bool:
        """Update Login if it has changed.

        Args
            login (AlexaLogin): AlexaLogin to check

        Returns
            bool: True if change detected

        """
        if login != self._login or login.session != self._session:
            _LOGGER.debug(
                "%s: New Login %s detected; replacing %s",
                hide_email(login.email),
                login,
                self._login,
            )
            self._login = login
            self._session = login.session
            self._url: Text = "https://alexa." + login.url
            self._login._headers["Referer"] = f"{self._url}/spa/index.html"
            try:
                csrf = self._login._get_cookies_from_session()["csrf"]
                self._login._headers["csrf"] = csrf.value
            except KeyError as ex:
                if login.status.get("login_successful"):
                    _LOGGER.warning(
                        (
                            "AlexaLogin session is missing required token: %s "
                            "This may result in authorization errors, please report"
                        ),
                        ex,
                    )
            return True
        return False

    @backoff.on_exception(
        backoff.expo,
        (AlexapyTooManyRequestsError, AlexapyConnectionError, ClientConnectionError),
        max_time=60,
        max_tries=5,
        logger=__name__,
    )
    async def _request(
        self,
        method: Text,
        uri: Text,
        data: Optional[Dict[Text, Text]] = None,
        query: Optional[Dict[Text, Text]] = None,
    ) -> ClientResponse:
        async with self._login._oauth_lock:
            if self._login.expires_in and (self._login.expires_in - time.time() < 0):
                _LOGGER.debug(
                    "%s: Detected access token expiration; refreshing",
                    hide_email(self._login.email),
                )
                if (
                    # await self._login.get_tokens()
                    # and
                    await self._login.refresh_access_token()
                    and await self._login.exchange_token_for_cookies()
                    and await self._login.get_csrf()
                ):
                    await self._login.save_cookiefile()
                else:
                    _LOGGER.debug(
                        "%s: Unable to refresh oauth", hide_email(self._login.email),
                    )
                    self._login.access_token = None
                    self._login.refresh_token = None
                    self._login.expires_in = None
        if method == "get":
            if query and not query.get("_"):
                query["_"] = math.floor(time.time() * 1000)
            elif query is None:
                query = {"_": math.floor(time.time() * 1000)}
        url: URL = URL(self._url + uri).update_query(query)
        # _LOGGER.debug("%s: Trying %s: %s : with uri: %s data %s query %s",
        #               method,
        #               url,
        #               uri,
        #               data,
        #               query)
        if self._login.close_requested:
            _LOGGER.debug(
                "%s: Login object has been asked to close; ignoring %s request to %s with %s %s",
                hide_email(self._login.email),
                method,
                uri,
                data,
                query,
            )
            raise AlexapyLoginCloseRequested()
        if not self._login.status.get("login_successful"):
            _LOGGER.debug(
                "%s:Login error detected; ignoring %s request to %s with %s %s",
                hide_email(self._login.email),
                method,
                uri,
                data,
                query,
            )
            raise AlexapyLoginError("Login error detected; not contacting API")
        if self._session.closed:
            raise AlexapyLoginError("Session is closed")
        response = await getattr(self._session, method)(
            url,
            json=data,
            # cookies=self._login._cookies,
            headers=self._login._headers,
            ssl=self._login._ssl,
        )
        _LOGGER.debug(
            "%s: %s: %s returned %s:%s:%s",
            hide_email(self._login.email),
            response.request_info.method,
            response.request_info.url,
            response.status,
            response.reason,
            response.content_type,
        )
        self._login.stats["api_calls"] += 1
        if response.status == 401:
            self._login.status["login_successful"] = False
            raise AlexapyLoginError(response.reason)
        if response.status == 429:
            raise AlexapyTooManyRequestsError(response.reason)
        return response

    async def _post_request(
        self, uri: Text, data: Optional[Dict[Text, Any]] = None
    ) -> ClientResponse:
        return await self._request("post", uri, data)

    async def _put_request(
        self, uri: Text, data: Optional[Dict[Text, Text]] = None
    ) -> ClientResponse:
        return await self._request("put", uri, data)

    async def _get_request(
        self, uri: Text, data: Optional[Dict[Text, Text]] = None
    ) -> ClientResponse:
        return await self._request("get", uri, data)

    async def _del_request(
        self, uri: Text, data: Optional[Dict[Text, Text]] = None
    ) -> ClientResponse:
        return await self._request("delete", uri, data)

    @staticmethod
    @backoff.on_exception(
        backoff.expo,
        (AlexapyTooManyRequestsError, AlexapyConnectionError, ClientConnectionError),
        max_time=60,
        max_tries=5,
        logger=__name__,
    )
    async def _static_request(
        method: Text,
        login: AlexaLogin,
        uri: Text,
        data: Optional[Dict[Text, Text]] = None,
        query: Optional[Dict[Text, Text]] = None,
    ) -> ClientResponse:
        async with login._oauth_lock:
            if login.expires_in and (login.expires_in - time.time() < 0):
                _LOGGER.debug(
                    "%s: Detected access token expiration; refreshing",
                    hide_email(login.email),
                )
                if (
                    # await login.get_tokens()
                    # and
                    await login.refresh_access_token()
                    and await login.exchange_token_for_cookies()
                    and await login.get_csrf()
                ):
                    await login.save_cookiefile()
                else:
                    _LOGGER.debug(
                        "%s: Unable to refresh oauth", hide_email(login.email),
                    )
                    login.access_token = None
                    login.refresh_token = None
                    login.expires_in = None
        session = login.session
        url: URL = URL("https://alexa." + login.url + uri).update_query(query)
        # _LOGGER.debug("%s: %s: Trying static %s: %s : with uri: %s data %s query %s", hide_email(login.email)
        #               method,
        #               url,
        #               uri,
        #               data,
        #               query)
        if login.close_requested:
            _LOGGER.debug(
                "%s: Login object has been asked to close; ignoring %s request to %s with %s %s",
                hide_email(login.email),
                method,
                uri,
                data,
                query,
            )
            raise AlexapyLoginCloseRequested()
        if not login.status.get("login_successful"):
            _LOGGER.debug(
                "%s: Login error detected; ignoring %s request to %s with %s %s",
                hide_email(login.email),
                method,
                uri,
                data,
                query,
            )
            raise AlexapyLoginError("Login error detected; not contacting API")
        if session.closed:
            raise AlexapyLoginError("Session is closed")
        response = await getattr(session, method)(
            url,
            json=data,
            # cookies=login._cookies,
            headers=login._headers,
            ssl=login._ssl,
        )
        _LOGGER.debug(
            "%s: static %s: %s returned %s:%s:%s",
            hide_email(login.email),
            response.request_info.method,
            response.request_info.url,
            response.status,
            response.reason,
            response.content_type,
        )
        login.stats["api_calls"] += 1
        if response.status == 401:
            login.status["login_successful"] = False
            raise AlexapyLoginError(response.reason)
        if response.status == 429:
            raise AlexapyTooManyRequestsError(response.reason)
        return response

    @_catch_all_exceptions
    async def run_behavior(self, node_data, queue_delay: float = 1.5,) -> None:
        """Queue node_data for running a behavior in sequence.

        Amazon sequences and routines are based on node_data.

        Args:
            node_data (dict, list of dicts): The node_data to run.
            queue_delay (float, optional): The number of seconds to wait
                                          for commands to queue together.
                                          Defaults to 1.5.
                                          Must be positive.

        """
        sequence_json: Dict[Any, Any] = {
            "@type": "com.amazon.alexa.behaviors.model.Sequence",
            "startNode": node_data,
        }
        if queue_delay is None:
            queue_delay = 1.5
        if queue_delay > 0:
            sequence_json["startNode"] = {
                "@type": "com.amazon.alexa.behaviors.model.SerialNode",
                "nodesToExecute": [],
            }
            async with AlexaAPI._sequence_lock[self._login.email]:
                if AlexaAPI._sequence_queue[self._login.email]:
                    last_node = AlexaAPI._sequence_queue[self._login.email][-1]
                    new_node = node_data
                    if node_data and isinstance(node_data, list):
                        new_node = node_data[0]
                    if (
                        last_node.get("operationPayload", {}).get("deviceSerialNumber")
                        and new_node.get("operationPayload", {}).get(
                            "deviceSerialNumber"
                        )
                    ) and last_node.get("operationPayload", {}).get(
                        "deviceSerialNumber"
                    ) != new_node.get(
                        "operationPayload", {}
                    ).get(
                        "deviceSerialNumber"
                    ):
                        _LOGGER.debug(
                            "%s: Creating Parallel node", hide_email(self._login.email),
                        )
                        sequence_json["startNode"][
                            "@type"
                        ] = "com.amazon.alexa.behaviors.model.ParallelNode"
                if isinstance(node_data, list):
                    AlexaAPI._sequence_queue[self._login.email].extend(node_data)
                else:
                    AlexaAPI._sequence_queue[self._login.email].append(node_data)
                items = len(AlexaAPI._sequence_queue[self._login.email])
                old_sequence: List[Dict[Any, Any]] = AlexaAPI._sequence_queue[
                    self._login.email
                ]
            await asyncio.sleep(queue_delay)
            async with AlexaAPI._sequence_lock[self._login.email]:
                if (
                    items == len(AlexaAPI._sequence_queue[self._login.email])
                    and old_sequence == AlexaAPI._sequence_queue[self._login.email]
                ):
                    sequence_json["startNode"]["nodesToExecute"].extend(
                        AlexaAPI._sequence_queue[self._login.email]
                    )
                    AlexaAPI._sequence_queue[self._login.email] = []
                    _LOGGER.debug(
                        "%s: Creating sequence for %s items",
                        hide_email(self._login.email),
                        items,
                    )
                else:
                    _LOGGER.debug(
                        "%s: Queue changed while waiting %s seconds",
                        hide_email(self._login.email),
                        queue_delay,
                    )
                    return
        data = {
            "behaviorId": "PREVIEW",
            "sequenceJson": json.dumps(sequence_json),
            "status": "ENABLED",
        }
        _LOGGER.debug(
            "%s: Running behavior with data: %s",
            hide_email(self._login.email),
            json.dumps(data),
        )
        await self._post_request("/api/behaviors/preview", data=data)

    @_catch_all_exceptions
    async def send_sequence(
        self,
        sequence: Text,
        customer_id: Optional[Text] = None,
        queue_delay: float = 1.5,
        extra: Optional[Dict[Any, Any]] = None,
        **kwargs,
    ) -> None:
        """Send sequence command.

        This allows some programatic control of Echo device using the behaviors
        API and is the basis of play_music, send_announcement, and send_tts.

        Args:
        sequence (string): The Alexa sequence.  Supported list below.
        customer_id (string): CustomerId to use for authorization. When none
                             specified this defaults to the logged in user. Used
                             with households where others may have their own
                             music.
        queue_delay (float, optional): The number of seconds to wait
                                    for commands to queue together.
                                    Defaults to 1.5.
                                    Must be positive.
        extra (Dict): Extra dictionary array; functionality undetermined
        **kwargs : Each named variable must match a recognized Amazon variable
                   within the operationPayload. Please see examples in
                   play_music, send_announcement, and send_tts.
                   Variables with value None are removed from the operationPayload.
                   Variables prefixed with "root_" will be added to the root node instead.

        Supported sequences:
        Alexa.Weather.Play
        Alexa.Traffic.Play
        Alexa.FlashBriefing.Play
        Alexa.GoodMorning.Play
        Alexa.GoodNight.Play
        Alexa.SingASong.Play
        Alexa.TellStory.Play
        Alexa.FunFact.Play
        Alexa.Joke.Play
        Alexa.CleanUp.Play
        Alexa.Music.PlaySearchPhrase
        Alexa.Calendar.PlayTomorrow
        Alexa.Calendar.PlayToday
        Alexa.Calendar.PlayNext
        https://github.com/custom-components/alexa_media_player/wiki#sequence-commands-versions--100

        """
        extra = extra or {}
        operation_payload = {
            "deviceType": self._device._device_type,
            "deviceSerialNumber": self._device.device_serial_number,
            "locale": (self._device._locale if self._device._locale else "en-US"),
            "customerId": self._login.customer_id
            if customer_id is None
            else customer_id,
        }
        root_node = {}
        if kwargs is not None:
            operation_payload.update(kwargs)
            for key, value in kwargs.items():
                if value is None:  # remove null keys
                    operation_payload.pop(key)
                elif isinstance(value, str) and value.startswith("root_"):
                    operation_payload.pop(key)
                    root_node[key] = value[5:]
            if kwargs.get("devices"):
                operation_payload.pop("deviceType")
                operation_payload.pop("deviceSerialNumber")
        node_data = {
            "@type": "com.amazon.alexa.behaviors.model.OpaquePayloadOperationNode",
            "type": sequence,
            "operationPayload": operation_payload,
        }
        node_data.update(root_node)
        await self.run_behavior(node_data, queue_delay=queue_delay)

    @_catch_all_exceptions
    async def run_skill(
        self,
        skill_id: Text,
        customer_id: Optional[Text] = None,
        queue_delay: float = 0,
    ) -> None:
        """Run Alexa skill.

        This allows running of defined Alexa skill.

        Args:
            skill_id (string): The full skill id.
            customer_id (string): CustomerId to use for authorization. When none
                             specified this defaults to the logged in user. Used
                             with households where others may have their own
                             music.
            queue_delay (float, optional): The number of seconds to wait
                                        for commands to queue together.
                                        Defaults to 1.5.
                                        Must be positive.

        """
        operation_payload = {
            "targetDevice": {
                "deviceType": self._device._device_type,
                "deviceSerialNumber": self._device.device_serial_number,
            },
            "locale": (self._device._locale if self._device._locale else "en-US"),
            "customerId": self._login.customer_id
            if customer_id is None
            else customer_id,
            "connectionRequest": {
                "uri": "connection://AMAZON.Launch/" + skill_id,
                "input": {},
            },
        }
        node_data = {
            "@type": "com.amazon.alexa.behaviors.model.OpaquePayloadOperationNode",
            "type": "Alexa.Operation.SkillConnections.Launch",
            "operationPayload": operation_payload,
        }
        await self.run_behavior(node_data, queue_delay=queue_delay)

    @_catch_all_exceptions
    async def run_custom(
        self,
        text: Text,
        customer_id: Optional[Text] = None,
        queue_delay: float = 0,
        extra: Optional[Dict[Any, Any]] = None,
    ) -> None:
        """Run Alexa skill.

        This allows running exactly what you can say to alexa.

        Args:
            text (string): The full text you want alexa to execute.
            customer_id (string): CustomerId to use for authorization. When none
                             specified this defaults to the logged in user. Used
                             with households where others may have their own
                             music.
            queue_delay (float, optional): The number of seconds to wait
                                        for commands to queue together.
                                        Defaults to 1.5.
                                        Must be positive.
            extra (Dict): Extra dictionary array; functionality undetermined

        """
        extra = extra or {}
        await self.send_sequence(
            "Alexa.TextCommand",
            skillId="amzn1.ask.1p.tellalexa",
            text=text,
            queue_delay=queue_delay,
        )

    @_catch_all_exceptions
    async def run_routine(
        self,
        utterance: Text,
        customer_id: Optional[Text] = None,
        queue_delay: float = 1.5,
    ) -> None:
        """Run Alexa automation routine.

        This allows running of defined Alexa automation routines.

        Args:
            utterance (string): The Alexa utterance to run the routine.
            customer_id (string): CustomerId to use for authorization. When none
                             specified this defaults to the logged in user. Used
                             with households where others may have their own
                             music.
            queue_delay (float, optional): The number of seconds to wait
                                        for commands to queue together.
                                        Defaults to 1.5.
                                        Must be positive.

        """

        def _populate_device_info(node):
            """Search node and replace with this Alexa's device_info."""
            if "devices" in node:
                list(map(_populate_device_info, node["devices"]))
            elif "targetDevice" in node:
                _populate_device_info(node["targetDevice"])
            elif "operationPayload" in node:
                _populate_device_info(node["operationPayload"])
            else:
                if (
                    "deviceType" in node
                    and node["deviceType"] == "ALEXA_CURRENT_DEVICE_TYPE"
                ):
                    (node["deviceType"]) = self._device._device_type
                if (
                    "deviceSerialNumber" in node
                    and node["deviceSerialNumber"] == "ALEXA_CURRENT_DSN"
                ):
                    (node["deviceSerialNumber"]) = self._device.device_serial_number
                if "locale" in node and node["locale"] == "ALEXA_CURRENT_LOCALE":
                    (node["locale"]) = (
                        self._device._locale if self._device._locale else "en-US"
                    )

        automations = await AlexaAPI.get_automations(self._login)
        automation_id = None
        sequence = None
        for automation in automations:
            # skip other automations (e.g., time, GPS, buttons)
            if "utterance" not in automation["triggers"][0]["payload"]:
                continue
            a_utterance = automation["triggers"][0]["payload"]["utterance"]
            a_name = automation.get("name")
            if (
                a_utterance is not None and a_utterance.lower() == utterance.lower()
            ) or (a_name and a_name.lower() == utterance.lower()):
                automation_id = automation["automationId"]
                sequence = automation["sequence"]
        if automation_id is None or sequence is None:
            _LOGGER.debug(
                "%s: No routine found for %s", hide_email(self._login.email), utterance
            )
            return
        new_nodes = []
        if "nodesToExecute" in sequence["startNode"]:
            # multiple sequences
            for node in sequence["startNode"]["nodesToExecute"]:
                if "nodesToExecute" in node:
                    # "@type":"com.amazon.alexa.behaviors.model.ParallelNode",
                    # nested nodesToExecute
                    for subnode in node["nodesToExecute"]:
                        _populate_device_info(subnode)
                else:
                    # "@type":"com.amazon.alexa.behaviors.model.SerialNode",
                    # nonNested nodesToExecute
                    _populate_device_info(node)
                new_nodes.append(node)
            sequence["startNode"]["nodesToExecute"] = new_nodes
            await self.run_behavior(
                sequence["startNode"]["nodesToExecute"], queue_delay=queue_delay,
            )
        else:
            # Single entry with no nodesToExecute
            _populate_device_info(sequence["startNode"])
            await self.run_behavior(
                sequence["startNode"], queue_delay=queue_delay,
            )

    @_catch_all_exceptions
    async def play_music(
        self,
        provider_id: Text,
        search_phrase: Text,
        customer_id: Optional[Text] = None,
        timer: Optional[int] = None,
        queue_delay: float = 1.5,
        extra: Optional[Dict[Any, Any]] = None,
    ) -> None:
        """Play music based on search.

        Args:
            provider_id (Text): Amazon music provider.
            search_phrase (Text): Phrase to be searched for
            customer_id (Optional[Text], optional): CustomerId to use for authorization. When none
                             specified this defaults to the logged in user. Used
                             with households where others may have their own
                             music.
            timer (Optional[int]): Number of seconds to play before stopping.
            queue_delay (float, optional): The number of seconds to wait
                                   for commands to queue together.
                                   Must be positive. Defaults to 1.5.
            extra (Dict): Extra dictionary array; functionality undetermined

        """
        extra = extra or {}
        customer_id = self._login.customer_id if customer_id is None else customer_id
        if timer:
            await self.send_sequence(
                "Alexa.Music.PlaySearchPhrase",
                customer_id=customer_id,
                searchPhrase=search_phrase,
                sanitizedSearchPhrase=search_phrase,
                musicProviderId=provider_id,
                waitTimeInSeconds=timer,
                queue_delay=queue_delay,
            )
        else:
            await self.send_sequence(
                "Alexa.Music.PlaySearchPhrase",
                customer_id=customer_id,
                searchPhrase=search_phrase,
                sanitizedSearchPhrase=search_phrase,
                musicProviderId=provider_id,
                queue_delay=queue_delay,
            )

    @_catch_all_exceptions
    async def play_sound(
        self,
        sound_string_id: Text,
        customer_id: Optional[Text] = None,
        queue_delay: float = 1.5,
        extra: Optional[Dict[Any, Any]] = None,
    ) -> None:
        """Play Alexa sound."""
        extra = extra or {}
        await self.send_sequence(
            "Alexa.Sound",
            customer_id=self._login.customer_id if customer_id is None else customer_id,
            soundStringId=sound_string_id,
            skillId="amzn1.ask.1p.sound",
            queue_delay=queue_delay,
        )

    @_catch_all_exceptions
    async def stop(
        self,
        customer_id: Optional[Text] = None,
        queue_delay: float = 1.5,
        all_devices: bool = False,
    ) -> None:
        """Stop device playback.

        Keyword Arguments:
            customer_id {Text} -- CustomerId issuing command (default: {None})
            queue_delay {float} -- The number of seconds to wait
                                   for commands to queue together.
                                   Must be positive.
                                   (default: {1.5})
            all_devices {bool} -- Whether all devices should be stopped (default: {False})

        """
        kwargs = {}

        if all_devices:
            kwargs["devices"] = (
                {
                    "deviceType": "ALEXA_ALL_DEVICE_TYPE",
                    "deviceSerialNumber": "ALEXA_ALL_DSN",
                },
            )
        else:
            kwargs["devices"] = [
                {
                    "deviceSerialNumber": self._device.device_serial_number,
                    "deviceType": self._device._device_type,
                },
            ]

        await self.send_sequence(
            "Alexa.DeviceControls.Stop",
            skillId="amzn1.ask.1p.alexadevicecontrols",
            customer_id=self._login.customer_id if customer_id is None else customer_id,
            queue_delay=queue_delay,
            **kwargs,
        )

    def process_targets(
        self, targets: Optional[List[Text]] = None
    ) -> List[Dict[Text, Text]]:
        """Process targets list to generate list of devices.

        Keyword Arguments
            targets {Optional[List[Text]]} -- List of serial numbers
                (default: {[]})

        Returns
            List[Dict[Text, Text] -- List of device dicts

        """
        targets = targets or []
        devices = []
        if self._device._device_family == "WHA":
            # Build group of devices based off _cluster_members
            for dev in AlexaAPI.devices[self._login.email]:
                if dev["serialNumber"] in self._device._cluster_members:
                    devices.append(
                        {
                            "deviceSerialNumber": dev["serialNumber"],
                            "deviceTypeId": dev["deviceType"],
                        }
                    )
        elif targets and isinstance(targets, list):
            for dev in AlexaAPI.devices[self._login.email]:
                if dev["serialNumber"] in targets or dev["accountName"] in targets:
                    devices.append(
                        {
                            "deviceSerialNumber": dev["serialNumber"],
                            "deviceTypeId": dev["deviceType"],
                        }
                    )
        else:
            devices.append(
                {
                    "deviceSerialNumber": self._device.device_serial_number,
                    "deviceTypeId": self._device._device_type,
                }
            )
        return devices

    @_catch_all_exceptions
    async def send_tts(
        self,
        message: Text,
        customer_id: Optional[Text] = None,
        targets: Optional[List[Text]] = None,
        queue_delay: float = 1.5,
    ) -> None:
        """Send message for TTS at speaker.

        This is the old method which used Alexa Simon Says which did not work
        for WHA. This will not beep prior to sending. send_announcement
        should be used instead.

        Args:
        message (string): The message to speak. For canned messages, the message
                            must start with `alexa.cannedtts.speak` as discovered
                            in the routines.
        customer_id (string): CustomerId to use for authorization. When none
                             specified this defaults to the logged in user. Used
                             with households where others may have their own
                             music.
        targets (list(string)): WARNING: This is currently non functional due
                                to Alexa's API and is only included for future
                                proofing.
                                List of serialNumber or accountName to send the
                                tts to. Only those in this AlexaAPI
                                account will be searched. If None, announce
                                will be self.
        queue_delay (float, optional): The number of seconds to wait
                                          for commands to queue together.
                                          Defaults to 1.5.
                                          Must be positive.

        """
        if message.startswith("alexa.cannedtts.speak"):
            await self.send_sequence(
                "Alexa.CannedTts.Speak",
                customer_id=self._login.customer_id
                if customer_id is None
                else customer_id,
                cannedTtsStringId=message,
                skillId="amzn1.ask.1p.saysomething",
                queue_delay=queue_delay,
            )
        else:
            target = {
                "customerId": self._login.customer_id
                if customer_id is None
                else customer_id,
                "devices": self.process_targets(targets),
            }
            await self.send_sequence(
                "Alexa.Speak",
                customer_id=self._login.customer_id
                if customer_id is None
                else customer_id,
                textToSpeak=message,
                target=target,
                skillId="amzn1.ask.1p.saysomething",
                queue_delay=queue_delay,
            )

    @_catch_all_exceptions
    async def send_announcement(
        self,
        message: Text,
        method: Text = "all",
        title: Text = "Announcement",
        customer_id: Optional[Text] = None,
        targets: Optional[List[Text]] = None,
        queue_delay: float = 1.5,
        extra: Optional[Dict[Any, Any]] = None,
    ) -> None:
        # pylint: disable=too-many-arguments
        """Send announcment to Alexa devices.

        This uses the AlexaAnnouncement and allows visual display on the Show.
        It will beep prior to speaking.

        Args:
        message (string): The message to speak or display.
        method (string): speak, show, or all
        title (string): title to display on Echo show
        customer_id (string): CustomerId to use for authorization. When none
                             specified this defaults to the logged in user. Used
                             with households where others may have their own
                             music.
        targets (list(string)): List of serialNumber or accountName to send the
                                announcement to. Only those in this AlexaAPI
                                account will be searched. If None, announce
                                will be self.
        queue_delay (float, optional): The number of seconds to wait
                                        for commands to queue together.
                                        Defaults to 1.5.
                                        Must be positive.
        extra (Dict): Extra dictionary array; functionality undetermined

        """
        extra = extra or {}
        display = (
            {"title": "", "body": ""}
            if method.lower() == "speak"
            else {"title": title, "body": message}
        )
        speak = (
            {"type": "text", "value": ""}
            if method.lower() == "show"
            else {"type": "text", "value": message}
        )
        content = [
            {
                "locale": (self._device._locale if self._device._locale else "en-US"),
                "display": display,
                "speak": speak,
            }
        ]
        target = {
            "customerId": self._login.customer_id
            if customer_id is None
            else customer_id,
            "devices": self.process_targets(targets),
        }
        await self.send_sequence(
            "AlexaAnnouncement",
            customer_id=self._login.customer_id if customer_id is None else customer_id,
            expireAfter="PT5S",
            content=content,
            target=target,
            skillId="amzn1.ask.1p.routines.messaging",
            queue_delay=queue_delay,
        )

    @_catch_all_exceptions
    async def send_mobilepush(
        self,
        message: Text,
        title: Text = "AlexaAPI Message",
        customer_id: Optional[Text] = None,
        queue_delay: float = 1.5,
        extra: Optional[Dict[Any, Any]] = None,
    ) -> None:
        """Send mobile push to Alexa app.

        Push a message to mobile devices with the Alexa App. This probably
        should be a static method.

        Args:
        message (string): The message to push to the mobile device.
        title (string): Title for push notification
        customer_id (string): CustomerId to use for sending. When none
                              specified this defaults to the logged in user.
        queue_delay (float, optional): The number of seconds to wait
                                        for commands to queue together.
                                        Defaults to 1.5.
                                        Must be positive.
        extra (Dict): Extra dictionary array; functionality undetermined

        """
        extra = extra or {}
        await self.send_sequence(
            "Alexa.Notifications.SendMobilePush",
            customer_id=(
                self._login.customer_id if customer_id is None else customer_id
            ),
            notificationMessage=message,
            alexaUrl="#v2/behaviors",
            title=title,
            skillId="amzn1.ask.1p.routines.messaging",
            queue_delay=queue_delay,
        )

    @_catch_all_exceptions
    async def send_dropin_notification(
        self,
        message: Text,
        title: Text = "AlexaAPI Dropin Notification",
        customer_id: Optional[Text] = None,
        queue_delay: float = 1.5,
        extra: Optional[Dict[Any, Any]] = None,
    ) -> None:
        """Send dropin notification to Alexa app for Alexa device.

        Push a message to mobile devices with the Alexa App. This can spawn a
        notification to drop in on a specific device.

        Args:
        message (string): The message to push to the mobile device.
        title (string): Title for push notification
        customer_id (string): CustomerId to use for sending. When none
                              specified this defaults to the logged in user.
        queue_delay (float, optional): The number of seconds to wait
                                        for commands to queue together.
                                        Defaults to 1.5.
                                        Must be positive.
        extra (Dict): Extra dictionary array; functionality undetermined

        """
        extra = extra or {}
        await self.send_sequence(
            "Alexa.Notifications.DropIn",
            customer_id=(
                self._login.customer_id if customer_id is None else customer_id
            ),
            notificationMessage=message,
            alexaUrl="#v2/comms/conversation-list?showDropInDialog=true",
            title=title,
            skillId="root_amzn1.ask.1p.action.dropin",
            queue_delay=queue_delay,
            deviceType=None,
            deviceSerialNumber=None,
            locale=None,
        )

    async def set_media(self, data: Dict[Text, Any]) -> None:
        """Select the media player."""
        await self._post_request(
            "/api/np/command?deviceSerialNumber="
            + self._device.device_serial_number
            + "&deviceType="
            + self._device._device_type,
            data=data,
        )

    @_catch_all_exceptions
    async def previous(self) -> None:
        """Play previous."""
        await self.set_media({"type": "PreviousCommand"})

    @_catch_all_exceptions
    async def next(self) -> None:
        """Play next."""
        await self.set_media({"type": "NextCommand"})

    @_catch_all_exceptions
    async def pause(self) -> None:
        """Pause."""
        await self.set_media({"type": "PauseCommand"})

    @_catch_all_exceptions
    async def play(self) -> None:
        """Play."""
        await self.set_media({"type": "PlayCommand"})

    @_catch_all_exceptions
    async def forward(self) -> None:
        """Fastforward."""
        await self.set_media({"type": "ForwardCommand"})

    @_catch_all_exceptions
    async def rewind(self) -> None:
        """Rewind."""
        await self.set_media({"type": "RewindCommand"})

    @_catch_all_exceptions
    async def set_volume(
        self,
        volume: float,
        customer_id: Optional[Text] = None,
        queue_delay: float = 1.5,
    ) -> None:
        """Set volume.

        Args:
        volume (float): The volume between 0 and 1.
        customer_id (string): CustomerId to use for sending. When none
                              specified this defaults to the logged in user.
        queue_delay (float, optional): The number of seconds to wait
                                        for commands to queue together.
                                        Defaults to 1.5.
                                        Must be positive.

        """
        await self.send_sequence(
            "Alexa.DeviceControls.Volume",
            customer_id=(
                self._login.customer_id if customer_id is None else customer_id
            ),
            value=volume * 100,
            queue_delay=queue_delay,
        )

    @_catch_all_exceptions
    async def shuffle(self, setting: bool) -> None:
        """Shuffle.

        setting (string) : true or false
        """
        await self.set_media({"type": "ShuffleCommand", "shuffle": setting})

    @_catch_all_exceptions
    async def repeat(self, setting: bool) -> None:
        """Repeat.

        setting (string) : true or false
        """
        await self.set_media({"type": "RepeatCommand", "repeat": setting})

    @_catch_all_exceptions
    async def get_state(self) -> Optional[Dict[Text, Any]]:
        """Get playing state."""
        response = await self._get_request(
            "/api/np/player?deviceSerialNumber="
            + self._device.device_serial_number
            + "&deviceType="
            + self._device._device_type
            + "&screenWidth=2560"
        )
        return await response.json(content_type=None) if response else None

    @_catch_all_exceptions
    async def set_dnd_state(self, state: bool) -> None:
        """Set Do Not Disturb state.

        Args:
        state (boolean): true or false

        Returns json

        """
        data = {
            "deviceSerialNumber": self._device.device_serial_number,
            "deviceType": self._device._device_type,
            "enabled": state,
        }
        _LOGGER.debug(
            "%s: Setting DND state: %s data: %s",
            hide_email(self._login.email),
            state,
            json.dumps(data),
        )
        response = await self._put_request("/api/dnd/status", data=data)
        response_json = await response.json(content_type=None) if response else None
        success = data == response_json
        _LOGGER.debug(
            "%s: Success: %s Response: %s",
            hide_email(self._login.email),
            success,
            response_json,
        )
        return success

    @staticmethod
    @_catch_all_exceptions
    async def get_bluetooth(login) -> Optional[Dict[Text, Any]]:
        """Get paired bluetooth devices."""
        response = await AlexaAPI._static_request(
            "get", login, "/api/bluetooth", query={"cached": "false"}
        )
        return await response.json(content_type=None) if response else None

    @_catch_all_exceptions
    async def set_bluetooth(self, mac: Text) -> None:
        """Pair with bluetooth device with mac address."""
        await self._post_request(
            "/api/bluetooth/pair-sink/"
            + self._device._device_type
            + "/"
            + self._device.device_serial_number,
            data={"bluetoothDeviceAddress": mac},
        )

    @_catch_all_exceptions
    async def disconnect_bluetooth(self) -> None:
        """Disconnect all bluetooth devices."""
        await self._post_request(
            "/api/bluetooth/disconnect-sink/"
            + self._device._device_type
            + "/"
            + self._device.device_serial_number,
            data=None,
        )

    @staticmethod
    @_catch_all_exceptions
    async def get_devices(login: AlexaLogin) -> Optional[Dict[Text, Any]]:
        """Identify all Alexa devices."""
        response = await AlexaAPI._static_request(
            "get", login, "/api/devices-v2/device", query=None
        )
        AlexaAPI.devices[login.email] = (
            (await response.json(content_type=None))["devices"]
            if response
            else AlexaAPI.devices[login.email]
        )
        return AlexaAPI.devices[login.email]

    @staticmethod
    @_catch_all_exceptions
    async def get_authentication(login: AlexaLogin) -> Optional[Dict[Text, Any]]:
        """Get authentication json."""
        response = await AlexaAPI._static_request(
            "get", login, "/api/bootstrap", query=None
        )
        return (
            (await response.json(content_type=None))["authentication"]
            if response
            else None
        )

    @staticmethod
    @_catch_all_exceptions
    async def get_activities(
        login: AlexaLogin, items: int = 10
    ) -> Optional[Dict[Text, Any]]:
        """Get activities json."""
        response = await AlexaAPI._static_request(
            "get",
            login,
            "/api/activities",
            query={"startTime": "", "size": items, "offset": 1},
        )
        result = await response.json(content_type=None)
        return result["activities"] if result and result.get("activities") else None

    @staticmethod
    @_catch_all_exceptions
    async def get_device_preferences(login: AlexaLogin) -> Optional[Dict[Text, Any]]:
        """Identify all Alexa device preferences."""
        response = await AlexaAPI._static_request(
            "get", login, "/api/device-preferences", query={}
        )
        return await response.json(content_type=None) if response else None

    @staticmethod
    @_catch_all_exceptions
    async def get_automations(
        login: AlexaLogin, items: int = 1000
    ) -> Optional[Dict[Text, Any]]:
        """Identify all Alexa automations."""
        response = await AlexaAPI._static_request(
            "get", login, "/api/behaviors/v2/automations", query={"limit": items}
        )
        return await response.json(content_type=None) if response else None

    @staticmethod
    @_catch_all_exceptions
    async def get_last_device_serial(
        login: AlexaLogin, items: int = 10
    ) -> Optional[Dict[Text, Any]]:
        """Identify the last device's serial number and last summary.

        This will search the [last items] activity records and find the latest
        entry where Echo successfully responded.
        """
        response = await AlexaAPI.get_activities(login, items)
        if response is not None:
            for last_activity in response:
                # Ignore discarded activity records
                # Ignore empty description and summary
                summary = ""
                if (
                    last_activity["activityStatus"]
                    != "DISCARDED_NON_DEVICE_DIRECTED_INTENT"
                    and last_activity["description"]
                ):
                    try:
                        summary = json.loads(last_activity["description"]).get(
                            "summary", ""
                        )
                    except JSONDecodeError:
                        pass
                    return {
                        "serialNumber": (
                            last_activity["sourceDeviceIds"][0]["serialNumber"]
                        ),
                        "timestamp": last_activity["creationTimestamp"],
                        "summary": summary,
                    }
                if (
                    last_activity["activityStatus"]
                    != "DISCARDED_NON_DEVICE_DIRECTED_INTENT"
                    and last_activity["domainAttributes"]
                ):
                    try:
                        domain_attributes = json.loads(
                            last_activity["domainAttributes"]
                        ).get("nBestList", "")
                        domain_attributes = domain_attributes[0]
                        if isinstance(domain_attributes, dict):
                            summary = f'{domain_attributes.get("entryType")} {domain_attributes.get("bookTitle")}'
                    except (JSONDecodeError, TypeError):
                        pass
                    if domain_attributes.get("entryType") and domain_attributes.get(
                        "bookTitle"
                    ):
                        return {
                            "serialNumber": (
                                last_activity["sourceDeviceIds"][0]["serialNumber"]
                            ),
                            "timestamp": last_activity["creationTimestamp"],
                            "summary": summary,
                        }
        return None

    @_catch_all_exceptions
    async def set_guard_state(
        self, entity_id: Text, state: Text, queue_delay: float = 1.5
    ) -> None:
        """Set Guard state.

        Args:
        entity_id (Text): numeric ending of applianceId of RedRock Panel
        state (Text): AWAY, HOME
        queue_delay (float, optional): The number of seconds to wait
                                        for commands to queue together.
                                        Defaults to 1.5.
                                        Must be positive.
        Returns json

        """
        _LOGGER.debug(
            "%s: Setting Guard state: %s ", hide_email(self._login.email), state
        )

        await self.send_sequence(
            "controlGuardState",
            target=entity_id,
            operationId="controlGuardState",
            state=state,
            skillId="amzn1.ask.skill.f71a9b50-e99a-4669-a226-d50ebb5e0830",
            queue_delay=queue_delay,
        )

    @staticmethod
    @_catch_all_exceptions
    async def get_guard_state(
        login: AlexaLogin, entity_id: Text
    ) -> Optional[Dict[Text, Any]]:
        """Get state of Alexa guard.

        Args:
        login (AlexaLogin): Successfully logged in AlexaLogin
        entity_id (Text): applianceId of RedRock Panel

        Returns json

        """
        return await AlexaAPI.get_entity_state(login, appliance_ids=[entity_id])

    @staticmethod
    @_catch_all_exceptions
    async def get_entity_state(
        login: AlexaLogin,
        entity_ids: Optional[List[Text]] = None,
        appliance_ids: Optional[List[Text]] = None,
    ) -> Optional[Dict[Text, Any]]:
        """Get the current state of multiple appliances.

        Note that this can take both entity_ids and appliance_ids.
        If you have both pieces of data available, prefer the entity id. A single entity might have multiple
        appliance ids. Its easier to ensure you don't miss data by just providing entity id instead.

        Args:
        login (AlexaLogin): Successfully logged in AlexaLogin
        entity_ids (List[Text]): The list of entities you want information about.
        appliance_ids: (List[Text]): The list of appliances you want information about.

        Returns json

        """
        state_requests = []
        if entity_ids is not None:
            for entity_id in entity_ids:
                state_requests.append({"entityId": entity_id, "entityType": "ENTITY"})
        if appliance_ids is not None:
            for appliance_id in appliance_ids:
                state_requests.append(
                    {"entityId": appliance_id, "entityType": "APPLIANCE"}
                )
        data = {"stateRequests": state_requests}
        response = await AlexaAPI._static_request(
            "post", login, "/api/phoenix/state", data=data
        )
        result = await response.json(content_type=None) if response else None
        _LOGGER.debug(
            "%s: get_entity_state response: %s", hide_email(login.email), result
        )
        return result

    @staticmethod
    @_catch_all_exceptions
    async def static_set_guard_state(
        login: AlexaLogin, entity_id: Text, state: Text
    ) -> Optional[Dict[Text, Any]]:
        """Set state of Alexa guard.

        Args:
        login (AlexaLogin): Successfully logged in AlexaLogin
        entity_id (Text): entityId of RedRock Panel
        state (Text): ARMED_AWAY, ARMED_STAY

        Returns json

        """
        parameters = {"action": "controlSecurityPanel", "armState": state}
        data = {
            "controlRequests": [
                {
                    "entityId": entity_id,
                    "entityType": "APPLIANCE",
                    "parameters": parameters,
                }
            ]
        }
        response = await AlexaAPI._static_request(
            "put", login, "/api/phoenix/state", data=data
        )
        _LOGGER.debug(
            "%s: set_guard_state response: %s for data: %s ",
            hide_email(login.email),
            await response.json(content_type=None) if response else None,
            json.dumps(data),
        )
        return await response.json(content_type=None) if response else None

    @staticmethod
    @_catch_all_exceptions
    async def set_light_state(
        login: AlexaLogin,
        entity_id: Text,
        power_on: bool = True,
        brightness: Optional[int] = None,
        color_name: Optional[Text] = None,
        color_temperature_name: Optional[Text] = None,
    ) -> Optional[Dict[Text, Any]]:
        """Set state of a light.

        Args:
        login (AlexaLogin): Successfully logged in AlexaLogin
        entity_id (Text): Entity ID of The light. Not the Application ID.
        power_on (bool): Should the light be on or off.
        brightness (Optional[int]): 0-100 or None to leave as is
        color_name (Optional[Text]): The name of a color that Alexa supports in snake case.
        color_temperature_name (Optional[Text]): The name of a color temperature name that Alexa supports in snake case.

        Returns json

        """
        control_requests = [
            {
                "entityId": entity_id,
                "entityType": "ENTITY",
                "parameters": {"action": "turnOn" if power_on else "turnOff"},
            }
        ]

        if brightness is not None and 0 <= brightness <= 100:
            control_requests.append(
                {
                    "entityId": entity_id,
                    "entityType": "ENTITY",
                    "parameters": {
                        "action": "setBrightness",
                        "brightness": str(brightness),
                    },
                }
            )

        if color_name is not None:
            control_requests.append(
                {
                    "entityId": entity_id,
                    "entityType": "ENTITY",
                    "parameters": {"action": "setColor", "colorName": color_name},
                }
            )

        if color_temperature_name is not None:
            control_requests.append(
                {
                    "entityId": entity_id,
                    "entityType": "ENTITY",
                    "parameters": {
                        "action": "setColorTemperature",
                        "colorTemperatureName": color_temperature_name,
                    },
                }
            )

        data = {"controlRequests": control_requests}

        response = await AlexaAPI._static_request(
            "put", login, "/api/phoenix/state", data=data
        )
        _LOGGER.debug(
            "%s: set_light_state response: %s for data: %s ",
            hide_email(login.email),
            await response.json(content_type=None) if response else None,
            json.dumps(data),
        )
        return await response.json(content_type=None) if response else None

    @staticmethod
    @_catch_all_exceptions
    async def get_guard_details(login: AlexaLogin) -> Optional[Dict[Text, Any]]:
        """Get Alexa Guard details.

        Args:
        login (AlexaLogin): Successfully logged in AlexaLogin

        Returns json

        """
        response = await AlexaAPI._static_request("get", login, "/api/phoenix")
        # _LOGGER.debug("%s: Response: %s", hide_email(login.email),
        #               await response.json(content_type=None))
        return (
            json.loads((await response.json(content_type=None))["networkDetail"])
            if response
            else None
        )

    @staticmethod
    @_catch_all_exceptions
    async def get_network_details(login: AlexaLogin) -> Optional[Dict[Text, Any]]:
        """Get the network of devices that Alexa is aware of. This is the same as calling get_guard_details().

        Args:
        login: (AlexaLogin): Successfully logged in AlexaLogin

        Returns json
        """
        network_detail = await AlexaAPI.get_guard_details(login)
        _LOGGER.debug(
            "%s: get_network_details response: %s",
            hide_email(login.email),
            network_detail,
        )
        return network_detail

    @staticmethod
    @_catch_all_exceptions
    async def get_notifications(login: AlexaLogin) -> Optional[Dict[Text, Any]]:
        """Get Alexa notifications.

        Args:
        login (AlexaLogin): Successfully logged in AlexaLogin

        Returns json

        """
        response = await AlexaAPI._static_request("get", login, "/api/notifications")
        # _LOGGER.debug("%s: Response: %s", hide_email(login.email),
        #               response.json(content_type=None))
        return (
            (await response.json(content_type=None))["notifications"]
            if response
            else None
        )

    @staticmethod
    @_catch_all_exceptions
    async def set_notifications(login: AlexaLogin, data) -> Optional[Dict[Text, Any]]:
        """Update Alexa notification.

        Args:
        login (AlexaLogin): Successfully logged in AlexaLogin
        data : Data to pass to notifications

        Returns json

        """
        response = await AlexaAPI._static_request(
            "put", login, "/api/notifications", data=data
        )
        # _LOGGER.debug("%s: Response: %s", hide_email(login.email),
        #               response.json(content_type=None))
        return await response.json(content_type=None) if response else None

    @staticmethod
    @_catch_all_exceptions
    async def get_dnd_state(login: AlexaLogin) -> Optional[Dict[Text, Any]]:
        """Get Alexa DND states.

        Args:
        login (AlexaLogin): Successfully logged in AlexaLogin

        Returns json

        """
        response = await AlexaAPI._static_request(
            "get", login, "/api/dnd/device-status-list",
        )
        return await response.json(content_type=None) if response else None

    @staticmethod
    @_catch_all_exceptions
    async def clear_history(login: AlexaLogin, items: int = 50) -> bool:
        """Clear entries in history."""
        email = login.email
        response = await AlexaAPI._static_request(
            "get", login, "/api/activities", query={"size": items, "offset": -1}
        )
        import urllib.parse  # pylint: disable=import-outside-toplevel

        completed = True
        result = await response.json(content_type=None)
        response_json = (
            result["activities"] if result and result.get("activities") else None
        )
        if not response_json:
            _LOGGER.debug("%s: No history to delete.", hide_email(email))
            return True
        _LOGGER.debug(
            "%s:Attempting to delete %s items from history",
            hide_email(email),
            len(response_json),
        )
        for activity in response_json:
            response = await AlexaAPI._static_request(
                "delete",
                login,
                f"/api/activities/{urllib.parse.quote_plus(activity['id'])}",
            )
            if response.status == 404:
                _LOGGER.warning(
                    (
                        "%s:Unable to delete %s: %s: \n"
                        "There is no voice recording to delete. "
                        "Please manually delete the entry in the Alexa app."
                    ),
                    hide_email(email),
                    activity["id"],
                    response.reason,
                )
                completed = False
            elif response.status == 200:
                _LOGGER.debug(
                    "%s: Succesfully deleted %s", hide_email(email), activity["id"],
                )
        return completed

    @_catch_all_exceptions
    async def set_background(self, url: Text) -> bool:
        """Set background for Echo Show.

        Sets the background to Alexa App Photo with the specific https url.

        Args
        url (URL): valid https url for the image

        Returns
        Whether the command was successful.

        """
        data = {
            "deviceSerialNumber": self._device.device_serial_number,
            "deviceType": self._device._device_type,
            "backgroundImageID": "JqIFZhtBTx25wLGTJGdNGQ",
            "backgroundImageType": "PERSONAL_PHOTOS",
            "backgroundImageURL": url,
        }
        _LOGGER.debug(
            "%s: Setting background of %s to: %s",
            hide_email(self._login.email),
            self._device,
            url,
        )
        if url.startswith("http://"):
            _LOGGER.warning("Background URL should be a valid https image")
        response = await self._post_request("/api/background-image", data=data)
        response_json = await response.json(content_type=None) if response else None
        success = response.status == 200
        _LOGGER.debug(
            "%s: Success: %s Response: %s",
            hide_email(self._login.email),
            success,
            response_json,
        )
        return success

    @staticmethod
    @_catch_all_exceptions
    async def force_logout() -> None:
        """Force logout.

        Raises
            AlexapyLoginError: Raise AlexapyLoginError

        """
        raise AlexapyLoginError("Forced Logout")

    @staticmethod
    @_catch_all_exceptions
    async def ping(login: AlexaLogin) -> Optional[Dict[Text, Any]]:
        """Ping.

        Args:
        login (AlexaLogin): Successfully logged in AlexaLogin

        Returns json

        """
        response = await AlexaAPI._static_request("get", login, "/api/ping",)
        return await response if response else None
