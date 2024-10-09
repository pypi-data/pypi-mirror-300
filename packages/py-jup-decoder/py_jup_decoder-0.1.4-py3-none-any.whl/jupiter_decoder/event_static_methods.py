from typing import Sequence, Union

from solders.transaction_status import EncodedTransactionWithStatusMeta, ParsedInstruction, \
    UiPartiallyDecodedInstruction, UiCompiledInstruction

from jupiter_decoder.contracts.consts import (TOKEN_PROGRAM_ID, TOKEN_2022_PROGRAM_ID,
                                              TRANSFER_INSTRUCTION_TYPES, AMM_TYPES,
                                              MULTI_STEP_SWAPS, SWAP_IN_OUT_ACCOUNTS_POSITION,
                                              SWAP_DIRECTION_ARGS)
from jupiter_decoder.contracts.route_info import RouteInfo
from jupiter_decoder.contracts.swap import Swap
from jupiter_decoder.contracts.transfer_instructions import TransferInstructions

InnerInstruction = Union[ParsedInstruction, UiPartiallyDecodedInstruction, UiCompiledInstruction]


def _get_inner_instructions(transaction_with_meta: EncodedTransactionWithStatusMeta,
                            route_info: RouteInfo):
    for instruction in transaction_with_meta.meta.inner_instructions:
        if instruction.index == route_info.index:
            return instruction.instructions
    return []


def _is_swap_instruction(instruction: InnerInstruction, route_ix_stack_height: int):
    return (str(instruction.program_id) in AMM_TYPES
            and instruction.stack_height == route_ix_stack_height + 1)


def _is_fee_instruction(inner_instruction: InnerInstruction,
                        fee_account: str,
                        destination: str,
                        route_ix_stack_height: int):
    ix_type = inner_instruction.parsed['type']
    stack_height = inner_instruction.stack_height
    return ((ix_type == 'transfer' or ix_type == 'transferChecked') and
            stack_height == route_ix_stack_height + 1 and
            fee_account == destination)


def _get_in_and_out_transfer_instructions(inner_instructions: Sequence[InnerInstruction],
                                          swap: Swap):
    def _is_transfer_instruction(_instruction: InnerInstruction, _swap_ix_stack_height: int):
        if (_instruction.program_id == TOKEN_PROGRAM_ID or
                _instruction.program_id == TOKEN_2022_PROGRAM_ID):
            _ix_type = _instruction.parsed['type']
            _ix_stack_height = _instruction.stack_height
            if _ix_type in TRANSFER_INSTRUCTION_TYPES and _ix_stack_height >= _swap_ix_stack_height + 1:
                return _ix_type
        return None

    transfer_instructions = TransferInstructions()
    transfer_instructions.in_transfers = []
    transfer_instructions.out_transfers = []
    in_account = str(swap.in_account)
    out_account = str(swap.out_account)

    index = swap.instruction_index + 1

    while index < swap.next_swap_index:
        inner_instruction = inner_instructions[index]
        ix_type = _is_transfer_instruction(inner_instruction, swap.stack_height)
        if ix_type is not None:
            source = inner_instruction.parsed['info'].get('source', '')
            destination = inner_instruction.parsed['info'].get('destination', '')

            if ix_type == 'transfer' or ix_type == 'transferChecked':
                if in_account == source:
                    transfer_instructions.in_transfers.append(inner_instruction)
                if out_account == destination:
                    transfer_instructions.out_transfers.append(inner_instruction)

            elif ix_type == 'burn' and in_account == inner_instruction.parsed['info']['account']:
                transfer_instructions.in_transfers.append(inner_instruction)

            elif ix_type == 'mintTo' and out_account == inner_instruction.parsed['info']['account']:
                transfer_instructions.out_transfers.append(inner_instruction)

        index = index + 1

    return transfer_instructions


