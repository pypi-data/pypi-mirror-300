from solders.pubkey import Pubkey


class ParsedSwapEvent:
    amm: Pubkey
    input_mint: Pubkey
    input_amount: int
    output_mint: Pubkey
    output_amount: int

    def __init__(self,
                 *,
                 amm: Pubkey,
                 input_mint: Pubkey,
                 input_amount: int,
                 output_mint: Pubkey,
                 output_amount: int):
        self.amm = amm
        self.input_mint = input_mint
        self.input_amount = input_amount
        self.output_mint = output_mint
        self.output_amount = output_amount
