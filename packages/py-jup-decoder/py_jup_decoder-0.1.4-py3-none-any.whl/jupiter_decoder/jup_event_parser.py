import asyncio
import datetime
from decimal import Decimal
from typing import Dict
from typing import Union, Sequence

import base58
from anchorpy import Coder, NamedInstruction
from anchorpy_core.idl import Idl
from solders.pubkey import Pubkey
from solders.rpc.responses import GetAccountInfoMaybeJsonParsedResp as AccountInfo
from solders.signature import Signature
from solders.transaction_status import EncodedTransactionWithStatusMeta
from solders.transaction_status import ParsedInstruction, UiPartiallyDecodedInstruction, UiCompiledInstruction

from jupiter_decoder.contracts.consts import JUPITER_V6_PROGRAM_ID, ROUTE_NAMES, AMM_TYPES, PLATFORM_FEE_ACCOUNTS_POSITION
from jupiter_decoder.contracts.parsed_event import ParsedEvent
from jupiter_decoder.contracts.parsed_fee_event import ParsedFeeEvent
from jupiter_decoder.contracts.parsed_swap_event import ParsedSwapEvent
from jupiter_decoder.contracts.route_info import RouteInfo
from jupiter_decoder.contracts.swap_attributes import SwapAttributes
from jupiter_decoder.account_info_manager import AccountInfoManager
from jupiter_decoder.sessions import TokensJupSession, PriceJupSession
from jupiter_decoder.event_static_methods import _get_inner_instructions, _get_swaps, \
    _get_in_and_out_transfer_instructions, _is_fee_instruction, InnerInstruction
from jupiter_decoder.instruction_static_methods import get_initial_and_final_swap_positions, \
    get_instruction_name_and_transfer_authority_and_last_account, get_exact_out_amount, get_exact_in_amount


