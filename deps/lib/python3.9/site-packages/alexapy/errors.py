"""Python Package for controlling Alexa devices (echo dot, etc) programmatically.

SPDX-License-Identifier: Apache-2.0

Package errors.

For more details about this api, please refer to the documentation at
https://gitlab.com/keatontaylor/alexapy
"""


class AlexapyError(Exception):
    """Define a base error."""


class AlexapyConnectionError(AlexapyError):
    """Define an error related to invalid requests."""


class AlexapyLoginError(AlexapyError):
    """Define an error related to no longer being logged in."""


class AlexapyTooManyRequestsError(AlexapyError):
    """Define an error related to too many requests."""


class AlexapyLoginCloseRequested(AlexapyError):
    """Define an error related to requesting access to API after requested close."""


class AlexapyPyotpInvalidKey(AlexapyError):
    """Define an error related to invalid 2FA key."""
