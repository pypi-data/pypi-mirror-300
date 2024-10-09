import logging
from typing import Union

from solana.rpc.async_api import AsyncClient
from solders.pubkey import Pubkey
from solders.rpc.responses import GetAccountInfoMaybeJsonParsedResp

from jupiter_decoder.contracts.consts import TOKEN_2022_PROGRAM_ID
from jupiter_decoder.contracts.fee_config import FeeConfig, TransferFee
from jupiter_decoder.contracts.errors import SolanaTransactionFetchError

PubkeyOrStr = Union[Pubkey, str]


class AccountInfoManager:
    def __init__(self, base_url: str = 'https://api.mainnet-beta.solana.com'):
        self._client = AsyncClient(base_url)
        self._base_url = base_url
        self._account_info_dict: dict[Pubkey, GetAccountInfoMaybeJsonParsedResp] = {}

    async def get_account_info(self, account_id: PubkeyOrStr) -> GetAccountInfoMaybeJsonParsedResp:
        if isinstance(account_id, str):
            account_id = Pubkey.from_string(account_id)

        if account_id in self._account_info_dict:
            return self._account_info_dict[account_id]

        num_retries = 3
        while num_retries > 0:
            try:
                account_info = await self._client.get_account_info_json_parsed(account_id)
                logging.info('fetched payload {0}'.format(account_id))
                self._account_info_dict[account_id] = account_info
                return account_info
            except Exception as e:
                logging.warning('failed to handle request, error: {0}'.format(e), exc_info=True)

            num_retries -= 1
            logging.debug('retrying to get response from endpoint {0}'.format(self._base_url))

        logging.critical('failed fetching from endpoint {0}'.format(self._base_url), exc_info=True)

        raise SolanaTransactionFetchError('exception occurred while requesting from endpoint {0}'
                                          .format(self._base_url))

    async def get_fee_config(self, account_id: PubkeyOrStr):
        account_info = await self.get_account_info(account_id)

        if account_info.value is None or account_info.value.owner != TOKEN_2022_PROGRAM_ID:
            return None

        data = account_info.value.data

        if data is not None:
            extensions = data.parsed['info']['extensions']
            for item in extensions:
                if isinstance(item, dict) and item['extension'] == 'transferFeeConfig':
                    state = item['state']
                    fee_config = FeeConfig()
                    fee_config.transfer_fee_config_authority = Pubkey.from_string(state['transferFeeConfigAuthority'])
                    fee_config.withdraw_withheld_authority = Pubkey.from_string(state['withdrawWithheldAuthority'])
                    fee_config.withheld_amount = state['withheldAmount']

                    older_transfer_fee = TransferFee()
                    older_transfer_fee.epoch = state['olderTransferFee']['epoch']
                    older_transfer_fee.maximum_fee = state['olderTransferFee']['maximumFee']
                    older_transfer_fee.transfer_fee_basis_points = state['olderTransferFee']['transferFeeBasisPoints']

                    newer_transfer_fee = TransferFee()
                    newer_transfer_fee.epoch = state['newerTransferFee']['epoch']
                    newer_transfer_fee.maximum_fee = state['newerTransferFee']['maximumFee']
                    newer_transfer_fee.transfer_fee_basis_points = state['newerTransferFee']['transferFeeBasisPoints']

                    fee_config.older_transfer_fee = older_transfer_fee
                    fee_config.newer_transfer_fee = newer_transfer_fee
                    return fee_config
