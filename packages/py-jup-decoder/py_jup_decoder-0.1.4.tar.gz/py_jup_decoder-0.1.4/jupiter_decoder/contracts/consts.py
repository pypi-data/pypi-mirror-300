from solders.pubkey import Pubkey

JUPITER_V6_PROGRAM_ID = Pubkey.from_string('JUP6LkbZbjS1jKKwapdHNy74zcZ3tLUZoi5QNyVTaV4')
TOKEN_PROGRAM_ID = Pubkey.from_string('TokenkegQfeZyiNwAJbNbGKPFXCWuBvf9Ss623VQ5DA')
TOKEN_2022_PROGRAM_ID = Pubkey.from_string('TokenzQdBNbLqP5VEhdkAS6EPFLC1PHnBqCXEpPxuEb')

TRANSFER_INSTRUCTION_TYPES = {
    'transfer',
    'transferChecked',
    'transferCheckedWithFee',
    'mintTo',
    'burn',
}

AMM_TYPES = {
    'DjVE6JNiYqPL2QXyCUUh8rNjHrbz9hXHNYt99MQ59qw1': 'Orca v1',
    '9W959DqEETiGZocYWCQPaJ6sBmUzgfxXfqGeTEdp3aQP': 'Orca',
    'MERLuDFBMmsHnsBPZw2sDQZHvXFMwp8EdjudcU2HKky': 'Mercurial',
    '9xQeWvG816bUx9EPjHmaT23yvVM2ZWbrrpZb9PusVFin': 'Serum',
    '675kPX9MHTjS2zt1qfr1NYHuzeLXfQM9H24wFSUt1Mp8': 'Raydium',
    'SSwpkEEcbUqx4vtoEByFjSkhKdCT862DNVb52nZg1UZ': 'Saber',
    'PSwapMdSai8tjrEXcxFeQth87xC4rRsa4VA5mhGhXkP': 'Penguin',
    'AMM55ShdkoGRB5jVYPjWziwk8m5MpwyDgsMWHaMSQWH6': 'Aldrin',
    'CURVGoZn8zycx6FXwwevgBTB2gVvdbGTEpvMJDbgs2t4': 'Aldrin v2',
    'SSwpMgqNDsyV7mAgN9ady4bDVu5ySjmmXejXvy2vLt1': 'Step',
    'CTMAxxk34HjKWxQ3QLZK1HpaLXmBveao3ESePXbiyfzh': 'Cropper',
    'SCHAtsf8mbjyjiv4LkhLKutTf6JnZAbdJKFkXQNMFHZ': 'Sencha',
    'CLMM9tUoggJu2wagPkkqs9eFG4BWhVBZWkP1qv3Sp7tR': 'Crema',
    'EewxydAPCCVuNEyrVN68PuSYdQ7wKn27V9Gjeoi8dy3S': 'Lifinity',
    'SSwapUtytfBdBn1b9NUGG6foMVPtcWgpRU32HToDUZr': 'Saros',
    'whirLbMiicVdio4qvUfM5KAg6Ct8VwpYzGff3uctyCc': 'Whirlpool',
    'cysPXAjehMpVKUapzbMCCnpFxUFFryEWEaLgnb9NrR8': 'Cykura',
    'MarBmsSgKXdrN1egZf5sqe1TMai9K1rChYNDJgjq7aD': 'Marinade',
    'Dooar9JkhdZ7J3LHN3A7YCuoGRUggXhQaG4kijfLGU2j': 'Stepn',
    'Eo7WjKq67rjJQSZxS6z3YkapzY3eMj6Xy8X5EQVn5UaB': 'Meteora',
    'HyaB3W9q6XdA5xwpU4XnSZV94htfmbmqJXZcEbRaJutt': 'Invariant',
    '7WduLbRfYhTJktjLw5FDEyrqoEv61aTTCuGAetgLjzN5': 'GooseFX',
    'DecZY86MU5Gj7kppfUCEmd4LbXXuyZH1yHaP2NTqdiZB': 'Saber Decimal Wrapper',
    'D3BBjqUdCYuP18fNvvMbPAZ8DpcRi4io2EsYHQawJDag': 'Balansol',
    'dp2waEWSBy5yKmq65ergoU3G6qRLmqa6K7We4rZSKph': 'Dradex',
    '2wT8Yq49kHgDzXuPxZSaeLaH1qbmGXtEyPy64bL7aD3c': 'Lifinity v2',
    'CAMMCzo5YL8w4VFF8KVHrK22GGUsp5VTaW7grrKgrWqK': 'Raydium CLMM',
    'srmqPvymJeFKQ4zGQed1GFppgkRHL9kaELCbyksJtPX': 'Openbook',
    '9tKE7Mbmj4mxDjWatikzGAtkoWosiiZX9y6J4Hfm2R8H': 'Marco Polo',
    'PhoeNiXZ8ByJGLkxNfZRnkUfjvmuYqLR89jjFHGqdXY': 'Phoenix',
    '2KehYt3KsEQR53jYcxjbQp2d2kCp4AkuQW68atufRwSr': 'Symmetry',
    'BSwp6bEBihVLdqJRKGgzjcGLHkcTuzmSo1TQkHepzH8p': 'BonkSwap',
    'FLUXubRmkEi2q6K3Y9kBPg9248ggaZVsoSFhtJHSrm1X': 'FluxBeam',
    'treaf4wWBBty3fHdyBpo35Mz84M8k3heKXmjmi9vFt5': 'Helium Network',
    'stkitrT1Uoy18Dk1fTrgPw8W6MVzoCfYoAFT4MLsmhq': 'unstake.it',
    'GFXsSL5sSaDfNFQUYsHekbWBW1TsFdjDYzACh62tEHxn': 'GooseFX v2',
    'PERPHjGBqRHArX4DySjwM6UJHiR3sWAatqfdBS2qQJu': 'Perps',
    'LBUZKhRxPF3XUpBCjp4YzTKgLccjZhTSDM9YuVaPwxo': 'Meteora DLMM',
    'SwaPpA9LAaLfeLi3a68M4DjnLqgtticKg6CnyNwgAC8': 'Token Swap',
    'opnb2LAfJYbRMAHHvqjCwQxanZn7ReEHp1k81EohpZb': 'Openbook v2',
    'DSwpgjMvXhtGn6BsbqmacdBZyfLj6jSWf3HJpdJtmg6N': 'Dexlab',
    'C1onEW2kPetmHmwe74YC1ESx3LnFEpVau6g2pg4fHycr': 'Clone',
    'CPMMoo8L3F4NbTegBCKVNunggL7H1ZpdTHKxQB5qKP1C': 'Raydium CP',
    'H8W3ctz92svYg6mkn1UtGfu2aQr2fnUFHM1RhScEtQDt': 'Cropper Whirlpool',
    '5ocnV1qiCgaQR8Jb8xWnVbApfaygJ8tNoZfgPwsgx9kx': 'Sanctum S',
    'Gswppe6ERWKpUTXvRPfXdzHhiCyJvLadVvXGfdpBqcE1': 'GuacSwap',
    'DEXYosS6oEGvk8uCDayvwEZz4qEyDJRf9nFgYCaqPMTm': '1DEX',
    'swapFpHZwjELNnjvThjajtiVmkz3yPQEHjLtka2fwHW': 'stabbleWeightedSwap',
    '6EF8rrecthR5Dkzon8Nwu78hRvfCKubJ14M5uBEwF6P': 'Pump.Fun',
    'obriQD1zbpyLz95G5n7nJe6a4DPjpFwa5XYPoNm113y': 'obric'
}

