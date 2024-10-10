"""High-level reliable submission methods with XAHL transactions."""

import asyncio
from typing import Optional

from xahau.asyncio.transaction import submit_and_wait as async_submit_and_wait
from xahau.clients.sync_client import SyncClient
from xahau.models.response import Response
from xahau.models.transactions.transaction import Transaction
from xahau.wallet.main import Wallet


def submit_and_wait(
    transaction: Transaction,
    client: SyncClient,
    wallet: Optional[Wallet] = None,
    *,
    check_fee: bool = True,
    autofill: bool = True,
    fail_hard: bool = False,
) -> Response:
    """
    Signs a transaction locally, without trusting external rippled nodes (only if
    the input transaction is unsigned; otherwise, proceeds to the next steps), submits,
    and verifies that it has been included in a validated ledger (or has errored
    /will not be included for some reason).
    `See Reliable Transaction Submission
    <https://xrpl.org/reliable-transaction-submission.html>`_

    Args:
        transaction: the signed/unsigned transaction (or transaction blob) to
            be submitted.
        client: the network client with which to submit the transaction.
        wallet: an optional wallet with which to sign the transaction. This is
            only needed if the transaction is unsigned.
        check_fee: an optional bolean indicating whether to check if the fee is
            higher than the expected transaction type fee. Defaults to True.
        autofill: an optional boolean indicating whether to autofill the
            transaction. Defaults to True.
        fail_hard: an optional boolean. If True, and the transaction fails for
            the initial server, do not retry or relay the transaction to other
            servers. Defaults to False.

    Returns:
        The response from the ledger.
    """
    return asyncio.run(
        async_submit_and_wait(
            transaction,
            client,
            wallet,
            check_fee=check_fee,
            autofill=autofill,
            fail_hard=fail_hard,
        )
    )
