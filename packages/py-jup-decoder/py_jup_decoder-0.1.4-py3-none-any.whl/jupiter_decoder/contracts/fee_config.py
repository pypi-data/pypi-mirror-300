from solders.pubkey import Pubkey


class TransferFee:
    epoch: int
    maximum_fee: int
    transfer_fee_basis_points: int


class FeeConfig:
    transfer_fee_config_authority: Pubkey
    withdraw_withheld_authority: Pubkey
    withheld_amount: int
    older_transfer_fee: TransferFee
    newer_transfer_fee: TransferFee