SWAP_IN_OUT_ACCOUNTS_POSITION = {
    'Aldrin': {'in': 7, 'out': 8},
    'AldrinV2': {'in': 7, 'out': 8},
    'Balansol': {'in': 6, 'out': 9},
    'Clone': {'in': 4, 'out': 5},
    'Crema': {'in': 4, 'out': 5},
    'Cropper': {'in': 4, 'out': 7},
    'Cykura': {'in': 3, 'out': 4},
    'DeltaFi': {'in': 2, 'out': 3},
    'Dradex': {'in': 9, 'out': 10},
    'GooseFX': {'in': 8, 'out': 9},
    'GooseFxv2': {'in': 5, 'out': 6},
    'HeliumTreasuryManagementRedeemV0': {'in': 5, 'out': 6},
    'Invariant': {'in': 3, 'out': 4},
    'Lifinity': {'in': 3, 'out': 4},
    'LifinityV2': {'in': 3, 'out': 4},
    'MarcoPolo': {'in': 6, 'out': 7},
    'MarinadeDeposit': {},
    'MarinadeUnstake': {},
    'Mercurial': {'in': -2, 'out': -1},
    'Meteora': {'in': 1, 'out': 2},
    'MeteoraDlmm': {'in': 4, 'out': 5},
    'OpenBookV2': {'in': 9, 'out': 10},
    'Perps': {'in': 1, 'out': 2},
    'PerpsAddLiquidity': {'in': 1, 'out': 2},
    'PerpsRemoveLiquidity': {'in': 2, 'out': 1},
    'PerpsV2': {'in': 1, 'out': 2},
    'PerpsV2AddLiquidity': {'in': 1, 'out': 2},
    'PerpsV2RemoveLiquidity': {'in': 2, 'out': 1},
    'Phoenix': {'in': 4, 'out': 5},
    'Raydium': {'in': 14, 'out': 15},
    'RaydiumClmm': {'in': 3, 'out': 4},
    'RaydiumClmmV2': {'in': 3, 'out': 4},
    'RaydiumCP': {'in': 4, 'out': 5},
    'Saber': {'in': 3, 'out': 6},
    'SaberAddDecimalsDeposit': {'in': 4, 'out': 5},
    'SaberAddDecimalsWithdraw': {'in': 5, 'out': 4},
    'SanctumS': {'in': 3, 'out': 4},
    'SanctumSAddLiquidity': {'in': 2, 'out': 3},
    'SanctumSRemoveLiquidity': {'in': 3, 'out': 2},
    'sencha': {'in': 3, 'out': 6},
    'Openbook': {'in': 6, 'out': {'ask': 6, 'bid': 5}},
    'Serum': {'in': 6, 'out': {'ask': 6, 'bid': 5}},
    'StakeDexStakeWrappedSol': {'in': 1, 'out': 2},
    'StakeDexSwapViaStake': {},
    'StakeDexPrefundWithdrawStakeAndDepositStake': {'in': 1, 'out': 2},
    'Step': {'in': 3, 'out': 6},
    'Symmetry': {'in': 4, 'out': 6},
    'TokenSwap': {'in': 3, 'out': 6},
    'TokenSwapV2': {'in': 3, 'out': 6},
    'Whirlpool': {'in': 3, 'out': 5},
    'WhirlpoolSwapV2': {'in': 7, 'out': 9},
    'OneIntro': {'in': 6, 'out': 7},
    'StabbleWeightedSwap': {'in': 1, 'out': 2},
    'PumpdotfunWrappedBuy': {'in': 5, 'out': 6},
    'PumpdotfunWrappedSell': {'in': 5, 'out': 6},
    'Obric': {'in': -6, 'out': -7}
}

