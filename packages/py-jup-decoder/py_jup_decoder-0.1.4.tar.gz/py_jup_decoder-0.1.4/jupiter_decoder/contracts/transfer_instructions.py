from typing import Union

from solders.transaction_status import ParsedInstruction, UiPartiallyDecodedInstruction, UiCompiledInstruction


class TransferInstructions:
    in_transfers: list[Union[ParsedInstruction, UiPartiallyDecodedInstruction, UiCompiledInstruction]] = []
    out_transfers: list[Union[ParsedInstruction, UiPartiallyDecodedInstruction, UiCompiledInstruction]] = []
