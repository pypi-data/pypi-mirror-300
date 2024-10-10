"""
Specifies an amount in an issued currency.

See https://xrpl.org/currency-formats.html#issued-currency-amounts.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import List, Union

from xahau.models.amounts.issued_currency_amount import IssuedCurrencyAmount
from xahau.models.base_model import BaseModel
from xahau.models.required import REQUIRED
from xahau.models.utils import require_kwargs_on_init


@require_kwargs_on_init
@dataclass(frozen=True)
class InnerAmount(BaseModel):
    """Represents an amount entry object."""

    amount: Union[IssuedCurrencyAmount, str] = REQUIRED  # type: ignore
    """
    This field is required.

    :meta hide-value:
    """


@require_kwargs_on_init
@dataclass(frozen=True)
class AmountEntry(BaseModel):
    """Represents an amount entry object."""

    amount_entry: InnerAmount = REQUIRED  # type: ignore
    """
    This field is required.

    :meta hide-value:
    """


Amounts = List[AmountEntry]
