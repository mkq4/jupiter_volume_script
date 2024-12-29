import asyncio
import requests

async def format_proxy(proxy: str) -> dict:
    username_password, server_port = proxy.replace('http://', '').split('@')
    username, password = username_password.split(':')
    server, port = server_port.split(':')
    proxy = {
        "server": f"http://{server}:{port}",
        "username": username,
        "password": password,
    }
    return proxy


async def check_webdriver(context):
    page = await context.new_page()
    await page.goto("https://intoli.com/blog/not-possible-to-block-chrome-headless/chrome-headless-test.html")
    await asyncio.sleep(1000)
    
async def check_user_agent(context):
    page = await context.new_page()
    await page.goto("https://2ip.ru/")
    await asyncio.sleep(1000)
    
async def get_solana_price():
    url = "https://api.binance.com/api/v3/ticker/price?symbol=SOLUSDT"
    response = requests.get(url)
    
    if response.status_code == 200:
        data = response.json()
        price = data['price']
        return float(price)
    else:
        print("Ошибка при получении данных:", response.status_code)
        return None

