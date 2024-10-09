from jupiter_decoder.contracts.route_info import RouteInfo


def get_initial_and_final_swap_positions(route_info: RouteInfo):
    def _is_circular(_route_plan: dict):
        if _route_plan is None or len(_route_plan) == 0:
            return False

        _index_map = {route.input_index: route.output_index for route in route_plan}

        _visited = set()
        _current_index = _route_plan[0].input_index
        while True:
            if _current_index in _visited:
                return _current_index == _route_plan[0].input_index
            _visited.add(_current_index)
            if _current_index not in _index_map:
                return False
            _current_index = _index_map[_current_index]

    route_plan = route_info.data.route_plan
    input_index = 0
    output_index = len(route_plan)

    initial_positions = []
    [initial_positions.append(index) for index, route in enumerate(route_plan)
     if route.input_index == input_index]

    final_positions = []
    [final_positions.append(index) for index, route in enumerate(route_plan)
     if route.output_index == output_index]

    if len(final_positions) == 0 and _is_circular(route_plan):
        [final_positions.append(index) for index, route in enumerate(route_plan)
         if route.output_index == 0]

    return initial_positions, final_positions


def get_instruction_name_and_transfer_authority_and_last_account(route_info: RouteInfo):
    def _get_transfer_authority_index(_instruction_name: str):
        if _instruction_name in {"route", "exact_out_route", "route_with_token_ledger"}:
            return 1
        elif _instruction_name in {"shared_accounts_route", "shared_accounts_route_with_token_ledger",
                                   "shared_accounts_exact_out_route"}:
            return 2
        return None

    transfer_authority = str(route_info.accounts[_get_transfer_authority_index(route_info.name)])
    last_account = str(route_info.accounts[len(route_info.accounts) - 1])
    return route_info.name, transfer_authority, last_account


def get_exact_out_amount(route_info: RouteInfo):
    if is_exact_in(route_info.name):
        return str(route_info.data.quoted_out_amount)
    return None


def get_exact_in_amount(route_info: RouteInfo):
    if is_exact_out(route_info.name):
        return str(route_info.data.quoted_in_amount)
    return None


def is_exact_in(name: str):
    return name in {
        "route",
        "route_with_token_ledger",
        "shared_accounts_route",
        "shared_accounts_route_with_token_ledger"
    }


def is_exact_out(name: str):
    return name in {
        "shared_accounts_exact_out_route",
        "exact_out_route"
    }

