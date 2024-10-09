from typing import Sequence

from solders.pubkey import Pubkey

from construct.lib.containers import Container


class RouteInfo:
    index: int
    stack_height: int
    name: str
    accounts: Sequence[Pubkey]
    data: Container

    def __init__(self,
                 index: int,
                 stack_height: int,
                 name: str,
                 accounts: Sequence[Pubkey],
                 data: Container):
        self.index = index
        self.stack_height = stack_height
        self.name = name
        self.accounts = accounts
        self.data = data
