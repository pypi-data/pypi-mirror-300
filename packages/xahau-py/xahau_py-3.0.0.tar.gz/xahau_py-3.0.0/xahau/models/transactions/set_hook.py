"""Model for SetHook transaction type."""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from enum import Enum
from typing import Dict, List, Optional, Pattern, Union

from typing_extensions import Final

from xahau.models.flags import FlagInterface
from xahau.models.nested_model import NestedModel
from xahau.models.required import REQUIRED
from xahau.models.transactions.transaction import Transaction
from xahau.models.transactions.types import TransactionType
from xahau.models.utils import require_kwargs_on_init

MAX_HOOKS: Final[int] = 10
"""
Maximum number of hooks allowed.

:meta private:
"""
HEX_REGEX: Final[Pattern[str]] = re.compile("[A-Fa-f0-9]{64}")
"""
Matches hex-encoded WalletLocator in the format allowed by XAHL.

:meta private:
"""


class SetHookFlag(int, Enum):
    """SetHookFlag"""

    HSF_OVERRIDE = 0x00000001
    """"""

    HSF_NS_DELETE = 0x00000002
    """"""

    HSF_COLLECT = 0x00000004
    """"""


class SetHookFlagInterface(FlagInterface):
    """SetHookFlagInterface"""

    HSF_OVERRIDE: bool
    HSF_NS_DELETE: bool
    HSF_COLLECT: bool


@require_kwargs_on_init
@dataclass(frozen=True)
class HookGrant(NestedModel):
    """Represents one grant in a list of grants on the transaction."""

    hook_hash: str = REQUIRED  # type: ignore
    """
    The hook hash of the grant.
    This field is required.

    :meta hide-value:
    """

    authorize: Optional[str] = None
    """The account authorized on the grant."""


@require_kwargs_on_init
@dataclass(frozen=True)
class HookParameter(NestedModel):
    """Represents one parameter in a list of parameters on the transaction."""

    hook_parameter_name: str = REQUIRED  # type: ignore
    """
    The name of the parameter.
    This field is required.

    :meta hide-value:
    """

    hook_parameter_value: str = REQUIRED  # type: ignore
    """
    The value of the parameter.
    This field is required.

    :meta hide-value:
    """


@require_kwargs_on_init
@dataclass(frozen=True)
class Hook(NestedModel):
    """Represents one hook in a list of hooks deployed to an account."""

    create_code: Optional[str] = None
    """
    The code that is executed when the hook is triggered.
    This field is required.

    :meta hide-value:
    """

    flags: Union[Dict[str, bool], int, List[int]] = 0
    """
    The flags that are set on the hook.
    This field is required.

    :meta hide-value:
    """

    hook_hash: Optional[str] = None
    """"""

    hook_on: Optional[str] = None
    """The transactions that triggers the hook. Represented as a 256Hash"""

    hook_namespace: Optional[str] = None
    """The namespace of the hook."""

    hook_api_version: Optional[int] = None
    """The API version of the hook."""

    hook_parameters: Optional[List[HookParameter]] = None
    """The parameters of the hook."""

    hook_grants: Optional[List[HookGrant]] = None
    """The grants of the hook."""


@require_kwargs_on_init
@dataclass(frozen=True)
class SetHook(Transaction):
    """Sets the an array of hooks on an account."""

    hooks: Optional[List[Hook]] = None
    transaction_type: TransactionType = field(
        default=TransactionType.SET_HOOK,
        init=False,
    )

    def _get_errors(self: SetHook) -> Dict[str, str]:
        errors = super()._get_errors()

        if self.hooks is None:  # deletion of the Hooks object
            return errors

        if len(self.hooks) > MAX_HOOKS:
            errors["hooks"] = "`hooks` must have no more than {} members.".format(
                MAX_HOOKS
            )
            return errors

        for hook in self.hooks:
            if hook.hook_on is not None and not bool(HEX_REGEX.fullmatch(hook.hook_on)):
                errors["hooks"] = "A Hook's hook_on must be a 256-bit (32-byte) "
                "hexadecimal value."

            if hook.hook_namespace is not None and not bool(
                HEX_REGEX.fullmatch(hook.hook_namespace)
            ):
                errors["hooks"] = "A Hook's hook_namespace must be a 256-bit (32-byte) "
                "hexadecimal value."

        return errors
