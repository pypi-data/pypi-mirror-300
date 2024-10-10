"""High-level ledger methods with the XAHL ledger."""

from typing import Optional, cast

from xahau.asyncio.clients import Client, XAHLRequestFailureException
from xahau.asyncio.ledger.utils import calculate_fee_dynamically
from xahau.constants import XAHLException
from xahau.models.requests import Fee, GenericRequest, Ledger
from xahau.utils import xah_to_drops


async def get_latest_validated_ledger_sequence(client: Client) -> int:
    """
    Returns the sequence number of the latest validated ledger.

    Args:
        client: The network client to use to send the request.

    Returns:
        The sequence number of the latest validated ledger.

    Raises:
        XAHLRequestFailureException: if the rippled API call fails.
    """
    response = await client._request_impl(Ledger(ledger_index="validated"))
    if response.is_successful():
        return cast(int, response.result["ledger_index"])

    raise XAHLRequestFailureException(response.result)


async def get_latest_open_ledger_sequence(client: Client) -> int:
    """
    Returns the sequence number of the latest open ledger.

    Args:
        client: The network client to use to send the request.

    Returns:
        The sequence number of the latest open ledger.

    Raises:
        XAHLRequestFailureException: if the rippled API call fails.
    """
    response = await client._request_impl(Ledger(ledger_index="open"))
    if response.is_successful():
        return cast(int, response.result["ledger_index"])

    raise XAHLRequestFailureException(response.result)


async def get_fee(
    client: Client, *, max_fee: Optional[float] = 2, fee_type: str = "open"
) -> str:
    """
    Query the ledger for the current transaction fee.

    Args:
        client: the network client used to make network calls.
        max_fee: The maximum fee in XAH that the user wants to pay. If load gets too
            high, then the fees will not scale past the maximum fee. If None, there is
            no ceiling for the fee. The default is 2 XAH.
        fee_type: The type of fee to return. The options are "open" (the load-scaled
            fee to get into the open ledger), "minimum" (the minimum transaction
            fee) or "dynamic" (dynamic fee-calculation based on the queue size
            of the node). The default is "open". The recommended option is
            "dynamic".

    Returns:
        The transaction fee, in drops.
        `Read more about drops <https://xrpl.org/currency-formats.html#xrp-amounts>`_

    Raises:
        XAHLException: if an incorrect option for `fee_type` is passed in.
        XAHLRequestFailureException: if the rippled API call fails.
    """
    response = await client._request_impl(Fee())
    if not response.is_successful():
        raise XAHLRequestFailureException(response.result)

    result = response.result
    drops = result["drops"]
    if fee_type == "open":
        fee = cast(str, drops["open_ledger_fee"])
    elif fee_type == "minimum":
        fee = cast(str, drops["minimum_fee"])
    elif fee_type == "dynamic":
        fee = calculate_fee_dynamically(fee_data_set=result)
    else:
        raise XAHLException(
            '`fee_type` param must be "open", "minimum" or "dynamic".'
            f" {fee_type} is not a valid option."
        )
    if max_fee is not None:
        max_fee_drops = int(xah_to_drops(max_fee))
        if max_fee_drops < int(fee):
            fee = str(max_fee_drops)
    return fee


async def get_fee_estimate(client: Client, tx_blob: str) -> str:
    """
    Query the ledger for the estimated transaction fee.

    Args:
        client: the network client used to make network calls.
        tx_blob: the encoded transaction that you want the fee estimate for.

    Returns:
        The transaction fee, in drops.
        `Read more about drops <https://xrpl.org/currency-formats.html#xrp-amounts>`_

    Raises:
        XAHLException: if an incorrect option for `fee_type` is passed in.
        XAHLRequestFailureException: if the rippled API call fails.
    """
    fee_request = GenericRequest(command="fee", tx_blob=tx_blob)
    response = await client._request_impl(fee_request)
    if not response.is_successful():
        raise XAHLRequestFailureException(response.result)

    result = response.result
    if "drops" not in result or "base_fee" not in result["drops"]:
        raise XAHLException("could not estimate transaction fee")

    return str(result["drops"]["base_fee"])
