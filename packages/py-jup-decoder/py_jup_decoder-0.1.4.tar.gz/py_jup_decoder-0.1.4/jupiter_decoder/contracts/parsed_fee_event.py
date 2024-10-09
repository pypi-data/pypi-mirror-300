from solders.pubkey import Pubkey


class ParsedFeeEvent:
    account: Pubkey
    mint: Pubkey
    amount: int

    def __init__(self,
                 *,
                 account: Pubkey,
                 mint: Pubkey,
                 amount: int):
        self.account = account
        self.mint = mint
        self.amount = amount
