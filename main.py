import asyncio
import random
import jupiter

from restore_wallet import restore_wallet
from playwright.async_api import async_playwright, expect

from data import config
from data.wallets import WALLETS, get_amount
from data.swaps import generate_token_way

from utils import check_webdriver, check_user_agent, format_proxy, get_solana_price
from loguru import logger


async def main():
    for wallet in WALLETS:
        async with async_playwright() as p:
            proxy = None
            if config.USE_PROXY:
                proxy = await format_proxy(wallet.proxy)
            
            context_kwargs = {
                'headless': False,
                'args': [
                    f"--disable-extensions-except={config.BP_EXTENTION_PATH}",
                    f"--load-extension={config.BP_EXTENTION_PATH}",
                    f"--disable-blink-features=AutomationControlled",
                    "--disable-extensions",
                    "--disable-infobars",
                    "--no-sandbox",
                    "--disable-setuid-sandbox"
                ],
                'slow_mo': 500,
                'user_agent': wallet.user_agent,
            }

            if proxy:
                context_kwargs['proxy'] = {
                    'server': proxy['server'],
                    'username': proxy['username'],
                    'password': proxy['password'],
            }
            context = await p.chromium.launch_persistent_context('', **context_kwargs)

            # await check_webdriver(context=context)
            # await check_user_agent(context=context)
            # await asyncio.sleep(1000)
            
            try:
                logger.info(f'PROXY | {wallet.proxy}')
                await restore_wallet(context=context, wallet=wallet)
                await jupiter.connect_wallet(context=context, wallet=wallet)
                START = float(wallet.amount)
                tokens = await generate_token_way(config.VALUE, START)
                
                for i in range(len(tokens) - 1):
                   delay = random.randint(config.TX_DELAY_RANGE[0], config.TX_DELAY_RANGE[1])
                   current_token = tokens[i]
                   next_token = tokens[i + 1]
                   await jupiter.swap(context=context, from_token=current_token, to_token=next_token, amount=wallet.amount, count=i)
                   logger.info(f"Delay between transactions | {delay} sec")
                   await asyncio.sleep(delay)
                
                logger.info(f"--------------------END--------------------")
                logger.success(f"ALL SWAPS END FOR - {wallet.address}")
                
                await asyncio.sleep(4)
                
                await context.close()
                logger.info(f"Browser closing")
            except Exception as e:
                logger.error(f'Error | {e}')
    logger.success('All wallets end 🦍')
    logger.success('🐒 tg - @cryptomakaquich 🐒')


if __name__ == '__main__':
    asyncio.run(main())

