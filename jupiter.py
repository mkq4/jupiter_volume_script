import asyncio

from playwright.async_api import expect, BrowserContext
from loguru import logger
from data.models import Token, Wallet


jupiter_url = "https://jup.ag/swap"

async def connect_wallet(context: BrowserContext, wallet: Wallet):
    logger.info(f'{wallet.address} | Connecting wallet to jup.ag')
    jupiter_page = await context.new_page()
    # jupiter_page = context.pages[0]
    await jupiter_page.goto(jupiter_url)
    await jupiter_page.bring_to_front()
    
    await jupiter_page.wait_for_load_state()
    
    try:
        connect_wallet_btn = jupiter_page.locator('//*[@id="__next"]/div[2]/div[1]/div[1]/div[4]/div[2]/button[2]')
        await expect(connect_wallet_btn).to_be_visible()
        await connect_wallet_btn.click()
        
        backpack_img = jupiter_page.get_by_text('Backpack')
        await expect(backpack_img).to_be_visible()
        await backpack_img.click()
        
        
        
        all_pages = context.pages
        extension_page = next(page for page in all_pages if page.url.startswith("chrome-extension://"))
        
        await extension_page.bring_to_front()
        submit_wallet_btn = extension_page.locator('//html/body/div[2]/span/span/div[2]/div[1]/div/div/div[2]/div[2]/div[2]/div/span')
        await asyncio.sleep(5)
        await expect(submit_wallet_btn).to_be_visible()
        await submit_wallet_btn.click()
        await asyncio.sleep(2)
        
        await jupiter_page.bring_to_front()
        
        await asyncio.sleep(2)
        
        jupiter_z_button = jupiter_page.locator('//*[@id="__next"]/div[2]/div[3]/div[2]/div[2]/div[2]/div[2]/form/div[4]/div/div[2]')
        await expect(jupiter_z_button).to_be_visible()
        await jupiter_z_button.click()
        
        
        logger.success(f'{wallet.address} | Successfully connected to jup.ag')
    except Exception as e:
        logger.error(f"error | {e}")
        pass

    return False

async def swap(context, from_token: Token ,to_token: Token, amount: int, count: int):
    to_token_name, to_token_address = list(to_token.items())[0]
    from_token_name, from_token_address = list(from_token.items())[0]
    logger.info(f'| {count + 1} | Starting swap to token - {(to_token_name).upper()}')
    jupiter_page = context.pages[1]
    await jupiter_page.bring_to_front()
    await jupiter_page.wait_for_load_state()
    await asyncio.sleep(2)
    
    try:
        # await asyncio.sleep(100000)
        #выбираем токен для свапа
        
        await asyncio.sleep(2)
        from_token_choose = jupiter_page.locator('//*[@id="__next"]/div[2]/div[3]/div[2]/div[2]/div[2]/div[2]/form/div[1]/div[1]/div[2]/div/button')
        await expect(from_token_choose).to_be_visible()
        await from_token_choose.click()
        
        token_input = jupiter_page.locator('//*[@id="__next"]/div[3]/div[1]/div/div/div[1]/input')
        await expect(token_input).to_be_visible()
        await token_input.type(from_token_address)
        
        from_token_text = f'{from_token_address[:5]}...{from_token_address[-5:]}'
        from_token = jupiter_page.get_by_text(from_token_text)
        await expect(from_token).to_be_visible()
        await from_token.click()
        
        # await asyncio.sleep(100000)
        #токен на который свапаем
        to_token_choose = jupiter_page.locator('//*[@id="__next"]/div[2]/div[3]/div[2]/div[2]/div[2]/div[2]/form/div[1]/div[3]/div[2]/div/button')
        await expect(to_token_choose).to_be_visible()
        await to_token_choose.click()
        
        token_input_to = jupiter_page.locator('//*[@id="__next"]/div[3]/div[1]/div/div/div[1]/input')
        await expect(token_input_to).to_be_visible()
        await token_input_to.type(to_token_address)
        
        swap_token_text = f'{to_token_address[:5]}...{to_token_address[-5:]}'
        swap_text_element = jupiter_page.get_by_text(swap_token_text)
        await expect(swap_text_element).to_be_visible()
        await swap_text_element.click()
        
        #количество токена
        if from_token_name == 'sol':
            from_token_input = jupiter_page.locator('//*[@id="__next"]/div[2]/div[3]/div[2]/div[2]/div[2]/div[2]/form/div[1]/div[1]/div[2]/span/div/input')
            await expect(from_token_input).to_be_visible()
            await asyncio.sleep(1)
            await from_token_input.type(str(amount))
        else: 
            max_btn = jupiter_page.locator('//*[@id="__next"]/div[2]/div[3]/div[2]/div[2]/div[2]/div[2]/form/div[1]/div[1]/div[1]/div/div[2]/button[2]')
            await expect(max_btn).to_be_visible()
            await asyncio.sleep(1)
            await max_btn.click()
            
        await asyncio.sleep(2)
        

        
        # Submit Jupiter button
        submit_jupiter_btn = jupiter_page.locator('//*[@id="__next"]/div[2]/div[3]/div[2]/div[2]/div[2]/div[2]/form/div[6]/button')
        is_disabled = await submit_jupiter_btn.is_disabled() 
        await asyncio.sleep(4)
        
        if is_disabled and from_token_name != 'sol':
            logger.info("Swap button is disabled | trying to retry swap amount")
            await asyncio.sleep(4)
            max_btn = jupiter_page.locator('//*[@id="__next"]/div[2]/div[3]/div[2]/div[2]/div[2]/div[2]/form/div[1]/div[1]/div[1]/div/div[2]/button[2]')
            await expect(max_btn).to_be_visible()
            await max_btn.click()
            
        await asyncio.sleep(2)
        await expect(submit_jupiter_btn).to_be_visible()
        await submit_jupiter_btn.click()
        
        # Береходим в backpack для аодверждения транзакции
        await asyncio.sleep(4)
        backpack_page = context.pages[0]
        await backpack_page.bring_to_front()
        await asyncio.sleep(1)

        submit_backpack_btn_locator = backpack_page.locator('//html/body/div[2]/span/span/div[2]/div[1]/div/div/div[3]/div[2]/div')
        # Ждём кнопку с таймаутом 10 секунд
        await submit_backpack_btn_locator.wait_for(state="visible", timeout=10000)

        # Кликаем на кнопку
        await submit_backpack_btn_locator.click()
        await jupiter_page.bring_to_front()
        
        
        await asyncio.sleep(5)
        
            
        logger.success(f'SWAP | {from_token_name.upper()} - {to_token_name.upper()} | {amount}') 
    except Exception as e:
        logger.error(f"error | {e}")
    return False

