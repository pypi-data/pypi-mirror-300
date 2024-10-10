"""
The channel_verify method checks the validity of a
signature that can be used to redeem a specific amount of
XAH from a payment channel.
"""

from dataclasses import dataclass, field

from xahau.models.amounts import Amount
from xahau.models.requests.request import Request, RequestMethod
from xahau.models.required import REQUIRED
from xahau.models.utils import KW_ONLY_DATACLASS, require_kwargs_on_init


@require_kwargs_on_init
@dataclass(frozen=True, **KW_ONLY_DATACLASS)
class ChannelVerify(Request):
    """
    The channel_verify method checks the validity of a
    signature that can be used to redeem a specific amount of
    XAH from a payment channel.
    """

    method: RequestMethod = field(default=RequestMethod.CHANNEL_VERIFY, init=False)
    channel_id: str = REQUIRED  # type: ignore
    """
    This field is required.

    :meta hide-value:
    """

    amount: Amount = REQUIRED  # type: ignore
    """
    This field is required.

    :meta hide-value:
    """

    public_key: str = REQUIRED  # type: ignore
    """
    This field is required.

    :meta hide-value:
    """

    signature: str = REQUIRED  # type: ignore
    """
    This field is required.

    :meta hide-value:
    """
