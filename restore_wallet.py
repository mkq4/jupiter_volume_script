from playwright.async_api import BrowserContext, expect
import asyncio
from loguru import logger

from data.models import Wallet
from data import config


async def restore_wallet(context: BrowserContext, wallet: Wallet) -> bool:
    try:
        logger.info(f'{wallet.address} | Starting recover wallet')
        page = context.pages[0]
        await page.goto(f'chrome-extension://{config.BP_EXTENTION_IDENTIFIER}/options.html?onboarding=true ')
        await page.bring_to_front()

        await page.wait_for_load_state()

        await page.locator('//*[@id="options"]/span/span/div/div/div/div/div/div[1]/div/div/div[3]/div/span[2]/button').click()
        await page.locator('//*[@id="options"]/span/span/div/div/div/div/div[1]/div[1]/div/div/div[2]/div[3]/button[1]').click()
        await page.locator('//*[@id="options"]/span/span/div/div/div/div/div[1]/div[1]/div/div/div[2]/span[4]/button').click()

        await page.locator('textarea').fill(wallet.private_key)

        await page.locator('//*[@id="options"]/span/span/div/div/div/div/div[1]/div[1]/div/div/div[3]/span/button').click()

        inputs = page.locator('[type="password"]')
        await inputs.nth(0).fill(config.BP_EXTENTION_PASSWORD)
        await inputs.nth(1).fill(config.BP_EXTENTION_PASSWORD)

        await page.locator('[type="checkbox"]').check()

        await page.locator('//*[@id="options"]/span/span/div/div/div/div/div[1]/div[1]/div/form/div[3]/span/button').click()

        await asyncio.sleep(4)

        await page.goto(f'chrome-extension://{config.BP_EXTENTION_IDENTIFIER}/popout.html')
        await page.bring_to_front()
        
        wallet_balance = page.locator('//*[@id="root"]/span[1]/span/div/div/div[7]/div/div/div[2]/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div/div/div/div/div/div/div[1]/div/div[2]/div[2]/div/div/div/div[2]/div/div[1]/div/div[2]/div[1]/div/div/div[1]/div/div[1]/div/div[1]/div[1]/div[1]/span')
        await expect(wallet_balance).to_be_visible()
        await asyncio.sleep(2)
        
        
        logger.success(f'{wallet.address} | Wallet Ready To Work')
        
        
        return True

    except Exception as err:
        logger.error(f'{wallet.address} | Not Recovered ({err})')
        logger.info(f'Error when getting an account, trying again')

    return False