def _get_swaps(inner_instructions: Sequence[InnerInstruction],
               route_info: RouteInfo):
    swaps = []
    index = 0

    while index < len(inner_instructions):
        if _is_swap_instruction(inner_instructions[index], route_info.stack_height):
            route_plan_index = len(swaps)
            route_plan = route_info.data.route_plan[route_plan_index]
            if route_plan.swap.__class__.__name__ in MULTI_STEP_SWAPS:
                swap = _get_multi_step_swap(inner_instructions, index,
                                            route_plan.swap, route_info.stack_height)
            else:
                swap = _get_swap(inner_instructions, index,
                                 route_plan.swap, route_info.stack_height)
            swaps.append(swap)
            index = swap.next_swap_index - 1

        index += 1

    return swaps


def _get_multi_step_swap(inner_instructions: Sequence[InnerInstruction],
                         swap_ix_index: int,
                         swap_data: any,
                         route_ix_stack_height: int):
    swap_instruction = inner_instructions[swap_ix_index]
    swap_ix_name = swap_data.__class__.__name__
    positions = SWAP_IN_OUT_ACCOUNTS_POSITION[swap_ix_name]

    swap = Swap()
    swap.in_account = swap_instruction.accounts[positions['in']]

    index = swap_ix_index + 1
    while (index < len(inner_instructions) and
           (inner_instructions[index].program_id == swap_instruction.program_id or
            not _is_swap_instruction(inner_instructions[index], route_ix_stack_height))):
        current_instruction = inner_instructions[index]
        if current_instruction.program_id == swap_instruction.program_id:
            if swap_ix_name == 'Openbook' or swap_ix_name == 'Serum':
                side = swap_data.side.__class__.__name__
                swap.out_account = current_instruction.accounts[positions['out'][side]]
            elif swap_ix_name == 'StakeDexPrefundWithdrawStakeAndDepositStake':
                swap.out_account = current_instruction.accounts[positions['out']]
        index = index + 1

    swap.instruction_index = swap_ix_index
    swap.stack_height = swap_instruction.stack_height
    swap.next_swap_index = index
    return swap


def _get_swap(inner_instructions: Sequence[InnerInstruction],
              swap_ix_index: int,
              swap_data: any,
              route_ix_stack_height: int):
    def _get_swap_direction(_amm: str, _swap_data: any) -> bool:
        if _amm in SWAP_DIRECTION_ARGS['SIDE']:
            return _swap_data.side.__class__.__name__ == "Ask"

        if _amm in SWAP_DIRECTION_ARGS['A_TO_B']:
            return _swap_data.a_to_b

        if _amm in SWAP_DIRECTION_ARGS['X_TO_Y']:
            return _swap_data.x_to_y

        if _amm in SWAP_DIRECTION_ARGS['QUANTITY_IS_COLLATERAL']:
            return _swap_data.quantity_is_collateral

        return True

    swap = Swap()
    swap_instruction = inner_instructions[swap_ix_index]
    swap_ix_name = swap_data.__class__.__name__
    positions = SWAP_IN_OUT_ACCOUNTS_POSITION[swap_ix_name]
    accounts = swap_instruction.accounts
    in_account_position = len(accounts) + positions['in'] if positions['in'] < 0 else positions['in']
    out_account_position = len(accounts) + positions['out'] if positions['out'] < 0 else positions['out']

    if _get_swap_direction(str(swap_instruction.program_id), swap_data):
        swap.in_account, swap.out_account = accounts[in_account_position], accounts[out_account_position]
    else:
        swap.in_account, swap.out_account = accounts[out_account_position], accounts[in_account_position]

    index = swap_ix_index + 1
    while (index < len(inner_instructions) and
           not _is_swap_instruction(inner_instructions[index], route_ix_stack_height)):
        index = index + 1

    swap.instruction_index = swap_ix_index
    swap.stack_height = swap_instruction.stack_height
    swap.next_swap_index = index
    return swap






