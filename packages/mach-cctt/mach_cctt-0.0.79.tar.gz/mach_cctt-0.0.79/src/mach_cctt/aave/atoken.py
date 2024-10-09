import functools

from eth_account.signers.local import LocalAccount
from eth_typing import ChecksumAddress
from mach_client import ChainId, Token
from web3 import AsyncWeb3

from .. import config


@functools.cache
async def get_all_atokens(w3: AsyncWeb3, chain: ChainId) -> dict[str, ChecksumAddress]:
    contract_address = config.aave_pool_data_provider_addresses[chain]
    pool_data_provider = w3.eth.contract(address=contract_address, abi=config.aave_pool_data_provider_abi)  # type: ignore

    # Tuples (symbol, address) where the symbol is of the form "a<first 3 letters of chain name><symbol name>", ie. aArbUSDC
    atokens: list[tuple[str, ChecksumAddress]] = (
        await pool_data_provider.functions.getAllATokens().call()
    )

    return {symbol[4:]: address for symbol, address in atokens}


async def get_atoken_balance(
    w3: AsyncWeb3, token: Token, account: LocalAccount
) -> int:
    chain = token.chain.id
    atokens = await get_all_atokens(w3, chain)

    token_address = atokens[token.symbol]
    token_contract = w3.eth.contract(address=token_address, abi=config.erc20_abi)  # type: ignore
    balance = await token_contract.functions.balanceOf(account.address).call()

    if native_token_address := atokens.get(f"{token.symbol}n"):
        native_token_contract = w3.eth.contract(
            address=native_token_address, abi=config.erc20_abi
        )
        balance += await native_token_contract.functions.balanceOf(
            account.address
        ).call()

    return balance