class JupEventParser(Coder):
    def __init__(self, idl: Idl, endpoint: str = 'https://api.mainnet-beta.solana.com'):
        self._account_info_manager = AccountInfoManager(endpoint)
        self._tokens_jup_session = TokensJupSession()
        self._price_jup_session = PriceJupSession()
        super().__init__(idl)

    def get_route_info_list(self, transaction_with_meta: EncodedTransactionWithStatusMeta):
        route_info_list = []
        for index, instruction in enumerate(transaction_with_meta.transaction.message.instructions):
            if instruction.program_id == JUPITER_V6_PROGRAM_ID:
                ix: NamedInstruction = self.instruction.parse(base58.b58decode(instruction.data))
                if ix.name in ROUTE_NAMES:
                    route_info_list.append(RouteInfo(
                        index,
                        1,
                        ix.name,
                        instruction.accounts,
                        ix.data
                    ))

        return route_info_list

    async def extract_single_route(self,
                                   signature: Signature,
                                   transaction_with_meta: EncodedTransactionWithStatusMeta,
                                   block_time: int,
                                   route_info: RouteInfo,
                                   program_id: Pubkey):
        account_infos_dict = {}
        parsed_events = await self.get_parsed_events(transaction_with_meta, route_info)
        if len(parsed_events) == 0:
            return

        swap_events = [event.data for event in parsed_events if event.name == 'ParsedSwapEvent']
        fee_events = [event.data for event in parsed_events if event.name == 'ParsedFeeEvent']
        if len(swap_events) == 0:
            # Not a swap event, for example:
            # https://solscan.io/tx/5ZSozCHmAFmANaqyjRj614zxQY8HDXKyfAs2aAVjZaadS4DbDwVq8cTbxmM5m5VzDcfhysTSqZgKGV1j2A2Hqz1V
            return

        accounts_to_be_fetched = []
        [accounts_to_be_fetched.append(event.input_mint) for event in swap_events]
        [accounts_to_be_fetched.append(event.output_mint) for event in swap_events]

        if len(fee_events) > 0:
            accounts_to_be_fetched.append(fee_events[0].account)

        for account_id in accounts_to_be_fetched:
            account_infos_dict[str(account_id)] = await self._account_info_manager.get_account_info(account_id)

        swap_data = await self.parse_swap_events(account_infos_dict, swap_events)
        initial_positions, final_positions = get_initial_and_final_swap_positions(route_info)
        if len(swap_events) == 1:
            final_positions = initial_positions

        in_symbol = swap_data[initial_positions[0]]['inSymbol']
        in_mint = swap_data[initial_positions[0]]['inMint']

        in_swap_data = [data for index, data in enumerate(swap_data)
                        if index in initial_positions and data['inMint'] == in_mint]
        in_amount = 0
        in_amount_in_decimal = Decimal(0)
        in_amount_in_usd = Decimal(0)

        for data in in_swap_data:
            in_amount += data['inAmount']
            in_amount_in_decimal += Decimal(data['inAmountInDecimal']) if 'inAmountInDecimal' in data else Decimal(0)
            in_amount_in_usd += Decimal(data['inAmountInUSD']) if ('inAmountInUSD' in data and
                                                                   data['inAmountInUSD'] is not None) else Decimal(0)

        out_symbol = swap_data[final_positions[0]]['outSymbol']
        out_mint = swap_data[final_positions[0]]['outMint']

        out_swap_data = [data for index, data in enumerate(swap_data)
                         if index in final_positions and data['outMint'] == out_mint]
        out_amount = 0
        out_amount_in_decimal = Decimal(0)
        out_amount_in_usd = Decimal(0)

        for data in out_swap_data:
            out_amount += data['outAmount']
            out_amount_in_decimal += Decimal(data['outAmountInDecimal']) if 'outAmountInDecimal' in data else Decimal(0)
            out_amount_in_usd += Decimal(data['outAmountInUSD']) if ('outAmountInUSD' in data and
                                                                     data['outAmountInUSD'] is not None) else Decimal(0)

        volume_in_usd = min(out_amount_in_usd, out_amount_in_usd) \
            if out_amount_in_usd and out_amount_in_usd else out_amount_in_usd or out_amount_in_usd

        swap = SwapAttributes()
        instruction_name, transfer_authority, last_account = (
            get_instruction_name_and_transfer_authority_and_last_account(route_info))
        swap.transfer_authority = transfer_authority
        swap.last_account = last_account
        swap.instruction = instruction_name
        swap.owner = str(transaction_with_meta.transaction.message.account_keys[0].pubkey)
        swap.program_id = str(program_id)
        swap.signature = str(signature)
        swap.timestamp = datetime.datetime.fromtimestamp(block_time)
        swap.leg_count = len(swap_events)
        swap.volume_in_usd = volume_in_usd

        swap.in_symbol = in_symbol
        swap.in_amount = in_amount
        swap.in_amount_in_decimal = in_amount_in_decimal
        swap.in_amount_in_usd = in_amount_in_usd
        swap.in_mint = in_mint

        swap.out_symbol = out_symbol
        swap.out_amount = out_amount
        swap.out_amount_in_decimal = out_amount_in_decimal
        swap.out_amount_in_usd = out_amount_in_usd
        swap.out_mint = out_mint

        exact_out_amount = get_exact_out_amount(route_info)
        swap.exact_out_amount = Decimal(exact_out_amount) if exact_out_amount else Decimal(0)
        swap.exact_out_amount_in_usd = swap.exact_out_amount / out_amount * out_amount_in_usd

        exact_in_amount = get_exact_in_amount(route_info)
        swap.exact_in_amount = Decimal(exact_in_amount) if exact_in_amount else Decimal(0)
        swap.exact_in_amount_in_usd = swap.exact_in_amount / in_amount * in_amount_in_usd
        swap.swap_data = swap_data

        if len(fee_events) > 0:
            fee_event = fee_events[0]
            volume = await self.extract_volume(account_infos_dict, fee_event.mint, fee_event.amount)
            swap.fee_token_pubkey = str(fee_event.account)
            swap.fee_owner = str(account_infos_dict[swap.fee_token_pubkey].value.data.parsed['info']['owner'])
            swap.fee_symbol = volume['symbol']
            swap.fee_amount = Decimal(volume['amount'])
            swap.fee_amount_in_decimal = Decimal(volume['amountInDecimal'])
            swap.fee_amount_in_usd = Decimal(volume['amountInUSD']) if volume['amountInUSD'] is not None else Decimal(0)
            swap.fee_mint = str(volume['mint'])

        return swap

    async def parse_swap_events(self,
                                account_infos_dict: Dict[str, AccountInfo],
                                swap_events: Sequence[ParsedSwapEvent]):
        swap_data = await asyncio.gather(
            *(self.extract_swap_data(account_infos_dict, swap_event) for swap_event in swap_events))
        return swap_data

    async def extract_swap_data(self,
                                account_infos_dict: Dict[str, AccountInfo],
                                swap_event: ParsedSwapEvent):
        amm = AMM_TYPES[str(swap_event.amm)]

        in_volume = await self.extract_volume(account_infos_dict, swap_event.input_mint, swap_event.input_amount)
        out_volume = await self.extract_volume(account_infos_dict, swap_event.output_mint, swap_event.output_amount)

        return {
            'amm': amm,
            'inSymbol': in_volume['symbol'],
            'inMint': in_volume['mint'],
            'inAmount': in_volume['amount'],
            'inAmountInDecimal': in_volume['amountInDecimal'],
            'inAmountInUSD': in_volume['amountInUSD'],
            'outSymbol': out_volume['symbol'],
            'outMint': out_volume['mint'],
            'outAmount': out_volume['amount'],
            'outAmountInDecimal': out_volume['amountInDecimal'],
            'outAmountInUSD': out_volume['amountInUSD'],
        }

    async def extract_volume(self,
                             account_infos_dict: Dict[str, AccountInfo],
                             mint: Pubkey,
                             amount: int):
        token = await self._tokens_jup_session.get_token_info(mint)
        token_price_in_usd = await self._price_jup_session.get_price_in_usd_by_mint(mint)
        token_decimals = account_infos_dict[str(mint)].value.data.parsed['info']['decimals'] \
            if str(mint) in account_infos_dict else None

        symbol = token['symbol'] if token and 'error' not in token else None
        amount_in_decimal = Decimal(amount) / (10 ** token_decimals)
        amount_in_usd = amount_in_decimal * token_price_in_usd if token_price_in_usd else None

        return {
            'token': token,
            'symbol': symbol,
            'mint': mint,
            'amount': amount,
            'amountInDecimal': amount_in_decimal,
            'amountInUSD': amount_in_usd,
        }

    async def get_parsed_events(self,
                                transaction_with_meta: EncodedTransactionWithStatusMeta,
                                route_info: RouteInfo):
        events = []
        inner_instructions = _get_inner_instructions(transaction_with_meta, route_info)
        if len(inner_instructions) == 0:
            return events

        swaps = _get_swaps(inner_instructions, route_info)
        for swap in swaps:
            transfer_instructions = _get_in_and_out_transfer_instructions(inner_instructions, swap)
            if len(transfer_instructions.in_transfers) == 0 or len(transfer_instructions.out_transfers) == 0:
                continue

            in_transfer_data = await self.get_transfer_data(transfer_instructions.in_transfers, 'in')
            out_transfer_data = await self.get_transfer_data(transfer_instructions.out_transfers, 'out')
            events.append(ParsedEvent(
                'ParsedSwapEvent',
                ParsedSwapEvent(
                    amm=inner_instructions[swap.instruction_index].program_id,
                    input_mint=in_transfer_data['mint'],
                    input_amount=in_transfer_data['amount'],
                    output_mint=out_transfer_data['mint'],
                    output_amount=out_transfer_data['amount']
                )
            ))

        if route_info.data.platform_fee_bps > 0:
            swap_fee = await self.get_swap_fee(route_info, inner_instructions)
            if swap_fee is None:
                return events

            events.append(ParsedEvent(
                'ParsedFeeEvent',
                ParsedFeeEvent(
                    account=Pubkey.from_string(swap_fee['account']),
                    mint=Pubkey.from_string(swap_fee['mint']),
                    amount=swap_fee['amount']
                )
            ))

        return events

    async def get_transfer_data(self, transfer_instructions: Sequence[InnerInstruction], transfer_type: str):
        mint = ''
        amount = 0
        for instruction in transfer_instructions:
            if (instruction.parsed['type'] == 'transferChecked' or
                    instruction.parsed['type'] == 'transferCheckedWithFee'):
                if transfer_type == 'out':
                    amount = (amount + await self.get_exact_out_amount_after_fee(
                        instruction.parsed['info'],
                        instruction.parsed['type']))
                else:
                    amount = amount + int(instruction.parsed['info']['tokenAmount']['amount'])
            else:
                amount = amount + int(instruction.parsed['info']['amount'])

        transfer_instruction = transfer_instructions[0]
        if transfer_instruction.parsed['type'] == 'transfer':
            if transfer_type == 'in':
                account = transfer_instruction.parsed['info']['destination']
            else:
                account = transfer_instruction.parsed['info']['source']

            account_info = await self._account_info_manager.get_account_info(account)
            if account_info is None:
                mint = transfer_instruction.parsed['info']['mint']
            else:
                mint = account_info.value.data.parsed['info']['mint']
        else:
            mint = transfer_instruction.parsed['info']['mint']

        return {'mint': mint, 'amount': amount}

    async def get_exact_out_amount_after_fee(self, info: dict, _type: str):
        # testcase 7atgF8KQo4wJrD5ATGX7t1V2zVvykPJbFfNeVf1icFv1
        # tx_id 3b6xEqa7cZv8Gbo1VjaKKuLbbXDD4g9x1m5yzGgRfSb2ozktqCrY9BtoqkSiBgnu1uwMsjBWcqqHTE2eQDy9DtTR

        # testcase 2b1kV6DkPAnxd5ixfnxCpjxmKwqjjaYmCZfHsFu24GXo
        # tx_id 2nRKszNNFYHjKevkBs9zT7gctuCS7iFVQXPfuRKX5cfCeYAQwFsZP4N6GbkXvAJSnXjMk1aNhFyYtrtDimkhJBAD

        if _type == 'transferChecked':
            fee_config = await self._account_info_manager.get_fee_config(info['mint'])
            if fee_config is None:
                return int(info['tokenAmount']['amount'])

            fee_basis_points = fee_config.newer_transfer_fee.transfer_fee_basis_points
            amount = int(info['tokenAmount']['amount'])
            fee = amount * fee_basis_points / 10_000
            return amount - fee

        return int(info['tokenAmount']['amount']) - int(info['feeAmount']['amount'])

    async def get_swap_fee(self, route_info: RouteInfo, inner_instructions: Sequence[InnerInstruction]):
        position = PLATFORM_FEE_ACCOUNTS_POSITION[route_info.name]
        fee_account = route_info.accounts[position]

        for inner_instruction in inner_instructions:
            if not hasattr(inner_instruction, 'parsed') or inner_instruction.parsed is None:
                continue

            destination = inner_instruction.parsed['info'].get('destination')
            if _is_fee_instruction(inner_instruction, str(fee_account),
                                   destination, route_info.stack_height):
                if inner_instruction.parsed['type'] == 'transfer':
                    account_info = await self._account_info_manager.get_account_info(destination)
                    mint = account_info.value.data.parsed['info']['mint']
                else:
                    mint = inner_instruction.parsed['info']['mint']

                if inner_instruction.parsed['type'] == 'transferChecked':
                    amount = inner_instruction.parsed['info']['tokenAmount']['amount']
                else:
                    amount = inner_instruction.parsed['info']['amount']

                return {'mint': mint, 'amount': amount, 'account': destination}

        return None
