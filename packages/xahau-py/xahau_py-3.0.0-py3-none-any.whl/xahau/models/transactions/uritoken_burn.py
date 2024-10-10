"""Model for URITokenBurn transaction type."""
from dataclasses import dataclass, field

from xahau.models.required import REQUIRED
from xahau.models.transactions.transaction import Transaction
from xahau.models.transactions.types import TransactionType
from xahau.models.utils import require_kwargs_on_init


@require_kwargs_on_init
@dataclass(frozen=True)
class URITokenBurn(Transaction):
    """
    The URITokenBurn transaction is used to remove an URIToken object from the
    Account Objects in which it is being held, effectively removing the token from
    the ledger ("burning" it).
    """

    account: str = REQUIRED  # type: ignore
    """
    Identifies the AccountID that submitted this transaction. The account must
    be the present owner of the token or, if the lsfBurnable flag is set
    on the URIToken, either the issuer account or an account authorized by the
    issuer (i.e. MintAccount). This field is required.

    :meta hide-value:
    """

    uritoken_id: str = REQUIRED  # type: ignore
    """
    Identifies the URIToken to be burned. This field is required.

    :meta hide-value:
    """

    transaction_type: TransactionType = field(
        default=TransactionType.URITOKEN_BURN,
        init=False,
    )
