from solders.pubkey import Pubkey


class Swap:
    instruction_index: int
    stack_height: int
    next_swap_index: int
    in_account: Pubkey
    out_account: Pubkey
