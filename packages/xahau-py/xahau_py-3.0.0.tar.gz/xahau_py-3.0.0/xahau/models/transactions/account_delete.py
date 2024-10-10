"""Model for AccountDelete transaction type."""

from dataclasses import dataclass, field
from typing import Optional

from xahau.models.required import REQUIRED
from xahau.models.transactions.transaction import Transaction
from xahau.models.transactions.types import TransactionType
from xahau.models.utils import KW_ONLY_DATACLASS, require_kwargs_on_init


@require_kwargs_on_init
@dataclass(frozen=True, **KW_ONLY_DATACLASS)
class AccountDelete(Transaction):
    """
    Represents an `AccountDelete transaction
    <https://xrpl.org/accountdelete.html>`_, which deletes an account and any
    objects it owns in the XAH Ledger, if possible, sending the account's remaining
    XAH to a specified destination account.

    See `Deletion of Accounts
    <https://xrpl.org/accounts.html#deletion-of-accounts>`_ for the requirements to
    delete an account.
    """

    destination: str = REQUIRED  # type: ignore
    """
    The address of the account to which to send any remaining XAH.
    This field is required.

    :meta hide-value:
    """

    destination_tag: Optional[int] = None
    """
    The `destination tag
    <https://xrpl.org/source-and-destination-tags.html>`_ at the
    ``destination`` account where funds should be sent.
    """

    transaction_type: TransactionType = field(
        default=TransactionType.ACCOUNT_DELETE,
        init=False,
    )
