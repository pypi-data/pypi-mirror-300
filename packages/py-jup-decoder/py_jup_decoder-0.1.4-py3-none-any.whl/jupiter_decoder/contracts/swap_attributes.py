import json
from datetime import datetime
from decimal import Decimal
from typing import Optional, Any


class SwapAttributes:
    owner: str
    transfer_authority: str
    program_id: str
    signature: str
    timestamp: datetime
    leg_count: int
    volume_in_usd: Decimal
    in_symbol: str
    in_amount: Decimal
    in_amount_in_decimal: Optional[Decimal] = None
    in_amount_in_usd: Decimal
    in_mint: str
    out_symbol: str
    out_amount: Decimal
    out_amount_in_decimal: Optional[Decimal] = None
    out_amount_in_usd: Decimal
    out_mint: str
    instruction: str
    exact_in_amount: Decimal
    exact_in_amount_in_usd: Decimal
    exact_out_amount: Decimal
    exact_out_amount_in_usd: Decimal
    swap_data: dict[str, Any]
    fee_token_pubkey: Optional[str] = None
    fee_owner: Optional[str] = None
    fee_symbol: Optional[str] = None
    fee_amount: Optional[Decimal] = None
    fee_amount_in_decimal: Optional[Decimal] = None
    fee_amount_in_usd: Optional[Decimal] = None
    fee_mint: Optional[str] = None
    token_ledger: Optional[str] = None
    last_account: str

    def __repr__(self):
        def default_converter(o):
            if isinstance(o, Decimal):
                return str(o)
            if isinstance(o, datetime):
                return o.isoformat()
            return o.__dict__

        return json.dumps(self, default=default_converter, indent=2)


