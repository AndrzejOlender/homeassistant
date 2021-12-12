"""Python Package for controlling Alexa devices (echo dot, etc) programmatically.

SPDX-License-Identifier: Apache-2.0

Login class.

For more details about this api, please refer to the documentation at
https://gitlab.com/keatontaylor/alexapy
"""

import asyncio
import base64
import binascii
from binascii import Error
import datetime
from http.cookies import SimpleCookie
from json import JSONDecodeError, dumps
import logging
import os
import pickle
import re
import secrets
from typing import Any, Callable, Dict, List, Optional, Text, Tuple, Union
from urllib.parse import urlencode, urlparse

import aiofiles
from aiofiles import os as aioos
from bs4 import BeautifulSoup
import pyotp
from simplejson import JSONDecodeError as SimpleJSONDecodeError
from yarl import URL

from alexapy import aiohttp
from alexapy.aiohttp.client_exceptions import ContentTypeError

from .const import APP_NAME, EXCEPTION_TEMPLATE, LOCALE_KEY, USER_AGENT
from .errors import AlexapyPyotpInvalidKey
from .helpers import (
    _catch_all_exceptions,
    delete_cookie,
    hide_email,
    hide_serial,
    obfuscate,
)

_LOGGER = logging.getLogger(__name__)


class AlexaLogin:
    # pylint: disable=too-many-instance-attributes
    """Class to handle login connection to Alexa. This class will not reconnect.

    Args:
    url (string): Localized Amazon domain (e.g., amazon.com)
    email (string): Amazon login account
    password (string): Password for Amazon login account
    outputpath (function): Local path with write access for storing files
    debug (boolean): Enable additional debugging including debug file creation
    otp_secret (string): TOTP Secret key for automatic 2FA filling
    uuid: (string): Unique 32 char hex to serve as app serial number for registration

    """

    def __init__(
        self,
        url: Text,
        email: Text,
        password: Text,
        outputpath: Callable[[Text], Text],
        debug: bool = False,
        otp_secret: Text = "",
        oauth: Optional[Dict[Any, Any]] = None,
        uuid: Optional[Text] = None,
        oauth_login: bool = True,
    ) -> None:
        # pylint: disable=too-many-arguments,import-outside-toplevel
        """Set up initial connection and log in."""
        import ssl

        import certifi

        oauth = oauth or {}
        self._hass_domain: Text = "alexa_media"
        self._prefix: Text = "https://alexa."
        self._url: Text = url
        self._email: Text = email
        self._password: Text = password
        self._session: Optional[aiohttp.ClientSession] = None
        self._ssl = ssl.create_default_context(
            purpose=ssl.Purpose.SERVER_AUTH, cafile=certifi.where()
        )
        self._headers: Dict[Text, Text] = {}
        self._data: Optional[Dict[Text, Text]] = None
        self.status: Optional[Dict[Text, Union[Text, bool]]] = {}
        self.stats: Optional[Dict[Text, Union[Text, bool]]] = {
            "login_timestamp": datetime.datetime(1, 1, 1),
            "api_calls": 0,
        }
        self._outputpath = outputpath
        self._cookiefile: List[Text] = [
            self._outputpath(f".storage/{self._hass_domain}.{self.email}.pickle"),
            self._outputpath(f"{self._hass_domain}.{self.email}.pickle"),
            self._outputpath(f".storage/{self._hass_domain}.{self.email}.txt"),
        ]
        self._debugpost: Text = outputpath(f"{self._hass_domain}{email}post.html")
        self._debugget: Text = outputpath(f"{self._hass_domain}{email}get.html")
        self._lastreq: Optional[aiohttp.ClientResponse] = None
        self._debug: bool = debug
        self._links: Optional[Dict[Text, Tuple[Text, Text]]] = {}
        self._options: Optional[Dict[Text, Text]] = {}
        self._site: Optional[Text] = None
        self._close_requested = False
        self._customer_id: Optional[Text] = None
        self._totp: Optional[pyotp.TOTP] = None
        self.set_totp(otp_secret.replace(" ", ""))
        self.access_token: Optional[Text] = oauth.get("access_token")
        self.refresh_token: Optional[Text] = oauth.get("refresh_token")
        self.mac_dms: Optional[Text] = None
        self.expires_in: Optional[float] = oauth.get("expires_in")
        self._oauth_lock: asyncio.Lock = asyncio.Lock()
        self.uuid = uuid  # needed to be unique but repeateable for device registration
        self.oauth_login: bool = oauth_login
        _LOGGER.debug(
            "Login created for %s - %s", obfuscate(self.email), self.url,
        )
        self._create_session()

    @property
    def email(self) -> Text:
        """Return email or mobile account for this Login."""
        return self._email

    @email.setter
    def email(self, value: Optional[Text]) -> None:
        """Set email."""
        self._email = value

    @property
    def password(self) -> Text:
        """Return password for this Login."""
        return self._password

    @password.setter
    def password(self, value: Optional[Text]) -> None:
        """Set password."""
        self._password = value

    @property
    def customer_id(self) -> Optional[Text]:
        """Return customer_id for this Login."""
        return self._customer_id

    @customer_id.setter
    def customer_id(self, value: Optional[Text]) -> None:
        self._customer_id = value

    @property
    def session(self) -> Optional[aiohttp.ClientSession]:
        """Return session for this Login."""
        return self._session

    @property
    def url(self) -> Text:
        """Return url for this Login."""
        return self._url

    @property
    def start_url(self) -> URL:
        """Return start url for this Login."""
        if self.oauth_login:
            site: URL = URL("https://www.amazon.com/ap/signin")
            deviceid: Text = f"{binascii.hexlify(secrets.token_hex(16).encode()).decode()}23413249564c5635564d32573831"
            query = {
                "openid.return_to": "https://www.amazon.com/ap/maplanding",
                "openid.assoc_handle": "amzn_dp_project_dee_ios",
                "openid.identity": "http://specs.openid.net/auth/2.0/identifier_select",
                "pageId": "amzn_dp_project_dee_ios",
                "accountStatusPolicy": "P1",
                "openid.claimed_id": "http://specs.openid.net/auth/2.0/identifier_select",
                "openid.mode": "checkid_setup",
                "openid.ns.oa2": "http://www.amazon.com/ap/ext/oauth/2",
                "openid.oa2.client_id": f"device:{deviceid}",
                "openid.ns.pape": "http://specs.openid.net/extensions/pape/1.0",
                "openid.oa2.response_type": "token",
                "openid.ns": "http://specs.openid.net/auth/2.0",
                "openid.pape.max_auth_age": "0",
                "openid.oa2.scope": "device_auth_access",
                "language": LOCALE_KEY.get(self.url.replace("amazon", ""))
                if LOCALE_KEY.get(self.url.replace("amazon", ""))
                else "en_US",
            }
            site = site.update_query(query)
            _LOGGER.debug("Attempting oauth login to %s", site)
        else:
            site: URL = URL(self._prefix + self.url)
            self._headers["authority"] = f"www.{self._url}"
        return site

    @property
    def lastreq(self) -> Optional[aiohttp.ClientResponse]:
        """Return last response for last request for this Login."""
        return self._lastreq

    @property
    def close_requested(self) -> bool:
        """Return whether this Login has been asked to close."""
        return self._close_requested

    @property
    def links(self) -> Text:
        """Return string list of links from last page for this Login."""
        result = ""
        assert self._links is not None
        for key, value in self._links.items():
            result += f"link{key}:{value[0]}\n"
        return result

    def set_totp(self, otp_secret: Text) -> Optional[pyotp.TOTP]:
        """Enable a TOTP generator for the login.

        Args
            otp_secret (Text): Secret. If blank, it will remove the TOTP entry.

        Returns
            Optional[pyotp.TOTP]: The pyotp TOTP object

        """
        if otp_secret:
            _LOGGER.debug("Creating TOTP for %s", hide_serial(otp_secret))
            try:
                self._totp = pyotp.TOTP(otp_secret)
                self.get_totp_token()
            except Error as ex:
                self._totp = None
                _LOGGER.warning(
                    "Error creating TOTP; %s likely invalid", hide_serial(otp_secret)
                )
                raise AlexapyPyotpInvalidKey(ex) from ex
            except AttributeError:
                self._totp = None
                _LOGGER.warning("Error creating TOTP; pyotp version likely outdated",)
        else:
            self._totp = None
        return self._totp

    def get_totp_token(self) -> Text:
        """Generate Timed based OTP token.

        Returns
            Text: OTP for current time.

        """
        if self._totp:
            token: Text = self._totp.now()
            _LOGGER.debug("Generating OTP %s", token)
            return token
        _LOGGER.debug("Unable to generate OTP; 2FA app key not configured")
        return ""

    async def load_cookie(self, cookies_txt: Text = "") -> Optional[Dict[Text, Text]]:
        # pylint: disable=import-outside-toplevel
        """Load cookie from disk."""
        from collections import defaultdict
        import http.cookiejar

        from requests.cookies import RequestsCookieJar

        cookies: Optional[
            Union[RequestsCookieJar, http.cookiejar.MozillaCookieJar]
        ] = None
        return_cookies = {}
        numcookies: int = 0
        loaded: bool = False
        if self._cookiefile:
            if cookies_txt:
                _LOGGER.debug(
                    "Saving passed in cookie to %s\n%s",
                    self._cookiefile[0],
                    repr(cookies_txt),
                )
                async with aiofiles.open(self._cookiefile[0], mode="w") as localfile:
                    try:
                        await localfile.write(cookies_txt)
                    except (OSError, EOFError, TypeError, AttributeError) as ex:
                        _LOGGER.debug(
                            "Error saving passed in cookie to %s: %s",
                            self._cookiefile[0],
                            EXCEPTION_TEMPLATE.format(type(ex).__name__, ex.args),
                        )
            for cookiefile in self._cookiefile:
                _LOGGER.debug("Searching for cookies from %s", cookiefile)
                if loaded:
                    break
                numcookies = 0
                if not os.path.exists(cookiefile):
                    continue
                if loaded and cookiefile != self._cookiefile[0]:
                    await delete_cookie(cookiefile)
                _LOGGER.debug("Trying to load cookie from file %s", cookiefile)
                try:
                    async with aiofiles.open(cookiefile, "rb") as myfile:
                        cookies = pickle.loads(await myfile.read())
                        if self._debug:
                            _LOGGER.debug(
                                "Pickled cookie loaded: %s %s", type(cookies), cookies
                            )
                except (pickle.UnpicklingError):
                    try:
                        cookies = http.cookiejar.MozillaCookieJar(cookiefile)
                        cookies.load(ignore_discard=True, ignore_expires=True)
                        if self._debug:
                            _LOGGER.debug(
                                "Mozilla cookie loaded: %s %s", type(cookies), cookies
                            )
                    except (ValueError, http.cookiejar.LoadError) as ex:
                        _LOGGER.debug(
                            "Cookie %s is truncated: %s",
                            cookiefile,
                            EXCEPTION_TEMPLATE.format(type(ex).__name__, ex.args),
                        )
                        continue
                except (OSError, EOFError) as ex:
                    _LOGGER.debug(
                        "Error loading cookie from %s: %s",
                        cookiefile,
                        EXCEPTION_TEMPLATE.format(type(ex).__name__, ex.args),
                    )
                    continue
                if isinstance(cookies, RequestsCookieJar):
                    _LOGGER.debug("Loading RequestsCookieJar")
                    cookies = cookies.get_dict()
                    assert cookies is not None
                    for key, value in cookies.items():
                        if self._debug:
                            _LOGGER.debug('Key: "%s", Value: "%s"', key, value)
                        # escape extra quote marks from Requests cookie
                        return_cookies[str(key)] = value.strip('"')
                    numcookies = len(return_cookies)
                elif isinstance(cookies, defaultdict):
                    _LOGGER.debug("Trying to load aiohttpCookieJar to session")
                    cookie_jar: aiohttp.CookieJar = self._session.cookie_jar
                    try:
                        cookie_jar.load(cookiefile)
                        return_cookies = self._get_cookies_from_session()
                        numcookies = len(return_cookies)
                    except (OSError, EOFError, TypeError, AttributeError) as ex:
                        _LOGGER.debug(
                            "Error loading aiohttpcookie from %s: %s",
                            cookiefile,
                            EXCEPTION_TEMPLATE.format(type(ex).__name__, ex.args),
                        )
                        # a cookie_jar.load error can corrupt the session
                        # so we must recreate it
                        self._create_session(True)
                elif isinstance(cookies, dict):
                    _LOGGER.debug("Found dict cookie")
                    return_cookies = cookies
                    numcookies = len(return_cookies)
                elif isinstance(cookies, http.cookiejar.MozillaCookieJar):
                    _LOGGER.debug("Found Mozillacookiejar")
                    for cookie in cookies:
                        if self._debug:
                            _LOGGER.debug(
                                "Processing cookie %s expires: %s",
                                cookie,
                                cookie.expires,
                            )
                        # escape extra quote marks from MozillaCookieJar cookie
                        return_cookies[cookie.name] = cookie.value.strip('"')
                    numcookies = len(return_cookies)
                else:
                    _LOGGER.debug("Ignoring unknown file %s", type(cookies))
                if numcookies:
                    _LOGGER.debug("Loaded %s cookies", numcookies)
                    loaded = True
                    if cookiefile != self._cookiefile[0]:
                        _LOGGER.debug(
                            "Migrating old cookiefile to %s ", self._cookiefile[0]
                        )
                        try:
                            await aioos.rename(cookiefile, self._cookiefile[0])
                        except (OSError, EOFError, TypeError, AttributeError) as ex:
                            _LOGGER.debug(
                                "Error moving cookie from %s to %s: %s",
                                cookiefile,
                                self._cookiefile[0],
                                EXCEPTION_TEMPLATE.format(type(ex).__name__, ex.args),
                            )
        return return_cookies

    async def close(self) -> None:
        """Close connection for login."""
        self._close_requested = True
        if self._session and not self._session.closed:
            if self._session._connector_owner:
                assert self._session._connector is not None
                await self._session._connector.close()
            self._session._connector = None

    async def reset(self) -> None:
        # pylint: disable=import-outside-toplevel
        """Remove data related to existing login."""
        _LOGGER.debug("Resetting Login for %s - %s", self.email, self.url)
        await self.close()
        self._session = None
        self._data = None
        self._lastreq = None
        self.status = {}
        self._links = {}
        self._options = {}
        self._site = None
        self._create_session()
        self._close_requested = False

        for cookiefile in self._cookiefile:
            if (cookiefile) and os.path.exists(cookiefile):
                await delete_cookie(cookiefile)

    @classmethod
    def get_inputs(cls, soup: BeautifulSoup, searchfield=None) -> Dict[str, str]:
        """Parse soup for form with searchfield."""
        searchfield = searchfield or {"name": "signIn"}
        data = {}
        form = soup.find("form", searchfield)
        if not form:
            form = soup.find("form")
        for field in form.find_all("input"):
            try:
                data[field["name"]] = ""
                if field["type"] and field["type"] == "hidden":
                    data[field["name"]] = field["value"]
            except BaseException:  # pylint: disable=broad-except
                pass
        return data

    async def test_loggedin(self, cookies: Union[Dict[str, str], None] = None) -> bool:
        # pylint: disable=import-outside-toplevel
        """Function that will test the connection is logged in.

        Tests:
        - Attempts to get authenticaton and compares to expected login email
        Returns false if unsuccesful getting json or the emails don't match
        Returns false if no csrf found; necessary to issue commands
        """
        if self._debug:
            _LOGGER.debug("Testing whether logged in to alexa.%s", self._url)
            _LOGGER.debug("Cookies: %s", cookies)
            _LOGGER.debug("Session Cookies:\n%s", self._print_session_cookies())
            _LOGGER.debug("Header: %s", dumps(self._headers))
        if not self._session:
            self._create_session()
        await self.get_tokens()
        await self.exchange_token_for_cookies()
        await self.get_csrf()
        get_resp = await self._session.get(
            self._prefix + "amazon.com" + "/api/bootstrap",
            cookies=cookies,
            ssl=self._ssl,
        )
        email = None
        json = None
        await self._process_resp(get_resp)
        try:
            json = await get_resp.json()
            email = json["authentication"]["customerEmail"]
        except (JSONDecodeError, SimpleJSONDecodeError, ContentTypeError) as ex:
            _LOGGER.debug(
                "Not logged in: %s",
                EXCEPTION_TEMPLATE.format(type(ex).__name__, ex.args),
            )
            if self.url.lower() == "amazon.com":
                return False
        # Convert from amazon.com domain to native domain
        if self.url.lower() != "amazon.com":
            self._headers["authority"] = f"www.{self._url}"
            get_resp = await self._session.get(
                self._prefix + self._url + "/api/bootstrap",
            )
            await self._process_resp(get_resp)
            try:
                json = await get_resp.json()
                email = json["authentication"]["customerEmail"]
            except (JSONDecodeError, SimpleJSONDecodeError, ContentTypeError) as ex:
                _LOGGER.debug(
                    "Not logged in: %s",
                    EXCEPTION_TEMPLATE.format(type(ex).__name__, ex.args),
                )
                return False
        self.customer_id = json.get("authentication", {}).get("customerId")
        if (email and email.lower() == self.email.lower()) or "@" not in self.email:
            if "@" in self.email:
                _LOGGER.debug(
                    "Logged in as %s to %s with id: %s",
                    email,
                    self.url,
                    self.customer_id,
                )
            else:
                _LOGGER.debug(
                    "Logged in as to %s mobile account %s with %s",
                    email,
                    self.url,
                    self.customer_id,
                )
            self.stats["login_timestamp"] = datetime.datetime.now()
            self.stats["api_calls"] = 0
            await self.check_domain()
            await self.save_cookiefile()
            return True
        _LOGGER.debug(
            "Not logged in due to email mismatch to stored %s", hide_email(email)
        )
        await self.reset()
        return False

    def _create_session(self, force=False) -> None:
        if not self._session or force:
            #  define session headers
            if self.oauth_login:
                self._headers = {
                    "User-Agent": USER_AGENT,
                    # "User-Agent": (
                    #     "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 PitanguiBridge/2.2.345247.0-[HARDWARE=iPhone10_4][SOFTWARE=13.5.1]"
                    # ),
                    "Accept": ("*/*"),
                    "Accept-Language": "*",
                    "DNT": "1",
                    "Upgrade-Insecure-Requests": "1",
                    # "authority": "www.amazon.com",
                }
            else:
                self._headers = {
                    "User-Agent": (
                        "Mozilla/5.0 (iPhone; CPU iPhone OS 13_5_1 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148 PitanguiBridge/2.2.345247.0-[HARDWARE=iPhone10_4][SOFTWARE=13.5.1]"
                    ),
                    "Accept": ("*/*"),
                    "Accept-Language": "*",
                    "DNT": "1",
                    "Upgrade-Insecure-Requests": "1",
                }
            #  initiate session
            self._session = aiohttp.ClientSession(headers=self._headers)

    def _get_cookies_from_session(self, site: Text = "") -> Dict[Text, Text]:
        """Return cookies from aiohttp session."""
        assert self._session
        if not site:
            site = self.url
        cookies = {}
        cookie_jar = self._session.cookie_jar
        cookies = cookie_jar.filter_cookies(URL(f"https://{site}"))
        return cookies

    def _print_session_cookies(self) -> Text:
        result: Text = ""
        if not self._session.cookie_jar:
            result = "Session cookie jar is empty."
        for cookie in self._session.cookie_jar:
            result += f"{cookie}\n"
        return result

    @_catch_all_exceptions
    async def login(
        self,
        cookies: Optional[Dict[Text, Text]] = None,
        data: Optional[Dict[Text, Optional[Text]]] = None,
    ) -> None:
        # pylint: disable=too-many-branches,too-many-locals,
        # pylint: disable=too-many-statements
        """Login to Amazon."""
        data = data or {}
        if cookies:
            _LOGGER.debug("Using cookies to log in")
            if await self.test_loggedin(cookies):
                await self.finalize_login()
                return
            await self.reset()
        _LOGGER.debug("Using credentials to log in")
        if not self._site:
            site: URL = self.start_url
        else:
            site = self._site
        if not self._session:
            self._create_session()
        #  This will process links which is used for debug only to force going
        #  to other links.  Warning, chrome will cache any link parameters
        #  breaking the configuration flow until refresh on browser.
        digit = None
        for datum, value in data.items():
            if (
                value
                and str(value).startswith("link")
                and len(value) > 4
                and value[4:].isdigit()
            ):
                digit = str(value[4:])
                _LOGGER.debug("Found link selection %s in %s ", digit, datum)
                assert self._links is not None
                if self._links.get(digit):
                    (text, site) = self._links[digit]
                    data[datum] = None
                    _LOGGER.debug("Going to link with text: %s href: %s ", text, site)
                    _LOGGER.debug("%s reset to %s ", datum, data[datum])
        if not digit and self._lastreq is not None:
            assert self._lastreq is not None
            site = str(self._lastreq.url)
            _LOGGER.debug("Loaded last request to %s ", site)
            resp = self._lastreq
        else:
            resp = await self._session.get(
                site, headers=self._headers, ssl=self._ssl, params=self._data
            )
            self._lastreq = resp
            site = await self._process_resp(resp)
        html: Text = await resp.text()
        if self._debug:
            async with aiofiles.open(self._debugget, mode="wb") as localfile:
                await localfile.write(await resp.read())
        # This commented block can be used to read a file directly to process.
        # async with aiofiles.open(
        #     "/config/anti-automation-js.html", "rb"
        #     "/config/Amazon-Password-Assistance.html", "rb"
        #     "/config/password_reset_required.html", "rb"
        # ) as myfile:
        #     html = await myfile.read()
        site = await self._process_page(html, site)
        if not self.status.get("ap_error"):
            missing_params = self._populate_data(site, data)
            if self._debug:
                if missing_params:
                    _LOGGER.debug(
                        "WARNING: Detected missing params: %s",
                        [k for (k, v) in self._data.items() if v == ""],
                    )
                _LOGGER.debug("Session Cookies:\n%s", self._print_session_cookies())
                _LOGGER.debug("Submit Form Data: %s", dumps(obfuscate(self._data)))
                _LOGGER.debug("Header: %s", dumps(self._headers))

            # submit post request with username/password and other needed info
            post_resp = None
            if self.status.get("force_get"):
                if not self.status.get("approval") and not self.status.get(
                    "action_required"
                ):
                    post_resp = await self._session.get(
                        site, params=self._data, headers=self._headers, ssl=self._ssl,
                    )
            else:
                post_resp = await self._session.post(
                    site, data=self._data, headers=self._headers, ssl=self._ssl,
                )

            # headers need to be submitted to have the referer
            if post_resp:
                if self._debug:
                    async with aiofiles.open(self._debugpost, mode="wb") as localfile:
                        await localfile.write(await post_resp.read())
                self._lastreq = post_resp
                site = await self._process_resp(post_resp)
                self._site = await self._process_page(await post_resp.text(), site)

    async def save_cookiefile(self) -> None:
        """Save login session cookies to file."""
        self._cookiefile = [
            self._outputpath(f".storage/{self._hass_domain}.{self.email}.pickle"),
            self._outputpath(f"{self._hass_domain}.{self.email}.pickle"),
            self._outputpath(f".storage/{self._hass_domain}.{self.email}.txt"),
        ]
        for cookiefile in self._cookiefile:
            if cookiefile == self._cookiefile[0]:
                cookie_jar = self._session.cookie_jar
                assert isinstance(cookie_jar, aiohttp.CookieJar)
                if self._debug:
                    _LOGGER.debug("Saving cookie to %s", cookiefile)
                try:
                    cookie_jar.save(self._cookiefile[0])
                except (OSError, EOFError, TypeError, AttributeError) as ex:
                    _LOGGER.debug(
                        "Error saving pickled cookie to %s: %s",
                        self._cookiefile[0],
                        EXCEPTION_TEMPLATE.format(type(ex).__name__, ex.args),
                    )
            elif (cookiefile) and os.path.exists(cookiefile):
                _LOGGER.debug("Removing outdated cookiefile %s", cookiefile)
                await delete_cookie(cookiefile)
        if self._debug:
            _LOGGER.debug("Session Cookies:\n%s", self._print_session_cookies())

    async def get_tokens(self) -> bool:
        """Get access and refresh tokens after registering device using cookies.

        Returns:
            bool: True if successful.
        """
        if not self.access_token:
            _LOGGER.warning(
                "No access token found; falling back to credential login instead of oauth."
            )
            return False
        frc = base64.b64encode(secrets.token_bytes(313)).decode("ascii")
        map_md = base64.b64encode(
            '{"device_user_dictionary":[],"device_registration_data":{"software_version":"1"},"app_identifier":{"app_version":"2.2.223830","bundle_id":"com.amazon.echo"}}'.encode(
                "utf8"
            )
        ).decode("utf8")

        if self.url.lower() != "amazon.com":
            urls = [self.url, "amazon.com"]
        else:
            urls = [self.url]
        registered = False
        for url in urls:
            cookies = self._get_cookies_from_session(f"https://{url}")
            cookies["frc"] = frc
            cookies["map-md"] = map_md
            headers = {
                "Content-Type": "application/json",
                "Accept-Charset": "utf-8",
                "x-amzn-identity-auth-domain": f"api.{url}",
                "Connection": "keep-alive",
                "Accept": "*/*",
                "User-Agent": USER_AGENT,
                "Accept-Language": "en-US",
                # "Cookie": "; ".join(
                #     [str(x) + "=" + str(y) for x, y in self._cookies.items()]
                # ),
            }
            cookies_list = []
            for k, value in cookies.items():
                # if k == "csrf":
                #     continue
                cookies_list.append({"Value": value.value, "Name": k})
            data = {
                "requested_extensions": ["device_info", "customer_info"],
                "cookies": {"website_cookies": cookies_list, "domain": f".{url}"},
                "registration_data": {
                    "domain": "Device",
                    "app_version": "2.2.223830.0",
                    "device_type": "A2IVLV5VM2W81",
                    "device_name": f"%FIRST_NAME%'s%DUPE_STRATEGY_1ST%{APP_NAME}",
                    "os_version": "11.4.1",
                    "device_serial": "2cf947a5a093d686a30c33cb07a703fd"
                    if not self.uuid
                    else self.uuid,
                    "device_model": "iPhone",
                    "app_name": APP_NAME,
                    "software_version": "1",
                },
                "auth_data": {"access_token": self.access_token},
                "user_context_map": {"frc": frc},
                "requested_token_type": ["bearer", "mac_dms", "website_cookies"],
            }
            _LOGGER.debug("Attempting to register with %s", url)
            try:
                response = await self._session.post(
                    "https://api." + url + "/auth/register", json=data, headers=headers,
                )
            except aiohttp.ClientConnectorError:
                _LOGGER.debug("Fallback attempt to register with api.amazon.com")
                response = await self._session.post(
                    "https://api.amazon.com/auth/register", json=data, headers=headers,
                )
            _LOGGER.debug("auth response %s with \n%s", response, dumps(data))
            if response.status == 200:
                registered = True
                break
        if not registered:
            _LOGGER.debug("Unable to register with %s", urls)
            return False
        response = (await response.json()).get("response")
        if response.get("success"):
            _LOGGER.debug(
                "Successfully registered %s device with Amazon",
                response["success"]["extensions"]["device_info"]["device_name"],
            )
            if self._debug:
                _LOGGER.debug("Received registration data:\n%s", dumps(response))
            self.refresh_token = response["success"]["tokens"]["bearer"][
                "refresh_token"
            ]
            self.mac_dms = response["success"]["tokens"]["mac_dms"]
            old = self.access_token
            self.access_token = response["success"]["tokens"]["bearer"]["access_token"]
            self.expires_in = datetime.datetime.now().timestamp() + int(
                response["success"]["tokens"]["bearer"]["expires_in"]
            )
            if old != self.access_token:
                _LOGGER.debug(
                    "New access token received which expires at %s in %s",
                    datetime.datetime.fromtimestamp(self.expires_in),
                    datetime.datetime.fromtimestamp(self.expires_in)
                    - datetime.datetime.now(),
                )
            return True
        return False

    async def refresh_access_token(self) -> bool:
        """Refresh access token and expires in using refresh token.

        Returns
            bool: Return true if successful.

        """
        if not self.refresh_token:
            _LOGGER.debug("No refresh token found to get access_token")
            return False
        data = {
            "app_name": APP_NAME,
            "app_version": "2.2.223830.0",
            "di.sdk.version": "6.10.0",
            "source_token": self.refresh_token,
            "package_name": "com.amazon.echo",
            "di.hw.version": "iPhone",
            "platform": "iOS",
            "requested_token_type": "access_token",
            "source_token_type": "refresh_token",
            "di.os.name": "iOS",
            "di.os.version": "11.4.1",
            "current_version": "6.10.0",
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Charset": "utf-8",
            "x-amzn-identity-auth-domain": "api.amazon.com",
            "Connection": "keep-alive",
            "Accept": "*/*",
            "User-Agent": USER_AGENT,
            "Accept-Language": LOCALE_KEY.get(self.url.replace("amazon", ""))
            if LOCALE_KEY.get(self.url.replace("amazon", ""))
            else "en_US",
            # "Cookie": "; ".join(
            #     [str(x) + "=" + str(y) for x, y in self._cookies.items()]
            # ),
        }
        try:
            response = await self._session.post(
                "https://api." + self.url + "/auth/token", data=data, headers=headers,
            )
        except aiohttp.ClientConnectionError:
            _LOGGER.debug(
                "Fallback attempt to refresh access token with api.amazon.com"
            )
            response = await self._session.post(
                "https://api.amazon.com/auth/token", data=data, headers=headers,
            )
        _LOGGER.debug("refresh response %s with \n%s", response, dumps(data))
        if response.status != 200:
            if self._debug:
                _LOGGER.debug("Failed to refresh access token: %s", response)
            else:
                _LOGGER.debug("Failed to refresh access token")
            return False
        response = await response.json()
        if self._debug:
            _LOGGER.debug("Refresh token json:\n%s ", response)
        if response.get("access_token"):
            self.access_token = response.get("access_token")
            self.expires_in = datetime.datetime.now().timestamp() + int(
                response.get("expires_in")
            )
            _LOGGER.debug(
                "Successfully updated access_token which expires at %s in %s",
                datetime.datetime.fromtimestamp(self.expires_in),
                datetime.datetime.fromtimestamp(self.expires_in)
                - datetime.datetime.now(),
            )
            return True
        return False

    async def exchange_token_for_cookies(self) -> bool:
        """Generate new session cookies using refresh token.

        Returns
            bool: True if succesful

        """
        if not self.refresh_token:
            _LOGGER.debug("No refresh token found to get access token")
            return False
        data = {
            "di.os.name": "iOS",
            "app_version": "2.2.223830.0",
            "domain": f".{self.url}",
            "source_token": self.refresh_token,
            "requested_token_type": "auth_cookies",
            "source_token_type": "refresh_token",
            "di.hw.version": "iPhone",
            "di.sdk.version": "6.10.0",
            # "cookies": {},
            "app_name": APP_NAME,
            "di.os.version": "11.4.1",
        }
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Charset": "utf-8",
            # "x-amzn-identity-auth-domain": f"api.{self.url}",
            "Connection": "keep-alive",
            "Accept": "*/*",
            "User-Agent": USER_AGENT,
            "Accept-Language": LOCALE_KEY.get(self.url.replace("amazon", ""))
            if LOCALE_KEY.get(self.url.replace("amazon", ""))
            else "en_US",
            # "Cookie": "; ".join(
            #     [str(x) + "=" + str(y) for x, y in self._cookies.items()]
            # ),
        }
        try:
            response = await self._session.post(
                "https://www." + self.url + "/ap/exchangetoken/cookies",
                data=data,
                headers=headers,
            )
        except aiohttp.ClientConnectorError:
            _LOGGER.debug("Fallback attempt to exchange tokens with www.amazon.com")
            response = await self._session.post(
                "https://www.amazon.com/ap/exchangetoken/cookies",
                data=data,
                headers=headers,
            )
        if response.status != 200:
            if self._debug:
                _LOGGER.debug(
                    "Failed to exchange cookies for refresh token: %s", response
                )
            else:
                _LOGGER.debug("Failed to exchange cookies for refresh token")
            return False
        response = (await response.json()).get("response")
        if self._debug:
            _LOGGER.debug("Exchange cookie json %s ", response)
        success = False
        for domain, cookies in response["tokens"]["cookies"].items():
            # _LOGGER.debug("updating %s with %s", domain, cookies)
            for item in cookies:
                raw_cookie = SimpleCookie()
                cookie_name = item["Name"]
                raw_cookie[item["Name"]] = (
                    item["Value"]
                    if not (
                        item["Value"].startswith('"') and item["Value"].endswith('"')
                    )
                    # Strings are returned within quotations, strip them
                    else item["Value"][1:-1]
                )
                for name, value in item.items():
                    if name in ["Name", "Value"]:
                        continue
                    raw_cookie[cookie_name][name] = f"{value}; Domain={domain}"
                # _LOGGER.debug("updating jar with cookie %s", raw_cookie)
                self._session.cookie_jar.update_cookies(raw_cookie, URL(domain))
            _LOGGER.debug(
                "%s cookies successfully exchanged for refresh token for domain %s",
                len(cookies),
                domain,
            )
            success = True
        return success

    async def get_csrf(self) -> bool:
        """Generate csrf if missing.

        Returns
            bool: True if csrf is found

        """
        cookies = self._get_cookies_from_session()
        if cookies.get("csrf"):
            _LOGGER.debug("CSRF already exists; no need to discover")
            return True
        _LOGGER.debug("Attempting to discover CSRF token")
        csrf_urls = [
            "/spa/index.html",
            "/api/language",
            "/api/devices-v2/device?cached=false",
            "/templates/oobe/d-device-pick.handlebars",
            "/api/strings",
        ]
        for url in csrf_urls:
            failed = False
            response = None
            try:
                response = await self._session.get(f"{self._prefix}{self.url}{url}")
            except aiohttp.ClientConnectionError:
                failed = True
            if failed or response and response.status != 200:
                if self._debug:
                    _LOGGER.debug("Unable to load page for csrf: %s", response)
                continue
            cookies = self._get_cookies_from_session()
            if cookies.get("csrf"):
                _LOGGER.debug("CSRF token found from %s", url)
                return True
            _LOGGER.debug("CSRF token not found from %s", url)
        _LOGGER.debug("No csrf token found")
        return False

    async def check_domain(self) -> bool:
        """Check whether logged into appropriate login domain.

        Returns
            bool: True if in correct domain

        """
        headers = {
            "Content-Type": "application/x-www-form-urlencoded",
            "Accept-Charset": "utf-8",
            "x-amzn-identity-auth-domain": f"api.{self.url}",
            "Connection": "keep-alive",
            "Accept": "*/*",
            "User-Agent": USER_AGENT,
            "Accept-Language": "en-US",
        }
        response = await self._session.get(
            f"{self._prefix}{self.url}/api/users/me?platform=ios&version=2.2.223830.0",
            headers=headers,
        )
        if response.status != 200:
            if self._debug:
                _LOGGER.debug("Unable to check for domain; proceeding:\n%s", response)
            return True
        try:
            response = await response.json(content_type=None)
        except JSONDecodeError:
            if self._debug:
                _LOGGER.debug("Unable to check for domain; proceeding:\n%s", response)
            return True
        domain = response.get("marketPlaceDomainName")
        if self.url not in domain:
            _LOGGER.warning(
                "Domain %s does not match reported account domain %s; functionality is not likely to work, please fix",
                self.url,
                domain,
            )
            return False
        _LOGGER.debug("Domain %s matches reported account domain: %s", self.url, domain)
        return True

    async def _process_resp(self, resp) -> Text:
        if resp.history:
            for item in resp.history:
                _LOGGER.debug("%s: redirected from\n%s", item.method, item.url)
            self._headers["Referer"] = str(resp.url)
        url = str(resp.request_info.url)
        method = resp.request_info.method
        status = resp.status
        reason = resp.reason
        headers = resp.request_info.headers
        if self._debug:
            _LOGGER.debug(
                "%s: \n%s with\n%s\n returned %s:%s with response %s",
                method,
                url,
                headers,
                status,
                reason,
                resp.headers,
            )
        else:
            _LOGGER.debug(
                "%s: \n%s returned %s:%s with response %s",
                method,
                url,
                status,
                reason,
                resp.headers,
            )
        self._headers["Referer"] = str(url)
        return url

    async def _process_page(self, html: str, site: Text) -> Text:
        # pylint: disable=too-many-branches,too-many-locals,
        # pylint: disable=too-many-statements
        # pylint: disable=import-outside-toplevel
        """Process html to set login.status and find form post url."""

        def find_links() -> None:
            links = {}
            index = 0
            if links_tag:
                for link in links_tag:
                    if not link.string:
                        continue
                    string = link.string.strip()
                    href = link["href"]
                    # _LOGGER.debug("Found link: %s <%s>",
                    #               string,
                    #               href)
                    if href.startswith("/"):
                        links[str(index)] = (string, (self._prefix + self.url + href))
                        index += 1
                    elif href.startswith("http"):
                        links[str(index)] = (string, href)
                        index += 1
            if forms_tag:
                for form in forms_tag:
                    if (
                        form.get("method")
                        and form.get("method") == "get"
                        and form.get("action")
                    ):
                        string = form.get("id")
                        action = form.get("action")
                        params = {}
                        inputs = form.findAll("input")
                        for item in inputs:
                            if (
                                item
                                and item.get("type")
                                and item.get("type") == "hidden"
                            ):
                                params[item.get("name")] = item.get("value")
                        href = f"{self._prefix}{self.url}{action}?{urlencode(params)}"
                        links[str(index)] = (string, href)
                        index += 1
            if links:
                _LOGGER.debug("Links: %s", links)
            self._links = links

        _LOGGER.debug("Processing %s", site)
        site_url = URL(site)
        soup: BeautifulSoup = BeautifulSoup(html, "html.parser")

        status: Dict[Text, Union[Text, bool]] = {}

        #  Find tags to determine which path
        login_tag = soup.find("form", {"name": "signIn"})
        captcha_tag = soup.find(id="auth-captcha-image")
        securitycode_tag = soup.find(id="auth-mfa-otpcode")
        errorbox = (
            soup.find(id="auth-error-message-box")
            if soup.find(id="auth-error-message-box")
            else soup.find(id="auth-warning-message-box")
        )
        claimspicker_tag = soup.find("form", {"name": "claimspicker"})
        authselect_tag = soup.find("form", {"id": "auth-select-device-form"})
        verificationcode_tag = soup.find("form", {"action": "verify"})
        verification_captcha_tag = soup.find("img", {"alt": "captcha"})
        javascript_authentication_tag = soup.find("form", {"id": "pollingForm"})
        links_tag = soup.findAll("a", href=True)
        forms_tag = soup.findAll("form")
        form_tag = soup.find("form")
        missingcookies_tag = soup.find(id="ap_error_return_home")
        forgotpassword_tag = soup.find("form", {"name": "forgotPassword"})
        polling_tag = soup.find(id="updatedChannelDetails")
        if self._debug:
            find_links()

        # pull out Amazon error message

        if errorbox:
            error_message = errorbox.find("h4").string
            for list_item in errorbox.findAll("li"):
                error_message += list_item.find("span").string
            _LOGGER.debug("Error message: %s", error_message)
            status["error_message"] = error_message

        if login_tag and not captcha_tag:
            _LOGGER.debug("Found standard login page")
            #  scrape login page to get all the inputs required for login
            self._data = self.get_inputs(soup, {"name": "signIn"})
        elif captcha_tag is not None:
            _LOGGER.debug("Captcha requested")
            status["captcha_required"] = True
            status["captcha_image_url"] = captcha_tag.get("src")
            self._data = self.get_inputs(soup)

        elif securitycode_tag is not None:
            _LOGGER.debug("2FA requested")
            status["securitycode_required"] = True
            self._data = self.get_inputs(soup, {"id": "auth-mfa-form"})

        elif claimspicker_tag is not None:
            self._options = {}
            index = 0
            claims_message = ""
            options_message = ""
            for div in claimspicker_tag.findAll("div", "a-row"):
                claims_message += f"{div.text}\n"
            for label in claimspicker_tag.findAll("label"):
                value = (
                    (label.find("input")["value"]).strip()
                    if label.find("input")
                    else ""
                )
                message = (
                    (label.find("span").string).strip() if label.find("span") else ""
                )
                valuemessage = (
                    (f"* **`{index}`**:\t `{value} - {message}`.\n")
                    if value != ""
                    else ""
                )
                options_message += valuemessage
                if value:
                    self._options[str(index)] = value
                    index += 1
            _LOGGER.debug(
                "Verification method requested: %s, %s", claims_message, options_message
            )
            status["claimspicker_required"] = True
            status["claimspicker_message"] = options_message
            self._data = self.get_inputs(soup, {"name": "claimspicker"})
        elif authselect_tag is not None:
            self._options = {}
            index = 0
            authselect_message = ""
            authoptions_message = ""
            for div in soup.findAll("div", "a-box-inner"):
                if div.find("p"):
                    authselect_message += f"{div.find('p').string}\n"
            for label in authselect_tag.findAll("label"):
                value = (
                    (label.find("input")["value"]).strip()
                    if label.find("input")
                    else ""
                )
                message = (
                    (label.find("span").string).strip() if label.find("span") else ""
                )
                valuemessage = (f"{index}:\t{message}\n") if value != "" else ""
                authoptions_message += valuemessage
                if value:
                    self._options[str(index)] = value
                    index += 1
            _LOGGER.debug(
                "OTP method requested: %s%s", authselect_message, authoptions_message
            )
            status["authselect_required"] = True
            status["authselect_message"] = authoptions_message
            self._data = self.get_inputs(soup, {"id": "auth-select-device-form"})
        elif verification_captcha_tag is not None:
            _LOGGER.debug("Verification captcha code requested:")
            status["captcha_required"] = True
            status["captcha_image_url"] = verification_captcha_tag.get("src")
            status["verification_captcha_required"] = True
            self._data = self.get_inputs(soup, {"action": "verify"})
        elif verificationcode_tag is not None:
            _LOGGER.debug("Verification code requested:")
            status["verificationcode_required"] = True
            self._data = self.get_inputs(soup, {"action": "verify"})
        elif missingcookies_tag is not None and site_url.path != "/ap/maplanding":
            _LOGGER.debug("Error page detected:")
            href = ""
            links = missingcookies_tag.findAll("a", href=True)
            for link in links:
                href = link["href"]
            status["ap_error"] = True
            status["force_get"] = True
            status["ap_error_href"] = href
        elif javascript_authentication_tag:
            message: Text = ""

            message = soup.find("span").getText()
            for div in soup.findAll("div", {"id": "channelDetails"}):
                message += div.getText()
            status["force_get"] = True
            status["message"] = re.sub("(\\s)+", "\\1", message)
            status["action_required"] = True
            _LOGGER.debug("Javascript Authentication page detected: %s", message)
        elif forgotpassword_tag or soup.find("input", {"name": "OTPChallengeOptions"}):
            status["message"] = (
                "Forgot password page detected; "
                "Amazon has detected too many failed logins. "
                "Please check to see if Amazon requires any further action. "
                "You may have to wait before retrying."
            )
            status["ap_error"] = True
            _LOGGER.warning(status["message"])
            status["login_failed"] = "forgot_password"
        elif polling_tag:
            status["force_get"] = True
            status["message"] = self.status["message"]
            approval_status = soup.find("input", {"id": "transactionApprovalStatus"})
            _LOGGER.debug(
                "Polling page detected: %s with %s", polling_tag, approval_status
            )
            status["approval_status"] = approval_status.get("value")
        else:
            _LOGGER.debug("Captcha/2FA not requested; confirming login.")
            query = site_url.query
            self.access_token = query.get("openid.oa2.access_token")
            if await self.test_loggedin():
                await self.finalize_login()
                return
            _LOGGER.debug("Login failed; check credentials")
            status["login_failed"] = "login_failed"
            if self._data and "" in self._data.values():
                missing = [k for (k, v) in self._data.items() if v == ""]
                _LOGGER.debug(
                    "If credentials correct, please report" " these missing values: %s",
                    missing,
                )
        self.status = status
        # determine post url if not logged in
        if status.get("approval_status") == "TransactionCompleted":
            site = self._data.get("openid.return_to")
        elif form_tag and "login_successful" not in status:
            formsite: Text = form_tag.get("action")
            if self._debug:
                _LOGGER.debug("Found form to process: %s", form_tag)
            if formsite and formsite == "verify":
                search_results = re.search(r"(.+)/(.*)", str(site))
                assert search_results is not None
                site = search_results.groups()[0] + "/verify"
                _LOGGER.debug("Found post url to verify; converting to %s", site)
            elif formsite and formsite == "get":
                if "ap_error" in status and status.get("ap_error_href"):
                    assert isinstance(status["ap_error_href"], str)
                    site = status["ap_error_href"]
                elif self._headers.get("Referer"):
                    site = self._headers["Referer"]
                else:
                    site = self.start_url
                _LOGGER.debug("Found post url to get; forcing get to %s", site)
                self._lastreq = None
            elif formsite and formsite == "/ap/cvf/approval/poll":
                self._data = self.get_inputs(soup, {"id": "pollingForm"})
                url = urlparse(site)
                site = f"{url.scheme}://{url.netloc}{formsite}"
                # site = form_tag.find("input", {"name": "openid.return_to"}).get("value")
                _LOGGER.debug("Found url for polling page %s", site)
            elif formsite and forgotpassword_tag:
                site = self.start_url
                _LOGGER.debug("Restarting login process %s", site)
            elif formsite:
                site = formsite
                _LOGGER.debug("Found post url to %s", site)
        return str(site)

    def _populate_data(self, site: Text, data: Dict[str, Optional[str]]) -> bool:
        """Populate self._data with info from data."""
        _LOGGER.debug(
            "Preparing form submission to %s with input data: %s", site, obfuscate(data)
        )
        # pull data from configurator
        password: Optional[Text] = data.get("password", "")
        captcha: Optional[Text] = data.get("captcha", "")
        if data.get("otp_secret"):
            self.set_totp(data.get("otp_secret", ""))
        securitycode: Optional[Text] = data.get("securitycode", "")
        if not securitycode and self._totp:
            _LOGGER.debug("No 2FA code supplied but will generate.")
            securitycode = self.get_totp_token()
        claimsoption: Optional[Text] = data.get("claimsoption", "")
        authopt: Optional[Text] = data.get("authselectoption", "")
        verificationcode: Optional[Text] = data.get("verificationcode", "")

        #  add username and password to self._data for post request
        #  self._data is scraped from the form page in _process_page
        #  check if there is an input field
        if self._data:
            if "email" in self._data and self._data["email"] == "":
                self._data["email"] = self._email
                # add the otp to the password if available
            self._data["password"] = (
                self._password + securitycode
                if not password
                else password + securitycode
                if securitycode
                else password
            )
            if "rememberMe" in self._data:
                self._data["rememberMe"] = "true"
            if captcha is not None and "guess" in self._data:
                self._data["guess"] = captcha
            if captcha is not None and "cvf_captcha_input" in self._data:
                self._data["cvf_captcha_input"] = captcha
                self._data["cvf_captcha_captcha_action"] = "verifyCaptcha"
            if securitycode is not None and "otpCode" in self._data:
                self._data["otpCode"] = securitycode
                self._data["rememberDevice"] = "true"
            if claimsoption is not None and "option" in self._data:
                try:
                    self._data["option"] = self._options[str(claimsoption)]
                except KeyError:
                    _LOGGER.debug(
                        "Selected claimspicker option %s not in %s",
                        str(claimsoption),
                        self._options,
                    )
            if authopt is not None and "otpDeviceContext" in self._data:
                try:
                    self._data["otpDeviceContext"] = self._options[str(authopt)]
                except KeyError:
                    _LOGGER.debug(
                        "Selected OTP option %s not in %s", str(authopt), self._options,
                    )
            if verificationcode is not None and "code" in self._data:
                self._data["code"] = verificationcode
            self._data.pop("", None)  # remove '' key
            return "" in self._data.values()  # test if unfilled values
        return False

    async def finalize_login(self) -> None:
        """Perform final steps after successful login."""
        _LOGGER.debug(
            "Login confirmed for %s - %s; saving cookie to %s",
            self.email,
            self.url,
            self._cookiefile[0],
        )
        self.status = {}
        self.status["login_successful"] = True
        await self.save_cookiefile()
        #  remove extraneous Content-Type to avoid 500 errors
        self._headers.pop("Content-Type", None)
