"""High-level ledger methods with the XAHL ledger."""

import asyncio
from typing import Optional

from xahau.asyncio.ledger import main
from xahau.clients.sync_client import SyncClient


def get_latest_validated_ledger_sequence(client: SyncClient) -> int:
    """
    Returns the sequence number of the latest validated ledger.

    Args:
        client: The network client to use to send the request.

    Returns:
        The sequence number of the latest validated ledger.

    Raises:
        XAHLRequestFailureException: if the rippled API call fails.
    """
    return asyncio.run(main.get_latest_validated_ledger_sequence(client))


def get_latest_open_ledger_sequence(client: SyncClient) -> int:
    """
    Returns the sequence number of the latest open ledger.

    Args:
        client: The network client to use to send the request.

    Returns:
        The sequence number of the latest open ledger.

    Raises:
        XAHLRequestFailureException: if the rippled API call fails.
    """
    return asyncio.run(main.get_latest_open_ledger_sequence(client))


def get_fee(
    client: SyncClient,
    *,
    max_fee: Optional[float] = 2,
    fee_type: str = "open",
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
    return asyncio.run(main.get_fee(client, max_fee=max_fee, fee_type=fee_type))


def get_fee_estimate(
    client: SyncClient,
    tx_blob: str,
) -> str:
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
    return asyncio.run(main.get_fee_estimate(client, tx_blob=tx_blob))
