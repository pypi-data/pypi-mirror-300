import json
from typing import Union

from anchorpy_core.idl import Idl
from solana.rpc.async_api import AsyncClient
from solders.signature import Signature

from jupiter_decoder.contracts.consts import JUPITER_V6_PROGRAM_ID
from jupiter_decoder.contracts.idl_json import IDL_JSON
from jupiter_decoder.jup_event_parser import JupEventParser

StrOrSignature = Union[str, Signature]
IDL = Idl.from_json(json.dumps(IDL_JSON))


class JupRpcClient:
    def __init__(self, endpoint: str = 'https://api.mainnet-beta.solana.com'):
        self.client = AsyncClient(endpoint)
        self._jup_event_parser = JupEventParser(IDL, endpoint)

    async def decode_transaction(self, signature: StrOrSignature):
        if isinstance(signature, str):
            signature = Signature.from_string(signature)

        tx_resp = await self.client.get_transaction(
                        signature,
                        "jsonParsed",
                        max_supported_transaction_version=0,
                    )

        tx = tx_resp.value.transaction
        if tx.meta.err:
            print('Failed transaction {0}'.format(tx.meta.err))

        route_info_list = self._jup_event_parser.get_route_info_list(tx)
        swaps = []
        for route_info in route_info_list:
            swap = await self._jup_event_parser.extract_single_route(
                signature,
                tx,
                tx_resp.value.block_time,
                route_info,
                JUPITER_V6_PROGRAM_ID)
            if swap:
                swaps.append(swap)

        return swaps





