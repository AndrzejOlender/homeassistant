"""Python Package for controlling Alexa devices (echo dot, etc) programmatically.

SPDX-License-Identifier: Apache-2.0

Constants.

For more details about this api, please refer to the documentation at
https://gitlab.com/keatontaylor/alexapy
"""

EXCEPTION_TEMPLATE = "An exception of type {0} occurred. Arguments:\n{1!r}"

APP_NAME = "Alexa Media Player"
USER_AGENT = f"AmazonWebView/{APP_NAME}/2.2.223830.0/iOS/11.4.1/iPhone"
LOCALE_KEY = {
    ".de": "de_DE",
    ".com.au": "en_AU",
    ".ca": "en_CA",
    ".co.uk": "en_GB",
    ".in": "en_IN",
    ".com": "en_US",
    ".es": "es_ES",
    ".mx": "es_MX",
    ".fr": "fr_FR",
    ".it": "it_IT",
    ".co.jp": "ja_JP",
    ".com.br": "pt_BR",
}
