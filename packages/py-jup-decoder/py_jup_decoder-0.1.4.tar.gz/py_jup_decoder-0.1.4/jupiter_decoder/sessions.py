import abc
import logging
import time
from decimal import Decimal
from typing import Dict, Union

import aiohttp
from solders.pubkey import Pubkey


class BaseSession(metaclass=abc.ABCMeta):
    def __init__(
            self,
            base_url: str = 'https://localhost',
    ):
        self._base_url = base_url
        connector = aiohttp.TCPConnector(
            ttl_dns_cache=60,
            enable_cleanup_closed=True
        )
        self._session = aiohttp.ClientSession(
            base_url=base_url,
            connector=connector,
            timeout=aiohttp.ClientTimeout(total=60)
        )

    def __del__(self):
        self._session.connector.close()


class TokensJupSession(BaseSession):
    def __init__(self):
        # https://www.jupresear.ch/t/ecosystem-master-token-list/19786
        self._token_infos_dict: Dict[str, str] = {}
        super().__init__('https://tokens.jup.ag')

    async def get_token_info(self, mint: Union[str, Pubkey]):
        if isinstance(mint, Pubkey):
            mint = str(mint)

        if mint in self._token_infos_dict.keys():
            return self._token_infos_dict[mint]

        url = '/token/{0}'.format(mint)
        try:
            resp = await self._session.get(url)
            resp_json = await resp.json()
            self._token_infos_dict[mint] = resp_json
            return resp_json
        except Exception as e:
            logging.error(
                f'Failed to fetch request from endpoint {self._base_url + url}, {e}',
                exc_info=True,
            )

        return None


class PriceJupSession(BaseSession):
    def __init__(self):
        self._prices_dict: Dict[str, Decimal] = {}
        self._ttls_dict: Dict[str, int] = {}
        super().__init__('https://price.jup.ag')

    async def get_price_in_usd_by_mint(self, mint: Union[str, Pubkey]):
        if isinstance(mint, Pubkey):
            mint = str(mint)

        mint_contains = mint in self._prices_dict.keys() and mint in self._ttls_dict.keys()

        # cache for 5 secs
        if mint_contains and int(time.time()) - self._ttls_dict[mint] < 5:
            return self._prices_dict[mint]

        url = '/v4/price?ids={0}'.format(mint)
        try:
            resp = await self._session.get(url)
            resp_json = await resp.json()

            if mint in resp_json['data']:
                price = Decimal(resp_json['data'][mint]['price'])
                self._prices_dict[mint] = price
                self._ttls_dict[mint] = int(time.time())

                return price
        except Exception as e:
            logging.error(
                f'Failed to fetch request from endpoint {self._base_url + url}, {e}',
                exc_info=True,
            )

        return None




