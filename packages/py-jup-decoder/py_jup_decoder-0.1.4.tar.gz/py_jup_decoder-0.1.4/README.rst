###################
py-jup-decoder
###################

Made by the solution on typescript https://github.com/jup-ag/instruction-parser

*******
Installing
*******

.. code:: sh

   pip install py-jup-decoder

*******
Example
*******

.. code:: python

   SOLANA_RPC_URL = os.getenv('SOLANA_RPC_URL')
   setup_logging(os.getenv('LOGGER_LEVEL'))

   jup_rpc_client = JupRpcClient(SOLANA_RPC_URL)
   txs = await jup_rpc_client.client.get_signatures_for_address(
       Pubkey.from_string('BW6RXbEyug92G3DU8uMzP1SXynCCQMBGBy2tLFp8LbzU'), limit=100)
   tx_ids = [str(tx.signature) for tx in txs.value]

   for tx_id in tx_ids:
       print('tx_id: {0}'.format(tx_id))
       decoded_tx = await jup_rpc_client.decode_transaction(tx_id)
       logging.info('tx_id: {0}, decoded_tx: {1}'.format(
           tx_id, decoded_tx[0] if len(decoded_tx) > 0 else [])
       )

*********
Resources
*********

* PyPI page: http://pypi.python.org/pypi/django-downloadview
* Original project: https://github.com/jup-ag/instruction-parser