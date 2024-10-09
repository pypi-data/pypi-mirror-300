from setuptools import setup

setup(
    name='py-jup-decoder',
    version='0.1.4',
    description='Copied from https://github.com/jup-ag/instruction-parser',
    url='https://github.com/vladiolus3/jupiterDecoder',
    packages=['jupiter_decoder', 'jupiter_decoder.contracts'],
    install_requires=[
        'solana>=0.34.3',
        'solders>=0.21.0',
        'anchorpy>=0.20.1',
        'aiohttp>=3.10.9',
        'base58>=2.1.1'
    ]
)
