"""Python Package for controlling Alexa devices (echo dot, etc) programmatically.

SPDX-License-Identifier: Apache-2.0

This provides a login by proxy method.
Built on https://github.com/alandtse/auth_capture_proxy

For more details about this api, please refer to the documentation at
https://gitlab.com/keatontaylor/alexapy
"""
from functools import partial
import logging
from typing import Optional, Text, Union

import authcaptureproxy
from bs4 import BeautifulSoup
from yarl import URL

from alexapy.alexalogin import AlexaLogin
from alexapy.helpers import hide_email, hide_password

_LOGGER = logging.getLogger(__name__)


class AlexaProxy(authcaptureproxy.AuthCaptureProxy):
    """Class to handle proxy login connections to Alexa."""

    def __init__(self, login: AlexaLogin, base_url: Text) -> None:
        """Initialize proxy object.

        Args:
            login (AlexaLogin): AlexaLogin object to update after completion of proxy.
            base_url (Text): base url for proxy location. e.g., http://192.168.1.1

        """
        super().__init__(URL(base_url), URL(login.start_url))
        self._login: AlexaLogin = login
        self._config_flow_id = None
        self._callback_url = None
        self.tests = {"test_amazon_url": self.test_amazon_url}
        self.modifiers = {
            "autofill": partial(
                self.autofill,
                {
                    "email": self._login.email,
                    "password": self._login.password,
                    "otpCode": self._login.get_totp_token(),
                },
            )
        }

    async def test_amazon_url(self, resp, data, query) -> Optional[Union[URL, Text]]:
        """Test for Alexa success.

        Args
            resp (httpx.Response): The aiohttp response.
            data (Dict[Text, Any]): Dictionary of all post data captured through proxy with overwrites for duplicate keys.
            query (Dict[Text, Any]): Dictionary of all query data with overwrites for duplicate keys.

        Returns
            Optional[Union[URL, Text]]: URL for a http 302 redirect or Text to display on success. None indicates test did not pass.

        """
        if URL(str(resp.url)).path in ["/ap/maplanding", "/spa/index.html"]:
            self._login.session.cookie_jar.update_cookies(self.session.cookies)
            self._login.access_token = URL(str(resp.url)).query.get(
                "openid.oa2.access_token"
            )
            self._config_flow_id = self.init_query.get("config_flow_id")
            self._callback_url = self.init_query.get("callback_url")
            # Reset so proxy can be reused
            # Unfortunately because the route has a handler bound and cannot be changed, we need to remove the modifiers for other proxies.
            await self.reset_data()
            if self._callback_url:
                return URL(self._callback_url)
            return f"Successfully logged in as {self._login.email} for flow {self._config_flow_id}. Please close the window."

    def change_login(self, login: AlexaLogin) -> None:
        """Change login.

        Args:
            login (AlexaLogin): AlexaLogin object to update after completion of proxy.
        """
        self._login = login
        self.tests = {"test_amazon_url": self.test_amazon_url}
        self.modifiers = {
            "autofill": partial(
                self.autofill,
                {
                    "email": self._login.email,
                    "password": self._login.password,
                    "otpCode": self._login.get_totp_token(),
                },
            )
        }

    def autofill(self, items: dict, html: Text) -> Text:
        """Autofill input tags in form in html.

        Args
            html (Text): html to convert
            items (dict): Dictionary of values to fill

        Returns
            Text: html with values filled in

        """
        soup: BeautifulSoup = BeautifulSoup(html, "html.parser")
        for item, value in items.items():
            for html_tag in soup.find_all(attrs={"name": item}):
                if not html_tag.get("value"):
                    html_tag["value"] = value
                    if self._login._debug:
                        _LOGGER.debug(
                            "Filled %s",
                            str(html_tag).replace(
                                value,
                                hide_password(value)
                                if item == "password"
                                else hide_email(value)
                                if item == "email"
                                else value,
                            ),
                        )
        return str(soup)