SWAP_DIRECTION_ARGS = {
    'SIDE': [
        '9xQeWvG816bUx9EPjHmaT23yvVM2ZWbrrpZb9PusVFin',
        'AMM55ShdkoGRB5jVYPjWziwk8m5MpwyDgsMWHaMSQWH6',
        'CURVGoZn8zycx6FXwwevgBTB2gVvdbGTEpvMJDbgs2t4',
        'dp2waEWSBy5yKmq65ergoU3G6qRLmqa6K7We4rZSKph',
        'opnb2LAfJYbRMAHHvqjCwQxanZn7ReEHp1k81EohpZb',
        'PhoeNiXZ8ByJGLkxNfZRnkUfjvmuYqLR89jjFHGqdXY',
        'opnb2LAfJYbRMAHHvqjCwQxanZn7ReEHp1k81EohpZb',
        'srmqPvymJeFKQ4zGQed1GFppgkRHL9kaELCbyksJtPX',
    ],
    'A_TO_B': [
        'H8W3ctz92svYg6mkn1UtGfu2aQr2fnUFHM1RhScEtQDt',
        'whirLbMiicVdio4qvUfM5KAg6Ct8VwpYzGff3uctyCc',
        'CLMM9tUoggJu2wagPkkqs9eFG4BWhVBZWkP1qv3Sp7tR',
    ],
    'X_TO_Y': [
        'HyaB3W9q6XdA5xwpU4XnSZV94htfmbmqJXZcEbRaJutt',
        '9tKE7Mbmj4mxDjWatikzGAtkoWosiiZX9y6J4Hfm2R8H',
        'BSwp6bEBihVLdqJRKGgzjcGLHkcTuzmSo1TQkHepzH8p',
        'Gswppe6ERWKpUTXvRPfXdzHhiCyJvLadVvXGfdpBqcE1',
    ],
    'OBRIC_X_TO_Y': [
        'obriQD1zbpyLz95G5n7nJe6a4DPjpFwa5XYPoNm113y'
    ],
    'QUANTITY_IS_COLLATERAL': ['C1onEW2kPetmHmwe74YC1ESx3LnFEpVau6g2pg4fHycr'],
}

PLATFORM_FEE_ACCOUNTS_POSITION = {
    'route': 6,
    'route_with_token_ledger': 6,
    'shared_accounts_route': 9,
    'shared_accounts_route_with_token_ledger': 9,
    'shared_accounts_exact_out_route': 9,
    'exact_out_route': 7,
}

MULTI_STEP_SWAPS = [
    'Openbook',
    'Serum',
    'StakeDexPrefundWithdrawStakeAndDepositStake'
]

ROUTE_NAMES = [
    'route', 
    'route_with_token_ledger',
    'shared_accounts_route',
    'shared_accounts_route_with_token_ledger',
    'shared_accounts_exact_out_route',
    'exact_out_route'
]
