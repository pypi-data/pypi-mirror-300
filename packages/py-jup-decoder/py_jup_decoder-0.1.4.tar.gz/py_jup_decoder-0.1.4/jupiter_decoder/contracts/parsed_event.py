from typing import Union

from jupiter_decoder.contracts.parsed_fee_event import ParsedFeeEvent
from jupiter_decoder.contracts.parsed_swap_event import ParsedSwapEvent


class ParsedEvent:
    data: Union[ParsedSwapEvent, ParsedFeeEvent]
    name: str

    def __init__(self, name: str, data: Union[ParsedSwapEvent, ParsedFeeEvent]):
        self.name = name
        self.data = data